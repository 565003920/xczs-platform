import { useState, useEffect } from 'react';
import { Card, Row, Col, Select, Table, Descriptions, Tag, Spin, Empty, Typography, Button, Alert } from 'antd';
import { PrinterOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { getClasses, getCourses, getDiagnosis } from '../api/endpoints';
import type { ClassModel, Course, DiagnosisReport as DiagType } from '../types';

const { Text } = Typography;

export default function DiagnosisReport() {
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedId, setSelectedId] = useState<number | undefined>();
  const [report, setReport] = useState<DiagType | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { Promise.all([getClasses(), getCourses()]).then(([cl, co]) => { setClasses(cl); setCourses(co); }); }, []);

  useEffect(() => {
    if (!selectedId) return;
    setLoading(true);
    getDiagnosis(selectedId).then(setReport).finally(() => setLoading(false));
  }, [selectedId]);

  const courseMap = Object.fromEntries(courses.map(c => [c.id, c.name]));

  const profileRadar = report ? {
    tooltip: {},
    radar: {
      center: ['50%', '55%'],
      radius: '60%',
      indicator: [
        { name: '知识掌握度', max: 1 },
        { name: '参与度', max: 1 },
        { name: '互动质量', max: 1 },
        { name: '提问深度', max: 1 },
        { name: '实践均衡', max: 1 },
        { name: '满意度', max: 1 },
      ],
    },
    series: [{
      type: 'radar',
      data: [{
        value: [
          report.profile.dimensions.knowledge_mastery,
          report.profile.dimensions.participation,
          report.profile.dimensions.interaction_quality,
          report.profile.dimensions.question_depth,
          report.profile.dimensions.practice_balance,
          report.profile.dimensions.satisfaction,
        ],
        name: '学情画像',
        areaStyle: { color: 'rgba(22,119,255,0.15)' },
        lineStyle: { color: '#1677FF' },
        itemStyle: { color: '#1677FF' },
      }],
    }],
  } : {};

  const handlePrint = () => window.print();

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>诊断报告</h2>
        <Button icon={<PrinterOutlined />} onClick={handlePrint} disabled={!report}>打印报告</Button>
      </div>

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

      {!loading && !report && <Empty description="请先选择班级" />}

      {report && (
        <>
          <Descriptions bordered column={2} size="small" style={{ marginBottom: 20 }}>
            <Descriptions.Item label="班级">{report.class_name}</Descriptions.Item>
            <Descriptions.Item label="课程">{report.course_name}</Descriptions.Item>
            <Descriptions.Item label="授课教师">{report.teacher_name || '—'}</Descriptions.Item>
            <Descriptions.Item label="平均成绩">{report.profile.avg_grade} 分</Descriptions.Item>
            <Descriptions.Item label="学生人数">{report.profile.student_count}</Descriptions.Item>
            <Descriptions.Item label="教学模式">
              <Tag color="purple">{report.fingerprint.mode_label}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="观察记录数">{report.fingerprint.observation_count} 次</Descriptions.Item>
          </Descriptions>

          <Alert
            type="info"
            message="教学模式适配建议"
            description={report.teaching_mode_suggestion}
            showIcon
            style={{ marginBottom: 20, whiteSpace: 'pre-wrap' }}
          />

          <Row gutter={16} style={{ marginBottom: 16 }}>
            <Col span={12}>
              <Card title="学情画像雷达图" size="small">
                <ReactECharts option={profileRadar} style={{ height: 300 }} />
              </Card>
            </Col>
            <Col span={12}>
              <Card title="教学模式指纹" size="small">
                <Descriptions column={1} size="small">
                  <Descriptions.Item label="讲授导向">{report.fingerprint.fingerprint.lecture_oriented}</Descriptions.Item>
                  <Descriptions.Item label="互动导向">{report.fingerprint.fingerprint.interactive}</Descriptions.Item>
                  <Descriptions.Item label="实践导向">{report.fingerprint.fingerprint.practice_oriented}</Descriptions.Item>
                  <Descriptions.Item label="提问层次">{report.fingerprint.fingerprint.question_level}</Descriptions.Item>
                  <Descriptions.Item label="学生中心度">{report.fingerprint.fingerprint.student_centeredness}</Descriptions.Item>
                </Descriptions>
                <div style={{ marginTop: 12 }}>
                  <Text strong>改进建议：</Text>
                  <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                    {report.fingerprint.mode_recommendations.map((r, i) => (
                      <li key={i} style={{ marginBottom: 4 }}>{r}</li>
                    ))}
                  </ul>
                </div>
              </Card>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Card title="薄弱知识点" size="small">
                <Table
                  dataSource={report.profile.weak_points}
                  rowKey="knowledge_point"
                  pagination={false}
                  size="small"
                  columns={[
                    { title: '知识点', dataIndex: 'knowledge_point' },
                    { title: '平均分', dataIndex: 'avg_score', render: (v: number) => <Text type="danger">{v}</Text> },
                  ]}
                />
              </Card>
            </Col>
            <Col span={12}>
              <Card title="优势知识点" size="small">
                <Table
                  dataSource={report.profile.strengths}
                  rowKey="knowledge_point"
                  pagination={false}
                  size="small"
                  columns={[
                    { title: '知识点', dataIndex: 'knowledge_point' },
                    { title: '平均分', dataIndex: 'avg_score', render: (v: number) => <Text type="success">{v}</Text> },
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
