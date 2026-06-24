import { useState, useEffect } from 'react';
import { Card, Select, Input, InputNumber, Button, Spin, Empty, Tag, Timeline, Descriptions, Typography, Alert, Row, Col } from 'antd';
import { getClasses } from '../api/endpoints';
import type { ClassModel } from '../types';

const { Text } = Typography;

export default function LessonPlanGenerator() {
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [classId, setClassId] = useState<number | undefined>();
  const [topic, setTopic] = useState('');
  const [duration, setDuration] = useState(50);
  const [plan, setPlan] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { getClasses().then(setClasses); }, []);

  const generate = async () => {
    if (!classId) return;
    setLoading(true);
    try {
      const r = await fetch('/api/v2/lesson-plan/generate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ class_id: classId, lesson_topic: topic, duration }),
      });
      setPlan(await r.json());
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>智能备课助手</h2>
      <Card style={{ marginBottom: 20 }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div><Text>班级</Text><Select showSearch placeholder="选择班级" style={{ width: 220 }} value={classId} onChange={setClassId}
            options={classes.map(c => ({ label: c.name, value: c.id }))} /></div>
          <div><Text>课题</Text><Input placeholder="例：二叉树遍历" style={{ width: 200 }} value={topic} onChange={e => setTopic(e.target.value)} /></div>
          <div><Text>时长(分钟)</Text><InputNumber min={20} max={180} value={duration} onChange={v => setDuration(v || 50)} /></div>
          <Button type="primary" loading={loading} onClick={generate}>生成教案</Button>
        </div>
      </Card>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {plan && (
        <>
          <Descriptions bordered size="small" column={2} style={{ marginBottom: 16 }}>
            <Descriptions.Item label="班级">{plan.class_name}</Descriptions.Item>
            <Descriptions.Item label="课程">{plan.course_name}</Descriptions.Item>
            <Descriptions.Item label="课题">{plan.lesson_topic}</Descriptions.Item>
            <Descriptions.Item label="时长">{plan.duration} 分钟</Descriptions.Item>
            <Descriptions.Item label="班级均分">{plan.profile_summary?.avg_grade} 分</Descriptions.Item>
            <Descriptions.Item label="知识掌握度">{(plan.profile_summary?.knowledge_mastery * 100).toFixed(0)}%</Descriptions.Item>
          </Descriptions>

          {plan.tips?.map((t: string, i: number) => <Alert key={i} message={t} type="info" showIcon style={{ marginBottom: 8 }} />)}

          <Row gutter={16} style={{ marginTop: 16 }}>
            <Col span={12}>
              <Card title="重点讲解" size="small">
                {plan.key_points?.length > 0 ? plan.key_points.map((kp: any) => (
                  <Tag color="red" key={kp.name}>{kp.name} (掌握{(kp.mastery * 100).toFixed(0)}%)</Tag>
                )) : <Text type="secondary">无</Text>}
              </Card>
            </Col>
            <Col span={12}>
              <Card title="可快速通过" size="small">
                {plan.quick_pass?.length > 0 ? plan.quick_pass.map((kp: any) => (
                  <Tag color="green" key={kp.name}>{kp.name} (掌握{(kp.mastery * 100).toFixed(0)}%)</Tag>
                )) : <Text type="secondary">无</Text>}
              </Card>
            </Col>
          </Row>

          <Card title="教学环节" style={{ marginTop: 16 }}>
            <Timeline items={plan.stages?.map((s: any) => ({
              color: 'blue',
              children: <><Text strong>{s.name}</Text> <Tag>{s.duration}分钟</Tag> <Text type="secondary">{s.activity}</Text></>,
            }))} />
          </Card>
        </>
      )}
    </div>
  );
}
