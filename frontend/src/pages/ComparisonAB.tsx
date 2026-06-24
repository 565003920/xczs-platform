import { useState, useEffect } from 'react';
import { Card, Row, Col, Select, Statistic, Table, Spin, Empty, Typography, Tag } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { getClasses, getCourses, getModeComparison } from '../api/endpoints';
import type { ClassModel, Course } from '../types';

const { Text, Title } = Typography;

export default function ComparisonAB() {
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [classA, setClassA] = useState<number | undefined>();
  const [classB, setClassB] = useState<number | undefined>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { Promise.all([getClasses(), getCourses()]).then(([cl, co]) => { setClasses(cl); setCourses(co); }); }, []);

  useEffect(() => {
    if (!classA || !classB || classA === classB) return;
    setLoading(true);
    getModeComparison(classA, classB).then(setData).finally(() => setLoading(false));
  }, [classA, classB]);

  const courseMap = Object.fromEntries(courses.map(c => [c.id, c.name]));
  const clsOpts = classes.map(c => ({ label: `${courseMap[c.course_id] || '?'} — ${c.name}`, value: c.id }));

  const dualRadarOption = data ? {
    tooltip: {},
    legend: { data: [data.class_a?.name, data.class_b?.name] },
    radar: {
      center: ['50%', '55%'], radius: '60%',
      indicator: [
        { name: '互动质量', max: 1 }, { name: '提问深度', max: 1 },
        { name: '参与度', max: 1 }, { name: '讲授导向', max: 1 },
        { name: '实践导向', max: 1 }, { name: '满意度', max: 1 },
      ],
    },
    series: [
      { type: 'radar', name: data.class_a?.name, data: [{ value: [
        data.dimension_comparison?.interaction_quality?.a || 0,
        data.dimension_comparison?.question_depth?.a || 0,
        data.dimension_comparison?.participation?.a || 0,
        data.dimension_comparison?.lecture_ratio?.a || 0,
        data.dimension_comparison?.practice_ratio?.a || 0,
        data.dimension_comparison?.satisfaction?.a || 0,
      ] }], areaStyle: { color: 'rgba(22,119,255,0.2)' }, lineStyle: { color: '#1677FF' }, itemStyle: { color: '#1677FF' } },
      { type: 'radar', name: data.class_b?.name, data: [{ value: [
        data.dimension_comparison?.interaction_quality?.b || 0,
        data.dimension_comparison?.question_depth?.b || 0,
        data.dimension_comparison?.participation?.b || 0,
        data.dimension_comparison?.lecture_ratio?.b || 0,
        data.dimension_comparison?.practice_ratio?.b || 0,
        data.dimension_comparison?.satisfaction?.b || 0,
      ] }], areaStyle: { color: 'rgba(114,46,209,0.2)' }, lineStyle: { color: '#722ED1' }, itemStyle: { color: '#722ED1' } },
    ],
  } : {};

  const d = data?.grade_comparison;
  const diffColor = d?.difference > 0 ? '#52c41a' : '#ff4d4f';

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>A/B 模式对比</h2>
      <Row gutter={16} style={{ marginBottom: 20 }}>
        <Col span={10}>
          <Select showSearch placeholder="选择班级 A" style={{ width: '100%' }} value={classA} onChange={setClassA} options={clsOpts.filter(o => o.value !== classB)} />
        </Col>
        <Col span={4} style={{ textAlign: 'center', lineHeight: '32px', fontWeight: 700 }}>VS</Col>
        <Col span={10}>
          <Select showSearch placeholder="选择班级 B" style={{ width: '100%' }} value={classB} onChange={setClassB} options={clsOpts.filter(o => o.value !== classA)} />
        </Col>
      </Row>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {!loading && !data && <Empty description="请选择两个不同班级进行对比" />}

      {data && (
        <>
          <Row gutter={16} style={{ marginBottom: 16 }}>
            <Col span={6}><Card><Statistic title="A班均分" value={d?.mean_a} suffix="分" /></Card></Col>
            <Col span={6}><Card><Statistic title="B班均分" value={d?.mean_b} suffix="分" /></Card></Col>
            <Col span={6}>
              <Card>
                <Statistic title="成绩差异" value={Math.abs(d?.difference || 0)} precision={1} suffix="分"
                  valueStyle={{ color: diffColor }}
                  prefix={d?.difference > 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />} />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic title="效应量 (Cohen's d)" value={d?.cohens_d} precision={3} />
                <Text type="secondary" style={{ fontSize: 12 }}>{d?.interpretation}</Text>
              </Card>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={14}>
              <Card title="六维对比雷达图">
                <ReactECharts option={dualRadarOption} style={{ height: 380 }} />
              </Card>
            </Col>
            <Col span={10}>
              <Card title="维度逐项对比" size="small">
                <Table dataSource={[
                  { dim: '互动质量', a: data.dimension_comparison?.interaction_quality?.a, b: data.dimension_comparison?.interaction_quality?.b },
                  { dim: '提问深度', a: data.dimension_comparison?.question_depth?.a, b: data.dimension_comparison?.question_depth?.b },
                  { dim: '参与度', a: data.dimension_comparison?.participation?.a, b: data.dimension_comparison?.participation?.b },
                  { dim: '讲授导向', a: data.dimension_comparison?.lecture_ratio?.a, b: data.dimension_comparison?.lecture_ratio?.b },
                  { dim: '实践导向', a: data.dimension_comparison?.practice_ratio?.a, b: data.dimension_comparison?.practice_ratio?.b },
                  { dim: '满意度', a: data.dimension_comparison?.satisfaction?.a, b: data.dimension_comparison?.satisfaction?.b },
                ]} rowKey="dim" pagination={false} size="small"
                  columns={[
                    { title: '维度', dataIndex: 'dim' },
                    { title: 'A班', dataIndex: 'a', render: (v: number) => v?.toFixed(2) },
                    { title: 'B班', dataIndex: 'b', render: (v: number) => v?.toFixed(2) },
                  ]} />
              </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  );
}
