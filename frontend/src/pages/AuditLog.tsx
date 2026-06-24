import { useState, useEffect } from 'react';
import { Card, Table, Tag, Spin, Empty } from 'antd';

export default function AuditLog() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/v2/audit/logs?size=50').then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <Spin size="large" style={{ display: 'block', margin: '80px auto' }} />;

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>操作审计日志</h2>
      {!data?.items?.length ? <Empty description="暂无审计记录" /> : (
        <Table dataSource={data.items} rowKey="id" pagination={{ pageSize: 20 }}
          columns={[
            { title: '时间', dataIndex: 'created_at', key: 'time', render: (v: string) => v?.substring(0, 19), width: 160 },
            { title: '用户', dataIndex: 'user_id', key: 'user', width: 100 },
            { title: '操作', dataIndex: 'action', key: 'action', width: 100, render: (v: string) => <Tag color="blue">{v}</Tag> },
            { title: '对象', key: 'entity', render: (_: any, r: any) => r.entity_type ? `${r.entity_type} #${r.entity_id}` : '—' },
            { title: '详情', dataIndex: 'details', key: 'details' },
          ]} />
      )}
    </div>
  );
}
