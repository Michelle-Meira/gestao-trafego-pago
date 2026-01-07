import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Row, Col, Statistic, Table, Tag, Button } from 'antd';
import { DollarOutlined, RocketOutlined, SyncOutlined } from '@ant-design/icons';

const SimpleDashboard = () => {
  const [loading, setLoading] = useState(false);
  const [campaigns, setCampaigns] = useState([]);

  // Buscar campanhas da API
  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/api/ads/meta/campaigns');
      setCampaigns(response.data.campaigns || []);
    } catch (error) {
      console.error('Erro ao carregar campanhas:', error);
    } finally {
      setLoading(false);
    }
  };

  // Colunas da tabela
  const columns = [
    {
      title: 'Campanha',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'ACTIVE' ? 'green' : 'orange'}>
          {status || 'PAUSED'}
        </Tag>
      ),
    },
    {
      title: 'Investimento',
      key: 'spend',
      render: (record) => `R$ ${record.spend?.toFixed(2) || record.daily_budget?.toFixed(2) || '0.00'}`,
    },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h1>🚀 Dashboard de Gestão de Tráfego</h1>
      
      {/* Botão de atualizar */}
      <Button 
        type="primary" 
        icon={<SyncOutlined />} 
        onClick={fetchCampaigns}
        loading={loading}
        style={{ marginBottom: '20px' }}
      >
        Atualizar Dados
      </Button>

      {/* Métricas */}
      <Row gutter={[16, 16]} style={{ marginBottom: '20px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Investido"
              value={1250.75}
              prefix={<DollarOutlined />}
              suffix="R$"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Conversões"
              value={142}
              prefix={<RocketOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="ROAS Médio"
              value={3.2}
              suffix="x"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="CPL Médio"
              value={22.89}
              suffix="R$"
            />
          </Card>
        </Col>
      </Row>

      {/* Tabela de campanhas */}
      <Card title="🎯 Campanhas Ativas">
        <Table 
          columns={columns}
          dataSource={campaigns.map((c, i) => ({ ...c, key: i }))}
          loading={loading}
          pagination={{ pageSize: 5 }}
        />
      </Card>

      {/* Status do sistema */}
      <div style={{ marginTop: '20px', textAlign: 'center', color: '#666' }}>
        <Tag color="green">● Online</Tag>
        <span style={{ marginLeft: '10px' }}>
          Sistema funcionando | Última atualização: {new Date().toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
};

export default SimpleDashboard;
