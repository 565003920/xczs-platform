import { useState, useEffect } from 'react';
import { Card, Select, Table, Spin, Empty, Typography, Tag } from 'antd';
import { TrophyOutlined } from '@ant-design/icons';
import { getCourses, getCrossTeacherComparison } from '../api/endpoints';
import type { Course } from '../types';

const { Text } = Typography;

export default function CrossClassCompare() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [courseId, setCourseId] = useState<number | undefined>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { getCourses().then(setCourses); }, []);

  useEffect(() => {
    if (!courseId) return;
    setLoading(true);
    getCrossTeacherComparison(courseId).then(setData).finally(() => setLoading(false));
  }, [courseId]);

  const columns = [
    { title: '排名', key: 'rank', width: 60, render: (_: any, __: any, i: number) => {
      if (i === 0) return <TrophyOutlined style={{ color: '#faad14', fontSize: 18 }} />;
      if (i === 1) return <Text style={{ color: '#999', fontWeight: 700 }}>🥈</Text>;
      if (i === 2) return <Text style={{ color: '#cd7f32', fontWeight: 700 }}>🥉</Text>;
      return i + 1;
    }},
    { title: '班级', dataIndex: 'class_name', key: 'name' },
    { title: '平均成绩', dataIndex: 'avg_grade', key: 'grade', sorter: (a: any, b: any) => a.avg_grade - b.avg_grade, render: (v: number) => <Text strong>{v} 分</Text> },
    { title: '平均参与度', dataIndex: 'avg_participation', key: 'participation', render: (v: number) => `${v}/5` },
    { title: '满意度', dataIndex: 'satisfaction', key: 'sat', render: (v: number) => {
      const color = v >= 0.85 ? 'green' : v >= 0.7 ? 'blue' : 'orange';
      return <Tag color={color}>{(v * 100).toFixed(0)}%</Tag>;
    }},
  ];

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>跨班级横向对比</h2>
      <div style={{ marginBottom: 20 }}>
        <Select showSearch placeholder="选择课程" style={{ width: 320 }} value={courseId}
          onChange={setCourseId}
          options={courses.map(c => ({ label: c.name, value: c.id }))} />
      </div>
      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}
      {!loading && !data && <Empty description="请选择课程查看同课程下各班级排名" />}
      {data?.rankings?.length > 0 && (
        <Card title={`${data.course_name} — 班级排名`}>
          <Table dataSource={data.rankings} columns={columns} rowKey="class_id" pagination={false} />
        </Card>
      )}
      {data && !data.rankings?.length && <Empty description="该课程暂无班级对比数据" />}
    </div>
  );
}
