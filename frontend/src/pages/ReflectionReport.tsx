import { useState, useEffect } from 'react';
import { Card, Select, Button, Spin, Empty, Descriptions, Tag, List, Typography, Progress } from 'antd';
import { BulbOutlined, WarningOutlined } from '@ant-design/icons';
import { getClasses, getCourses, generateReflection } from '../api/endpoints';
import type { ClassModel, Course } from '../types';

const { Text, Title } = Typography;

export default function ReflectionReport() {
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [classId, setClassId] = useState<number | undefined>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { Promise.all([getClasses(), getCourses()]).then(([cl, co]) => { setClasses(cl); setCourses(co); }); }, []);

  const generate = async () => {
    if (!classId) return;
    setLoading(true);
    try {
      const res = await generateReflection({ class_id: classId });
      setData(res);
    } finally { setLoading(false); }
  };

  const achieveColor = data?.achievement_estimation?.level === '优秀' ? '#52c41a' :
    data?.achievement_estimation?.level === '良好' ? '#1677FF' : data?.achievement_estimation?.level === '一般' ? '#faad14' : '#ff4d4f';

  const courseMap = Object.fromEntries(courses.map(c => [c.id, c.name]));

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>课后反思助手</h2>
      <Card style={{ marginBottom: 20 }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'flex-end' }}>
          <div><Text>班级</Text><Select showSearch placeholder="选择班级" style={{ width: 220 }} value={classId} onChange={setClassId}
            options={classes.map(c => ({ label: `${courseMap[c.course_id] || '?'} — ${c.name}`, value: c.id }))} /></div>
          <Button type="primary" loading={loading} onClick={generate}>生成反思报告</Button>
        </div>
      </Card>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {data?.note && <Empty description={data.note} />}

      {data && !data.note && (
        <>
          <Descriptions bordered size="small" column={2} style={{ marginBottom: 16 }}>
            <Descriptions.Item label="班级">{data.class_name}</Descriptions.Item>
            <Descriptions.Item label="观察日期">{data.observation_date}</Descriptions.Item>
            <Descriptions.Item label="教学模式"><Tag color="purple">{data.mode_label}</Tag></Descriptions.Item>
            <Descriptions.Item label="达成度">
              <Text style={{ color: achieveColor, fontWeight: 700 }}>{data.achievement_estimation?.level}</Text>
              <Text type="secondary"> ({data.achievement_estimation?.recent_avg_grade}分)</Text>
            </Descriptions.Item>
            <Descriptions.Item label="互动">{data.observation_summary?.interaction}</Descriptions.Item>
            <Descriptions.Item label="参与度">{data.observation_summary?.participation}</Descriptions.Item>
            <Descriptions.Item label="提问深度">{data.observation_summary?.question_depth}</Descriptions.Item>
            <Descriptions.Item label="满意度">{(data.satisfaction * 100).toFixed(0)}%</Descriptions.Item>
          </Descriptions>

          {data.deviations?.length > 0 && (
            <Card title={<><WarningOutlined style={{ color: '#faad14' }} /> 偏差分析</>} size="small" style={{ marginBottom: 16 }}>
              {data.deviations.map((d: any, i: number) => (
                <div key={i} style={{ marginBottom: 8 }}>
                  <Text strong>{d.aspect}</Text>：当前 <Tag>{d.current}</Tag> 建议 <Tag color="blue">{d.ideal}</Tag>
                  <br /><Text type="secondary">{d.suggestion}</Text>
                </div>
              ))}
            </Card>
          )}

          <Card title={<><BulbOutlined style={{ color: '#1677FF' }} /> 改进建议</>} size="small">
            <List dataSource={data.improvement_suggestions || []} renderItem={(item: string) => (
              <List.Item>💡 {item}</List.Item>
            )} />
          </Card>
        </>
      )}
    </div>
  );
}
