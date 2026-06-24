import { Card, Button, Radio, Space, Typography, Input } from 'antd';
import { UserOutlined, SafetyCertificateOutlined } from '@ant-design/icons';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, type Role } from '../contexts/AuthContext';

const { Title, Text } = Typography;

export default function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [role, setRole] = useState<Role>('teacher');
  const [name, setName] = useState('');

  useEffect(() => { if (isAuthenticated) navigate('/'); }, [isAuthenticated, navigate]);

  const handleLogin = () => { login(role, name || undefined); };

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    }}>
      <Card style={{ width: 400, borderRadius: 12, boxShadow: '0 8px 32px rgba(0,0,0,0.2)' }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <Title level={3} style={{ marginBottom: 4 }}>学程智枢</Title>
          <Text type="secondary">数据驱动的教学过程智能诊断平台</Text>
        </div>

        <div style={{ marginBottom: 24 }}>
          <Text strong style={{ display: 'block', marginBottom: 12 }}>选择身份</Text>
          <Radio.Group value={role} onChange={e => setRole(e.target.value)} style={{ width: '100%' }}>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Card
                hoverable
                size="small"
                style={{ border: role === 'teacher' ? '2px solid #1677FF' : '2px solid transparent', background: role === 'teacher' ? '#e6f4ff' : '#fafafa' }}
                onClick={() => setRole('teacher')}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <UserOutlined style={{ fontSize: 28, color: '#1677FF' }} />
                  <div>
                    <Text strong>教师</Text>
                    <div><Text type="secondary" style={{ fontSize: 12 }}>查看学情画像、使用教学工具</Text></div>
                  </div>
                </div>
              </Card>
              <Card
                hoverable
                size="small"
                style={{ border: role === 'admin' ? '2px solid #722ED1' : '2px solid transparent', background: role === 'admin' ? '#f9f0ff' : '#fafafa' }}
                onClick={() => setRole('admin')}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <SafetyCertificateOutlined style={{ fontSize: 28, color: '#722ED1' }} />
                  <div>
                    <Text strong>管理员</Text>
                    <div><Text type="secondary" style={{ fontSize: 12 }}>管理数据资产、审计日志、全部功能</Text></div>
                  </div>
                </div>
              </Card>
            </Space>
          </Radio.Group>
        </div>

        {role === 'teacher' && (
          <div style={{ marginBottom: 16 }}>
            <Input placeholder="教师姓名（可留空）" value={name} onChange={e => setName(e.target.value)} />
          </div>
        )}

        <Button type="primary" size="large" block onClick={handleLogin}>
          进入平台
        </Button>
      </Card>
    </div>
  );
}
