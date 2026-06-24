import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, ConfigProvider } from 'antd';
import {
  DashboardOutlined, UploadOutlined, RadarChartOutlined, AimOutlined,
  FileTextOutlined, SwapOutlined, RiseOutlined, BarChartOutlined,
  BookOutlined, EditOutlined, ApartmentOutlined,
} from '@ant-design/icons';
import zhCN from 'antd/locale/zh_CN';
import Dashboard from './pages/Dashboard';
import DataImport from './pages/DataImport';
import ClassProfile from './pages/ClassProfile';
import ModeFingerprint from './pages/ModeFingerprint';
import DiagnosisReport from './pages/DiagnosisReport';
import ComparisonAB from './pages/ComparisonAB';
import TeacherTrend from './pages/TeacherTrend';
import CrossClassCompare from './pages/CrossClassCompare';
import ModeLibrary from './pages/ModeLibrary';
import ModeEditor from './pages/ModeEditor';
import KnowledgeMap from './pages/KnowledgeMap';

const { Header, Sider, Content } = Layout;

const menuItems = [
  { key: '/', icon: <DashboardOutlined />, label: '教师工作台' },
  { key: '/import', icon: <UploadOutlined />, label: '数据导入' },
  {
    key: '/compare', icon: <SwapOutlined />, label: '对比分析',
    children: [
      { key: '/compare/ab', label: 'A/B 模式对比' },
      { key: '/compare/trend', label: '效能趋势' },
      { key: '/compare/cross', label: '跨班级对比' },
    ],
  },
  { key: '/profile', icon: <RadarChartOutlined />, label: '学情画像' },
  { key: '/fingerprint', icon: <AimOutlined />, label: '模式指纹' },
  {
    key: '/modes', icon: <BookOutlined />, label: '教学模式库',
    children: [
      { key: '/modes/library', label: '模板浏览' },
      { key: '/modes/editor', label: '创建模式' },
      { key: '/modes/knowledge', label: '知识图谱' },
    ],
  },
  { key: '/diagnosis', icon: <FileTextOutlined />, label: '诊断报告' },
];

function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  const selectedKey = '/' + location.pathname.split('/').filter(Boolean).join('/');
  const openKeys = ['/compare', '/modes'].filter(k => selectedKey.startsWith(k));

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
          theme="dark" mode="inline"
          selectedKeys={[selectedKey]}
          defaultOpenKeys={openKeys}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ marginTop: 8 }}
        />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', alignItems: 'center', borderBottom: '1px solid #f0f0f0', height: 56 }}>
          <span style={{ fontSize: 14, color: '#888' }}>数据驱动的教学过程智能诊断平台</span>
        </Header>
        <Content style={{ margin: 16, padding: 24, background: '#fff', borderRadius: 8, minHeight: 280 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/import" element={<DataImport />} />
            <Route path="/compare/ab" element={<ComparisonAB />} />
            <Route path="/compare/trend" element={<TeacherTrend />} />
            <Route path="/compare/cross" element={<CrossClassCompare />} />
            <Route path="/profile" element={<ClassProfile />} />
            <Route path="/fingerprint" element={<ModeFingerprint />} />
            <Route path="/modes/library" element={<ModeLibrary />} />
            <Route path="/modes/editor" element={<ModeEditor />} />
            <Route path="/modes/knowledge" element={<KnowledgeMap />} />
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
