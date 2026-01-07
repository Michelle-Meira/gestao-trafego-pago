from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from app.database import get_db
from app.models.user import User, UserCreate, UserLogin, Token, UserUpdate, UserInDB
from app.schemas.user_db import UserDB
from app.core.security import (
    verify_password, get_password_hash, 
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES,
    decode_access_token
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

# Configuração OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- Helper Functions ---
def authenticate_user(db: Session, email: str, password: str):
    """Autentica usuário pelo email e senha"""
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Obtém usuário atual a partir do token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_admin(current_user: UserDB = Depends(get_current_user)):
    """Verifica se usuário atual é admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
    return current_user

# --- Endpoints Públicos ---
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    # Verifica se email já existe
    existing_user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    # Cria novo usuário
    db_user = UserDB(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=user_data.is_active
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login de usuário (retorna token JWT)"""
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cria token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoints Protegidos ---
@router.get("/me", response_model=User)
async def get_me(current_user: UserDB = Depends(get_current_user)):
    """Retorna informações do usuário atual"""
    return current_user

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Altera senha do usuário atual"""
    # Verifica senha atual
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualiza senha
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Senha alterada com sucesso"}

@router.put("/me", response_model=User)
async def update_me(
    user_update: UserUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza informações do usuário atual"""
    update_data = user_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

# --- Endpoints Admin ---
@router.get("/users", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: UserDB = Depends(get_current_active_admin)
):
    """Lista todos os usuários (apenas admin)"""
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: UserDB = Depends(get_current_active_admin)
):
    """Busca usuário por ID (apenas admin)"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin: UserDB = Depends(get_current_active_admin)
):
    """Atualiza usuário (apenas admin)"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: UserDB = Depends(get_current_active_admin)
):
    """Remove usuário (apenas admin)"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "Usuário removido com sucesso"}
