from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Import routers
from app.routers import campaigns, auth  # <-- Adicionado auth

app = FastAPI(
    title="Gestão Tráfego Pago API",
    description="API para gerenciamento de campanhas de tráfego pago",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(campaigns.router)
app.include_router(auth.router)  # <-- Adicionado

@app.get("/")
async def root():
    return {
        "message": "API de Gestão de Tráfego Pago",
        "status": "online",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "endpoints": [
            "/campaigns - Gerenciamento de campanhas",
            "/auth - Autenticação de usuários",
            "/health - Health check"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "gestao-trafego-pago-api"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
