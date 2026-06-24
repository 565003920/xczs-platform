import { useState, useEffect, useCallback } from 'react';
import { Card, Row, Col, Tag, Spin, Empty, Typography, Divider, Modal, Descriptions, Button, message, Popconfirm, Tabs, Space, Timeline } from 'antd';
import { BookOutlined, StarOutlined, TeamOutlined, EditOutlined, DeleteOutlined, EyeOutlined, PlusOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { getModeTemplates, getCustomModes, deleteCustomMode } from '../api/endpoints';

const { Text, Paragraph, Title } = Typography;

export default function ModeLibrary() {
  const [templates, setTemplates] = useState<any[]>([]);
  const [customModes, setCustomModes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [detailMode, setDetailMode] = useState<any>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('builtin');
  const navigate = useNavigate();

  const fetchData = useCallback(() => {
    setLoading(true);
    Promise.all([
      getModeTemplates().then(d => Array.isArray(d) ? d : d.value || []),
      getCustomModes().then(d => Array.isArray(d) ? d : d.value || []),
    ]).then(([t, c]) => { setTemplates(t); setCustomModes(c); }).finally(() => setLoading(false));
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleDelete = async (id: number) => {
    try {
      await deleteCustomMode(id);
      message.success('已删除');
      fetchData();
    } catch { message.error('删除失败'); }
  };

  const showDetail = (mode: any) => { setDetailMode(mode); setDetailOpen(true); };

  const renderCard = (tpl: any) => (
    <Col key={tpl.id} xs={24} sm={12} lg={8}>
      <Card hoverable
        title={<><BookOutlined style={{ marginRight: 8 }} />{tpl.name}</>}
        extra={tpl.category === 'builtin'
          ? <Tag color="blue">内置</Tag>
          : <Space><Tag color="orange">自定义</Tag></Space>}
        actions={[
          <EyeOutlined key="view" onClick={() => showDetail(tpl)} />,
          ...(tpl.category === 'custom' ? [
            <EditOutlined key="edit" onClick={() => navigate(`/modes/editor?id=${tpl.id}`)} />,
            <Popconfirm key="del" title="确定删除此教学模式？" onConfirm={() => handleDelete(tpl.id)}>
              <DeleteOutlined style={{ color: '#ff4d4f' }} />
            </Popconfirm>,
          ] : []),
        ]}
        style={{ height: '100%' }}
      >
        <Paragraph ellipsis={{ rows: 2 }} type="secondary" style={{ minHeight: 44 }}>{tpl.description}</Paragraph>
        <Divider style={{ margin: '12px 0' }} />
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 8 }}>
          {(tpl.stages || []).slice(0, 5).map((s: any, i: number) => (
            <Tag key={i} style={{ fontSize: 11 }}>{s.name}</Tag>
          ))}
        </div>
        {tpl.suitable_scenarios && <Text type="secondary" style={{ fontSize: 12, display: 'block' }}>🎯 {tpl.suitable_scenarios}</Text>}
        <div style={{ marginTop: 8 }}>
          {tpl.strengths && <Text style={{ fontSize: 12, display: 'block' }}>✅ {tpl.strengths}</Text>}
          {tpl.limitations && <Text type="warning" style={{ fontSize: 12, display: 'block' }}>⚠️ {tpl.limitations}</Text>}
        </div>
        {tpl.usage_count > 0 && (
          <div style={{ marginTop: 8 }}>
            <TeamOutlined /> {tpl.usage_count} 次使用
            {tpl.avg_rating > 0 && <> · <StarOutlined style={{ color: '#faad14' }} /> {tpl.avg_rating.toFixed(1)}</>}
          </div>
        )}
      </Card>
    </Col>
  );

  const allItems = activeTab === 'builtin' ? templates : customModes;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>教学模式库</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/modes/editor')}>创建模式</Button>
      </div>

      <Tabs activeKey={activeTab} onChange={setActiveTab} items={[
        { key: 'builtin', label: `内置模板 (${templates.length})` },
        { key: 'custom', label: `我的模式 (${customModes.length})` },
      ]} />

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {!loading && allItems.length === 0 && (
        <Empty description={activeTab === 'builtin' ? '暂无内置模板' : '暂无自定义模式，点击右上角创建'} />
      )}

      <Row gutter={[16, 16]}>
        {allItems.map(renderCard)}
      </Row>

      {/* Detail Modal */}
      <Modal title={detailMode?.name} open={detailOpen} onCancel={() => setDetailOpen(false)} footer={null} width={700}>
        {detailMode && (
          <>
            <Descriptions column={2} size="small" bordered style={{ marginBottom: 16 }}>
              <Descriptions.Item label="类型">{detailMode.category === 'builtin' ? '内置模板' : '自定义模式'}</Descriptions.Item>
              <Descriptions.Item label="使用次数">{detailMode.usage_count || 0}</Descriptions.Item>
              <Descriptions.Item label="适用场景" span={2}>{detailMode.suitable_scenarios || '—'}</Descriptions.Item>
              <Descriptions.Item label="优势">{detailMode.strengths || '—'}</Descriptions.Item>
              <Descriptions.Item label="局限">{detailMode.limitations || '—'}</Descriptions.Item>
            </Descriptions>
            <Paragraph>{detailMode.description}</Paragraph>
            <Divider orientation="left">教学环节 ({detailMode.stages?.length || 0} 步)</Divider>
            <Timeline items={(detailMode.stages || []).map((s: any) => ({
              color: 'blue',
              children: (
                <div>
                  <Text strong>{s.name}</Text>
                  <Tag style={{ marginLeft: 8 }}>{s.duration}分钟</Tag>
                  <Tag color="purple">{s.activity_type}</Tag>
                  <div style={{ fontSize: 12, color: '#888', marginTop: 4 }}>
                    👨‍🏫 {s.teacher_action || '—'} · 👩‍🎓 {s.student_action || '—'}
                  </div>
                </div>
              ),
            }))} />
          </>
        )}
      </Modal>
    </div>
  );
}
