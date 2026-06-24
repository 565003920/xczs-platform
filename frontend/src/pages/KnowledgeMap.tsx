import { useState, useEffect } from 'react';
import { Card, Select, Spin, Empty, Typography, Table, Tag, Alert } from 'antd';
import { WarningOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { getCourses, getKnowledgeGraph } from '../api/endpoints';
import type { Course } from '../types';

const { Text } = Typography;

export default function KnowledgeMap() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [courseId, setCourseId] = useState<number | undefined>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { getCourses().then(setCourses); }, []);

  useEffect(() => {
    if (!courseId) return;
    setLoading(true);
    getKnowledgeGraph(courseId).then(setData).finally(() => setLoading(false));
  }, [courseId]);

  const graphOption = data?.nodes?.length > 0 ? {
    tooltip: { formatter: (params: any) => {
      if (params.dataType === 'node') return `${params.name}<br/>掌握率: ${(params.value * 100).toFixed(0)}%<br/>难度: ${params.data?.difficulty}`;
      return '';
    }},
    series: [{
      type: 'graph', layout: 'force', roam: true, draggable: true,
      force: { repulsion: 300, edgeLength: [80, 200] },
      data: data.nodes.map((n: any) => ({
        name: n.name, value: n.mastery_rate, symbolSize: Math.max(18, n.mastery_rate * 60),
        difficulty: n.difficulty,
        itemStyle: { color: n.mastery_rate > 0.7 ? '#52c41a' : n.mastery_rate > 0.4 ? '#faad14' : '#ff4d4f' },
        label: { show: true, fontSize: 11 },
      })),
      edges: data.edges.map((e: any) => ({
        source: data.nodes.find((n: any) => n.id === e.source)?.name || '',
        target: data.nodes.find((n: any) => n.id === e.target)?.name || '',
        label: { show: true, formatter: e.relation === 'prerequisite' ? '前置' : e.relation === 'parallel' ? '并列' : '包含' },
      })),
    }],
  } : {};

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>课程知识图谱</h2>
      <div style={{ marginBottom: 20 }}>
        <Select showSearch placeholder="选择课程" style={{ width: 320 }} value={courseId}
          onChange={setCourseId}
          options={courses.map(c => ({ label: c.name, value: c.id }))} />
      </div>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {!loading && !data && <Empty description="请选择课程查看知识图谱" />}

      {data?.nodes?.length > 0 && (
        <>
          {data.bottleneck_nodes?.length > 0 && (
            <Alert type="warning" showIcon icon={<WarningOutlined />}
              message="瓶颈知识点"
              description={data.bottleneck_nodes.map((b: any) => `${b.name}(掌握率 ${(b.mastery_rate * 100).toFixed(0)}%)`).join('、')}
              style={{ marginBottom: 16 }} />
          )}
          <Card title="知识点依赖关系图" style={{ marginBottom: 16 }}>
            <ReactECharts option={graphOption} style={{ height: 480 }} />
          </Card>
          <Card title="知识点掌握率明细" size="small">
            <Table dataSource={data.nodes} rowKey="id" pagination={false} size="small"
              columns={[
                { title: '知识点', dataIndex: 'name', key: 'name' },
                { title: '难度', dataIndex: 'difficulty', key: 'diff', render: (v: number) => '⭐'.repeat(Math.round(v)) },
                { title: '掌握率', dataIndex: 'mastery_rate', key: 'mr', sorter: (a: any, b: any) => a.mastery_rate - b.mastery_rate,
                  render: (v: number) => {
                    const color = v > 0.7 ? 'green' : v > 0.4 ? 'orange' : 'red';
                    return <Tag color={color}>{(v * 100).toFixed(0)}%</Tag>;
                  }},
                { title: '样本数', dataIndex: 'sample_count', key: 'count' },
              ]} />
          </Card>
        </>
      )}

      {data && !data.nodes?.length && <Empty description="该课程暂无知识图谱数据" />}
    </div>
  );
}
