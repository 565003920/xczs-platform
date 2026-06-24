import { useState, useEffect } from 'react';
import { Card, Row, Col, Select, List, Tag, Spin, Empty, Typography } from 'antd';
import { BulbOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { getClasses, getCourses, getModeFingerprint } from '../api/endpoints';
import type { ClassModel, Course, ModeFingerprint as FingerprintType } from '../types';

const { Title, Paragraph, Text } = Typography;

export default function ModeFingerprint() {
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedId, setSelectedId] = useState<number | undefined>();
  const [fingerprint, setFingerprint] = useState<FingerprintType | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { Promise.all([getClasses(), getCourses()]).then(([cl, co]) => { setClasses(cl); setCourses(co); }); }, []);

  useEffect(() => {
    if (!selectedId) return;
    setLoading(true);
    getModeFingerprint(selectedId).then(setFingerprint).finally(() => setLoading(false));
  }, [selectedId]);

  const radarOption = fingerprint ? {
    tooltip: {},
    radar: {
      center: ['50%', '55%'],
      radius: '65%',
      indicator: [
        { name: '讲授导向', max: 1 },
        { name: '互动导向', max: 1 },
        { name: '实践导向', max: 1 },
        { name: '提问层次', max: 1 },
        { name: '学生中心度', max: 1 },
      ],
    },
    series: [{
      type: 'radar',
      data: [{
        value: [
          fingerprint.fingerprint.lecture_oriented,
          fingerprint.fingerprint.interactive,
          fingerprint.fingerprint.practice_oriented,
          fingerprint.fingerprint.question_level,
          fingerprint.fingerprint.student_centeredness,
        ],
        name: '模式指纹',
        areaStyle: { color: 'rgba(114,46,209,0.2)' },
        lineStyle: { color: '#722ED1', width: 2 },
        itemStyle: { color: '#722ED1' },
      }],
    }],
  } : {};

  const modeColors: Record<string, string> = {
    '讲授主导型': 'blue',
    '互动讨论型': 'green',
    '实践驱动型': 'orange',
    '混合型(讲授+互动)': 'purple',
  };

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>教学模式指纹</h2>

      <div style={{ marginBottom: 20 }}>
        <Select
          showSearch
          placeholder="选择班级"
          style={{ width: 320 }}
          value={selectedId}
          onChange={(v) => setSelectedId(v)}
          filterOption={(input, option) => (option?.label as string || '').includes(input)}
          const courseMap = Object.fromEntries(courses.map(c => [c.id, c.name]));
          options={classes.map((c) => ({ label: `${courseMap[c.course_id] || '?'} — ${c.name}`, value: c.id }))}
        />
      </div>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {!loading && !fingerprint && <Empty description="请先选择班级" />}

      {fingerprint && (
        <Row gutter={16}>
          <Col span={14}>
            <Card title="五维教学模式雷达图">
              <ReactECharts option={radarOption} style={{ height: 400 }} />
            </Card>
          </Col>
          <Col span={10}>
            <Card>
              <div style={{ textAlign: 'center', marginBottom: 16 }}>
                <Tag color={modeColors[fingerprint.mode_label] || 'default'} style={{ fontSize: 18, padding: '4px 16px' }}>
                  {fingerprint.mode_label}
                </Tag>
              </div>
              <Paragraph style={{ fontSize: 14, lineHeight: 1.8 }}>
                {fingerprint.mode_description}
              </Paragraph>
              <div style={{ marginTop: 16 }}>
                <Text type="secondary">课堂观察记录数：{fingerprint.observation_count} 次</Text>
              </div>
            </Card>

            <Card title="改进建议" style={{ marginTop: 16 }}>
              <List
                dataSource={fingerprint.mode_recommendations}
                renderItem={(item) => (
                  <List.Item>
                    <BulbOutlined style={{ color: '#faad14', marginRight: 8 }} />
                    {item}
                  </List.Item>
                )}
              />
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
}
