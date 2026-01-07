import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = ({ setIsAuthenticated }) => {
  const [email, setEmail] = useState('frontend@teste.com');
  const [password, setPassword] = useState('Frontend123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    console.log('🔄 Tentando login com:', email);
    
    try {
      // FORMATO CORRETO para FastAPI OAuth2PasswordRequestForm
      const formData = new URLSearchParams();
      formData.append('username', email);  // IMPORTANTE: 'username' não 'email'
      formData.append('password', password);
      
      console.log('📤 Enviando:', formData.toString());
      
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });
      
      console.log('📥 Status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error('❌ Erro do servidor:', errorData);
        setError('Credenciais inválidas. Verifique email e senha.');
        return;
      }
      
      const data = await response.json();
      console.log('✅ Login success! Token:', data.access_token.substring(0, 30) + '...');
      
      // Salva token
      localStorage.setItem('token', data.access_token);
      
      // Busca perfil do usuário
      const profileResponse = await fetch('http://localhost:8000/auth/me', {
        headers: {
          'Authorization': `Bearer ${data.access_token}`,
        },
      });
      
      if (!profileResponse.ok) {
        throw new Error('Erro ao buscar perfil');
      }
      
      const userData = await profileResponse.json();
      console.log('👤 User data:', userData);
      
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Atualiza estado e redireciona
      setIsAuthenticated(true);
      navigate('/');
      
    } catch (err) {
      console.error('💥 Erro:', err);
      setError('Erro de conexão com o servidor. Verifique se a API está rodando.');
    } finally {
      setLoading(false);
    }
  };

  const handleTestDirect = async () => {
    // Botão para testar direto no console
    console.log('🧪 Testando login via console...');
    await testLoginAPI(); // A função que colamos acima
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div className="card shadow-lg" style={{ width: '450px' }}>
        <div className="card-body p-4">
          <h3 className="card-title text-center mb-4">🔐 Login</h3>
          
          {error && (
            <div className="alert alert-danger" role="alert">
              <strong>Erro:</strong> {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            
            <div className="mb-3">
              <label className="form-label">Senha</label>
              <input
                type="password"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            
            <button 
              type="submit" 
              className="btn btn-primary w-100 mb-2"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2"></span>
                  Entrando...
                </>
              ) : 'Entrar'}
            </button>
            
            <button 
              type="button"
              className="btn btn-outline-info w-100 mb-3"
              onClick={handleTestDirect}
            >
              Testar Conexão API
            </button>
          </form>
          
          <div className="mt-4">
            <div className="alert alert-info small">
              <strong>Credenciais de teste:</strong><br/>
              Email: frontend@teste.com<br/>
              Senha: Frontend123
            </div>
            
            <div className="text-center">
              <button 
                className="btn btn-sm btn-outline-warning"
                onClick={() => {
                  localStorage.clear();
                  console.log('🧹 LocalStorage limpo');
                  alert('Cache limpo. Recarregue a página.');
                }}
              >
                Limpar Cache Local
              </button>
              
              <a 
                href="http://localhost:8000/docs" 
                target="_blank" 
                rel="noreferrer"
                className="btn btn-sm btn-outline-secondary ms-2"
              >
                Ver API Docs
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Função auxiliar para testar no console
async function testLoginAPI() {
  const formData = new URLSearchParams();
  formData.append('username', 'frontend@teste.com');
  formData.append('password', 'Frontend123');
  
  try {
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString(),
    });
    
    const data = await response.json();
    console.log('🔍 Teste API - Status:', response.status);
    console.log('🔍 Teste API - Data:', data);
    
    if (response.ok) {
      console.log('✅ API funciona! Token:', data.access_token.substring(0, 30) + '...');
    }
  } catch (err) {
    console.error('❌ Teste API falhou:', err);
  }
}

export default Login;
