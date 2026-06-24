import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, ConfigProvider, theme } from 'antd';
import {
  DashboardOutlined,
  UploadOutlined,
  RadarChartOutlined,
  AimOutlined,
  FileTextOutlined,
} from '@ant-design/icons';
import zhCN from 'antd/locale/zh_CN';
import Dashboard from './pages/Dashboard';
import DataImport from './pages/DataImport';
import ClassProfile from './pages/ClassProfile';
import ModeFingerprint from './pages/ModeFingerprint';
import DiagnosisReport from './pages/DiagnosisReport';

const { Header, Sider, Content } = Layout;

const menuItems = [
  { key: '/', icon: <DashboardOutlined />, label: '教师工作台' },
  { key: '/import', icon: <UploadOutlined />, label: '数据导入' },
  { key: '/profile', icon: <RadarChartOutlined />, label: '学情画像' },
  { key: '/fingerprint', icon: <AimOutlined />, label: '模式指纹' },
  { key: '/diagnosis', icon: <FileTextOutlined />, label: '诊断报告' },
];

function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  const selectedKey = '/' + location.pathname.split('/')[1];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={220} style={{ background: '#001529' }}>
        <div style={{
          height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center',
          color: '#fff', fontSize: 18, fontWeight: 700, letterSpacing: 2,
          borderBottom: '1px solid rgba(255,255,255,0.1)',
        }}>
          学程智枢
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedKey]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ marginTop: 8 }}
        />
      </Sider>
      <Layout>
        <Header style={{
          background: '#fff', padding: '0 24px', display: 'flex', alignItems: 'center',
          borderBottom: '1px solid #f0f0f0', height: 56,
        }}>
          <span style={{ fontSize: 14, color: '#888' }}>
            数据驱动的教学过程智能诊断平台
          </span>
        </Header>
        <Content style={{ margin: 16, padding: 24, background: '#fff', borderRadius: 8, minHeight: 280 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/import" element={<DataImport />} />
            <Route path="/profile" element={<ClassProfile />} />
            <Route path="/fingerprint" element={<ModeFingerprint />} />
            <Route path="/diagnosis" element={<DiagnosisReport />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}

export default function App() {
  return (
    <ConfigProvider locale={zhCN} theme={{ token: { colorPrimary: '#1677FF' } }}>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </ConfigProvider>
  );
}
