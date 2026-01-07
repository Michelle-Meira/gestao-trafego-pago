import React, { useState, useEffect } from 'react';
import { campaignsAPI } from '../services/api';

const Dashboard = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [stats, setStats] = useState({
    total: 0,
    active: 0,
    paused: 0,
    draft: 0,
    totalSpent: 0,
    totalBudget: 0,
  });

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      console.log('📡 Buscando campanhas...');
      const data = await campaignsAPI.getAll();
      console.log('📦 Dados recebidos:', data);
      
      // GARANTE que é um array
      const campaignsArray = Array.isArray(data) ? data : [];
      
      setCampaigns(campaignsArray);
      
      // Calcula estatísticas
      const total = campaignsArray.length;
      const active = campaignsArray.filter(c => c.status === 'active').length;
      const paused = campaignsArray.filter(c => c.status === 'paused').length;
      const draft = campaignsArray.filter(c => c.status === 'draft').length;
      const totalSpent = campaignsArray.reduce((sum, c) => sum + (c.total_spent || 0), 0);
      const totalBudget = campaignsArray.reduce((sum, c) => sum + (c.budget_amount || 0), 0);
      
      setStats({ total, active, paused, draft, totalSpent, totalBudget });
      setError('');
      
    } catch (error) {
      console.error('❌ Erro buscando campanhas:', error);
      setError('Erro ao carregar campanhas');
      setCampaigns([]); // Garante array vazio
    } finally {
      setLoading(false);
    }
  };

  const handlePopulateSample = async () => {
    try {
      await campaignsAPI.populateSample();
      fetchCampaigns();
      alert('✅ Dados de exemplo carregados!');
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      alert('❌ Erro ao carregar dados de exemplo');
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Carregando...</span>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>📊 Dashboard</h1>
        <div>
          <button className="btn btn-success me-2" onClick={handlePopulateSample}>
            Carregar Dados de Exemplo
          </button>
          <button className="btn btn-outline-primary" onClick={fetchCampaigns}>
            Atualizar
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-warning">
          {error}
        </div>
      )}

      {/* Cards de Estatísticas */}
      <div className="row mb-4">
        <div className="col-md-2 mb-3">
          <div className="card bg-primary text-white">
            <div className="card-body">
              <h6 className="card-title">Total</h6>
              <h3 className="card-text">{stats.total}</h3>
            </div>
          </div>
        </div>
        
        <div className="col-md-2 mb-3">
          <div className="card bg-success text-white">
            <div className="card-body">
              <h6 className="card-title">Ativas</h6>
              <h3 className="card-text">{stats.active}</h3>
            </div>
          </div>
        </div>
        
        <div className="col-md-2 mb-3">
          <div className="card bg-warning text-white">
            <div className="card-body">
              <h6 className="card-title">Pausadas</h6>
              <h3 className="card-text">{stats.paused}</h3>
            </div>
          </div>
        </div>
        
        <div className="col-md-2 mb-3">
          <div className="card bg-secondary text-white">
            <div className="card-body">
              <h6 className="card-title">Rascunho</h6>
              <h3 className="card-text">{stats.draft}</h3>
            </div>
          </div>
        </div>
        
        <div className="col-md-2 mb-3">
          <div className="card bg-info text-white">
            <div className="card-body">
              <h6 className="card-title">Gasto Total</h6>
              <h6 className="card-text">R$ {stats.totalSpent.toFixed(2)}</h6>
            </div>
          </div>
        </div>
        
        <div className="col-md-2 mb-3">
          <div className="card bg-dark text-white">
            <div className="card-body">
              <h6 className="card-title">Orçamento Total</h6>
              <h6 className="card-text">R$ {stats.totalBudget.toFixed(2)}</h6>
            </div>
          </div>
        </div>
      </div>

      {/* Lista de Campanhas */}
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h5 className="mb-0">📋 Campanhas</h5>
          <span className="badge bg-primary">{campaigns.length} campanhas</span>
        </div>
        <div className="card-body">
          {campaigns.length === 0 ? (
            <div className="text-center py-5">
              <p className="text-muted">Nenhuma campanha encontrada.</p>
              <button className="btn btn-primary" onClick={handlePopulateSample}>
                Carregar Dados de Exemplo
              </button>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Plataforma</th>
                    <th>Status</th>
                    <th>Orçamento</th>
                    <th>Gasto</th>
                    <th>Início</th>
                  </tr>
                </thead>
                <tbody>
                  {campaigns.slice(0, 10).map((campaign) => (
                    <tr key={campaign.id}>
                      <td>
                        <strong>{campaign.name}</strong>
                      </td>
                      <td>
                        <span className="badge bg-secondary">
                          {campaign.platform?.replace('_', ' ') || 'N/A'}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${
                          campaign.status === 'active' ? 'bg-success' :
                          campaign.status === 'paused' ? 'bg-warning' :
                          'bg-secondary'
                        }`}>
                          {campaign.status || 'draft'}
                        </span>
                      </td>
                      <td>R$ {(campaign.budget_amount || 0).toFixed(2)}</td>
                      <td>R$ {(campaign.total_spent || 0).toFixed(2)}</td>
                      <td>{campaign.start_date ? new Date(campaign.start_date).toLocaleDateString() : 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
      
      <div className="mt-3 text-end">
        <small className="text-muted">
          Última atualização: {new Date().toLocaleTimeString()}
        </small>
      </div>
    </div>
  );
};

export default Dashboard;
