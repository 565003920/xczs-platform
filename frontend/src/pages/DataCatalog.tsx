import { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Progress, Spin } from 'antd';
import { DatabaseOutlined, CheckCircleOutlined, WarningOutlined } from '@ant-design/icons';
import { getCatalogSummary, getCatalogQuality } from '../api/endpoints';

export default function DataCatalog() {
  const [summary, setSummary] = useState<any>(null);
  const [quality, setQuality] = useState<any>(null);

  useEffect(() => {
    Promise.all([getCatalogSummary(), getCatalogQuality()])
      .then(([s, q]) => { setSummary(s); setQuality(q); });
  }, []);

  if (!summary) return <Spin size="large" style={{ display: 'block', margin: '80px auto' }} />;

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>数据资产目录</h2>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}><Card><Statistic title="总记录数" value={summary.total_records} prefix={<DatabaseOutlined />} /></Card></Col>
        <Col span={6}><Card><Statistic title="实体类型" value={summary.entity_count} /></Card></Col>
        <Col span={6}><Card><Statistic title="综合质量" value={quality?.overall_quality || 0} suffix="%" prefix={quality?.overall_quality >= 80 ? <CheckCircleOutlined style={{ color: '#52c41a' }} /> : <WarningOutlined style={{ color: '#faad14' }} />} /></Card></Col>
        <Col span={6}><Card><Statistic title="质量问题" value={quality?.issues?.length || 0} prefix={<WarningOutlined style={{ color: '#ff4d4f' }} />} /></Card></Col>
      </Row>

      <Card title="资产明细">
        <Table dataSource={summary.assets} rowKey="type" pagination={false}
          columns={[
            { title: '类型', dataIndex: 'label', key: 'label' },
            { title: '记录数', dataIndex: 'row_count', key: 'count', sorter: (a: any, b: any) => a.row_count - b.row_count },
            { title: '质量评分', dataIndex: 'quality_score', key: 'quality', render: (v: number) => (
              <Progress percent={v} size="small" status={v >= 90 ? 'success' : v >= 70 ? 'normal' : 'exception'} style={{ width: 120 }} />
            )},
            { title: '状态', key: 'status', render: (_: any, r: any) => (
              <Tag color={r.quality_score >= 90 ? 'green' : r.quality_score >= 70 ? 'orange' : 'red'}>
                {r.quality_score >= 90 ? '健康' : r.quality_score >= 70 ? '一般' : '需关注'}
              </Tag>
            )},
          ]} />
      </Card>

      {quality?.issues?.length > 0 && (
        <Card title="数据质量问题" size="small" style={{ marginTop: 16 }}>
          {quality.issues.map((i: any, idx: number) => (
            <div key={idx} style={{ marginBottom: 8 }}><WarningOutlined style={{ color: '#faad14', marginRight: 8 }} />{i.label}: {i.suggestion} (质量: {i.quality}%)</div>
          ))}
        </Card>
      )}
    </div>
  );
}
