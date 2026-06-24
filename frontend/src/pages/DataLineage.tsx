import { useState, useEffect } from 'react';
import { Card, Table, Tag, Empty, Spin, Typography, Timeline } from 'antd';
import ReactECharts from 'echarts-for-react';

const { Text } = Typography;

export default function DataLineage() {
  const [lineages, setLineages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/v2/catalog/lineage').then(r => r.json()).then(d => setLineages(Array.isArray(d) ? d : [])).finally(() => setLoading(false));
  }, []);

  if (loading) return <Spin size="large" style={{ display: 'block', margin: '80px auto' }} />;

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>数据血缘追踪</h2>

      {lineages.length === 0 ? (
        <Empty description="暂无血缘记录。使用智能备课或课后反思功能后将自动生成。" />
      ) : (
        <Table dataSource={lineages} rowKey="analysis_id" pagination={false}
          columns={[
            { title: '分析ID', dataIndex: 'analysis_id', key: 'id' },
            { title: '类型', dataIndex: 'analysis_type', key: 'type', render: (v: string) => <Tag>{v}</Tag> },
            { title: '数据来源', key: 'source', render: (_: any, r: any) => (r.inputs || []).map((i: any) => <Tag key={i.source} color="blue">{i.source}</Tag>) },
            { title: '输出类型', key: 'output', render: (_: any, r: any) => r.output?.type && <Tag color="green">{r.output.type}</Tag> },
            { title: '时间', dataIndex: 'timestamp', key: 'time', render: (v: string) => v?.substring(0, 19) },
          ]} />
      )}
    </div>
  );
}
