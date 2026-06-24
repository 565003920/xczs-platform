import { useState, useEffect } from 'react';
import { Card, Select, Spin, Empty, Tag } from 'antd';
import ReactECharts from 'echarts-for-react';
import { getCourses, getTeacherTrend } from '../api/endpoints';
import type { Course } from '../types';

export default function TeacherTrend() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [courseId, setCourseId] = useState<number | undefined>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { getCourses().then(setCourses); }, []);

  useEffect(() => {
    if (!courseId) return;
    setLoading(true);
    getTeacherTrend(courseId).then(setData).finally(() => setLoading(false));
  }, [courseId]);

  const option = data?.semesters?.length > 0 ? {
    tooltip: { trigger: 'axis' },
    legend: { data: ['平均成绩', '满意度', '教学模式'] },
    grid: { left: 60, right: 120, top: 40, bottom: 40 },
    xAxis: { type: 'category', data: data.semesters.map((s: any) => s.class_name) },
    yAxis: [
      { type: 'value', name: '成绩/分', min: 0, max: 100 },
      { type: 'value', name: '满意度', min: 0, max: 1 },
    ],
    series: [
      { name: '平均成绩', type: 'line', data: data.semesters.map((s: any) => s.avg_grade), smooth: true, symbol: 'circle', symbolSize: 10, itemStyle: { color: '#1677FF' }, markPoint: { data: data.semesters.map((s: any, i: number) => ({ name: s.mode_label, coord: [i, s.avg_grade], value: s.mode_label })) } },
      { name: '满意度', type: 'line', yAxisIndex: 1, data: data.semesters.map((s: any) => s.satisfaction), smooth: true, symbol: 'diamond', symbolSize: 8, itemStyle: { color: '#52c41a' } },
    ],
  } : {};

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>教学效能趋势</h2>
      <div style={{ marginBottom: 20 }}>
        <Select showSearch placeholder="选择课程" style={{ width: 320 }} value={courseId}
          onChange={setCourseId}
          options={courses.map(c => ({ label: c.name, value: c.id }))} />
      </div>
      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}
      {!loading && !data && <Empty description="请选择课程查看趋势" />}
      {data?.semesters?.length > 0 && (
        <>
          <Card title="学期效能趋势" style={{ marginBottom: 16 }}>
            <ReactECharts option={option} style={{ height: 380 }} />
          </Card>
          <Card title="教学模式切换记录" size="small">
            {data.semesters.map((s: any) => (
              <Tag key={s.class_id} style={{ margin: 4 }}>{s.class_name}: {s.mode_label || '未标注'}</Tag>
            ))}
          </Card>
        </>
      )}
      {data && !data.semesters?.length && <Empty description="该课程暂无学期趋势数据" />}
    </div>
  );
}
