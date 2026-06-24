import { Card, Button, Form, Input, Typography, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const { Title, Text } = Typography;

export default function LoginPage() {
  const { login, isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => { if (isAuthenticated) navigate('/'); }, [isAuthenticated, navigate]);

  const onFinish = async (values: { username: string; password: string }) => {
    setSubmitting(true);
    try {
      await login(values.username, values.password);
    } catch (e: any) {
      message.error(e.message || '登录失败');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return null;

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <Card style={{ width: 400, borderRadius: 12, boxShadow: '0 8px 32px rgba(0,0,0,0.2)' }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <Title level={3} style={{ marginBottom: 4 }}>学程智枢</Title>
          <Text type="secondary">数据驱动的教学过程智能诊断平台</Text>
        </div>

        <Form onFinish={onFinish} size="large">
          <Form.Item name="username" rules={[{ required: true, message: '请输入用户名' }]}>
            <Input prefix={<UserOutlined />} placeholder="用户名" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={submitting}>登录</Button>
          </Form.Item>
        </Form>

        <div style={{ background: '#f6f8fa', borderRadius: 8, padding: 12, fontSize: 12, color: '#666' }}>
          <Text strong style={{ fontSize: 12 }}>演示账号</Text>
          <div style={{ marginTop: 4 }}>教师：zhang / 123456（数据结构+软件工程）</div>
          <div>教师：li / 123456（操作系统+数据库原理）</div>
          <div>教师：wang / 123456（计算机网络+人工智能导论）</div>
          <div>管理员：admin / admin（全部数据）</div>
        </div>
      </Card>
    </div>
  );
}
