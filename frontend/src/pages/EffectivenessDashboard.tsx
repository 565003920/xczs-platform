import { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Progress, Spin } from 'antd';
import { DashboardOutlined, TrophyOutlined, BookOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export default function EffectivenessDashboard() {
  const [data, setData] = useState<any>(null);

  useEffect(() => { fetcher('/api/v2/dashboard/effectiveness').then(setData); }, []);

  if (!data) return <Spin size="large" style={{ display: 'block', margin: '80px auto' }} />;

  const dist = data.grade_distribution || {};
  const barOption = {
    xAxis: { type: 'category', data: Object.keys(dist) },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: Object.values(dist), itemStyle: { borderRadius: [4, 4, 0, 0] } }],
  };

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>效果仪表盘</h2>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={4}><Card><Statistic title="课程" value={data.summary?.total_courses} prefix={<BookOutlined />} /></Card></Col>
        <Col span={4}><Card><Statistic title="班级" value={data.summary?.total_classes} /></Card></Col>
        <Col span={4}><Card><Statistic title="学生" value={data.summary?.total_students} /></Card></Col>
        <Col span={4}><Card><Statistic title="成绩记录" value={data.summary?.total_grades} /></Card></Col>
        <Col span={4}><Card><Statistic title="平均分" value={data.summary?.avg_grade} suffix="分" /></Card></Col>
        <Col span={4}><Card><Statistic title="数据资产" value={data.summary?.data_assets} /></Card></Col>
      </Row>

      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={12}>
          <Card title="成绩分布">
            <ReactECharts option={barOption} style={{ height: 280 }} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="热门教学模式 TOP5">
            <Table dataSource={data.top_modes || []} rowKey="name" pagination={false} size="small"
              columns={[
                { title: '模式', dataIndex: 'name', key: 'name' },
                { title: '使用次数', dataIndex: 'usage', key: 'usage', render: (v: number) => <Progress percent={Math.min(v * 10, 100)} size="small" format={() => v} /> },
              ]} />
          </Card>
        </Col>
      </Row>

      <Card title="数据资产质量总览">
        <Table dataSource={data.data_quality?.details || []} rowKey="type" pagination={false} size="small"
          columns={[
            { title: '资产类型', dataIndex: 'label' },
            { title: '记录数', dataIndex: 'row_count' },
            { title: '质量', dataIndex: 'quality_score', render: (v: number) => <Progress percent={v} size="small" status={v >= 90 ? 'success' : 'normal'} style={{ width: 100 }} /> },
          ]} />
      </Card>
    </div>
  );
}
