import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ user, onLogout }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          📊 Gestão Tráfego Pago
        </Link>
        
        <div className="d-flex align-items-center">
          {user && (
            <>
              <span className="text-light me-3">
                Olá, <strong>{user.full_name}</strong>
                <span className="badge bg-primary ms-2">{user.role}</span>
              </span>
              
              <div className="dropdown">
                <button 
                  className="btn btn-outline-light dropdown-toggle"
                  type="button"
                  data-bs-toggle="dropdown"
                >
                  👤
                </button>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li>
                    <Link className="dropdown-item" to="/profile">
                      Meu Perfil
                    </Link>
                  </li>
                  <li><hr className="dropdown-divider" /></li>
                  <li>
                    <button className="dropdown-item text-danger" onClick={onLogout}>
                      Sair
                    </button>
                  </li>
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
