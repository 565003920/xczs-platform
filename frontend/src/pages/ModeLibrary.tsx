import { useState, useEffect } from 'react';
import { Card, Row, Col, Tag, Spin, Empty, Typography, Divider, Select } from 'antd';
import { BookOutlined, StarOutlined, TeamOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { getModeTemplates, recommendModes } from '../api/endpoints';

const { Text, Paragraph, Title } = Typography;

export default function ModeLibrary() {
  const [templates, setTemplates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getModeTemplates().then(d => { setTemplates(Array.isArray(d) ? d : d.value || []); }).finally(() => setLoading(false));
  }, []);

  const categoryColors: Record<string, string> = { builtin: 'blue', custom: 'orange' };

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>教学模式库</h2>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {!loading && templates.length === 0 && <Empty description="暂无教学模式模板" />}

      <Row gutter={[16, 16]}>
        {templates.map((tpl: any) => (
          <Col key={tpl.id} xs={24} sm={12} lg={8}>
            <Card hoverable
              title={<><BookOutlined style={{ marginRight: 8 }} />{tpl.name}</>}
              extra={<Tag color={categoryColors[tpl.category] || 'default'}>{tpl.category === 'builtin' ? '内置' : '自定义'}</Tag>}
              style={{ height: '100%' }}
            >
              <Paragraph ellipsis={{ rows: 2 }} type="secondary" style={{ minHeight: 44 }}>{tpl.description}</Paragraph>
              <Divider style={{ margin: '12px 0' }} />
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 8 }}>
                {(tpl.stages || []).slice(0, 5).map((s: any, i: number) => (
                  <Tag key={i} style={{ fontSize: 11 }}>{s.name}</Tag>
                ))}
              </div>
              {(tpl.suitable_scenarios) && (
                <Text type="secondary" style={{ fontSize: 12 }}>🎯 {tpl.suitable_scenarios}</Text>
              )}
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
        ))}
      </Row>
    </div>
  );
}
