import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Card, Row, Col, Select, Statistic, Table, Spin, Empty, Typography } from 'antd';
import ReactECharts from 'echarts-for-react';
import { getClasses, getCourses, getClassProfile } from '../api/endpoints';
import type { ClassModel, Course, ClassProfile as ProfileType } from '../types';

const { Text } = Typography;

export default function ClassProfile() {
  const [searchParams] = useSearchParams();
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedId, setSelectedId] = useState<number | undefined>(Number(searchParams.get('class_id')) || undefined);
  const [profile, setProfile] = useState<ProfileType | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Promise.all([getClasses(), getCourses()]).then(([cl, co]) => { setClasses(cl); setCourses(co); });
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    setLoading(true);
    getClassProfile(selectedId)
      .then(setProfile)
      .finally(() => setLoading(false));
  }, [selectedId]);

  const courseMap = Object.fromEntries(courses.map(c => [c.id, c.name]));

  const radarOption = profile ? {
    tooltip: {},
    radar: {
      center: ['50%', '55%'],
      radius: '65%',
      indicator: [
        { name: '知识掌握度', max: 1 },
        { name: '课堂参与度', max: 1 },
        { name: '互动质量', max: 1 },
        { name: '提问深度', max: 1 },
        { name: '实践均衡度', max: 1 },
        { name: '满意度', max: 1 },
      ],
    },
    series: [{
      type: 'radar',
      data: [{
        value: [
          profile.dimensions.knowledge_mastery,
          profile.dimensions.participation,
          profile.dimensions.interaction_quality,
          profile.dimensions.question_depth,
          profile.dimensions.practice_balance,
          profile.dimensions.satisfaction,
        ],
        name: '学情画像',
        areaStyle: { color: 'rgba(22,119,255,0.2)' },
        lineStyle: { color: '#1677FF', width: 2 },
        itemStyle: { color: '#1677FF' },
      }],
    }],
  } : {};

  const barOption = profile ? {
    tooltip: {},
    xAxis: { type: 'category', data: Object.keys(profile.grade_distribution) },
    yAxis: { type: 'value', name: '人数' },
    series: [{
      type: 'bar',
      data: Object.values(profile.grade_distribution),
      itemStyle: {
        color: (params: any) => {
          const colors = ['#52c41a', '#73d13d', '#faad14', '#ff7a45', '#ff4d4f'];
          return colors[params.dataIndex] || '#1677FF';
        },
      },
    }],
  } : {};

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>班级学情画像</h2>

      <div style={{ marginBottom: 20 }}>
        <Select
          showSearch
          placeholder="选择班级"
          style={{ width: 320 }}
          value={selectedId}
          onChange={(v) => setSelectedId(v)}
          filterOption={(input, option) => (option?.label as string || '').includes(input)}
          options={classes.map((c) => ({ label: `${courseMap[c.course_id] || '?'} — ${c.name}`, value: c.id }))}
        />
      </div>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {!loading && !profile && (
        <Empty description="请先选择班级" />
      )}

      {profile && (
        <>
          <Row gutter={16} style={{ marginBottom: 16 }}>
            <Col span={6}><Card><Statistic title="平均成绩" value={profile.avg_grade} suffix="分" precision={1} /></Card></Col>
            <Col span={6}><Card><Statistic title="学生人数" value={profile.student_count} /></Card></Col>
            <Col span={6}><Card><Statistic title="知识掌握度" value={profile.dimensions.knowledge_mastery * 100} suffix="%" precision={0} /></Card></Col>
            <Col span={6}><Card><Statistic title="满意度" value={profile.dimensions.satisfaction * 100} suffix="%" precision={0} /></Card></Col>
          </Row>

          <Row gutter={16} style={{ marginBottom: 16 }}>
            <Col span={14}>
              <Card title="六维学情画像雷达图">
                <ReactECharts option={radarOption} style={{ height: 380 }} />
              </Card>
            </Col>
            <Col span={10}>
              <Card title="成绩分布">
                <ReactECharts option={barOption} style={{ height: 380 }} />
              </Card>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Card title="薄弱知识点">
                <Table
                  dataSource={profile.weak_points}
                  rowKey="knowledge_point"
                  pagination={false}
                  size="small"
                  columns={[
                    { title: '知识点', dataIndex: 'knowledge_point', key: 'kp' },
                    { title: '平均分', dataIndex: 'avg_score', key: 'score', render: (v: number) => <Text type="danger">{v}</Text> },
                  ]}
                />
              </Card>
            </Col>
            <Col span={12}>
              <Card title="优势知识点">
                <Table
                  dataSource={profile.strengths}
                  rowKey="knowledge_point"
                  pagination={false}
                  size="small"
                  columns={[
                    { title: '知识点', dataIndex: 'knowledge_point', key: 'kp' },
                    { title: '平均分', dataIndex: 'avg_score', key: 'score', render: (v: number) => <Text type="success">{v}</Text> },
                  ]}
                />
              </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  );
}
