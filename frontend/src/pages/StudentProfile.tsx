import { useState, useEffect } from 'react';
import { Card, Select, Spin, Empty, Descriptions, Table, Tag, Typography } from 'antd';
import { getClasses, getStudentProfile } from '../api/endpoints';
import type { ClassModel } from '../types';

const { Text } = Typography;
// Local API call
const getStudentProfileLocal = (id: number) => fetch(`/api/v2/student/${id}/profile`).then(r => r.json());
const getClassStudentsLocal = (id: number) => fetch(`/api/v2/class/${id}/students`).then(r => r.json());

export default function StudentProfile() {
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [classId, setClassId] = useState<number | undefined>();
  const [students, setStudents] = useState<any[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { getClasses().then(setClasses); }, []);

  useEffect(() => {
    if (!classId) return;
    setLoading(true);
    getClassStudentsLocal(classId).then(d => setStudents(Array.isArray(d) ? d : [])).finally(() => setLoading(false));
  }, [classId]);

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>个体学情画像</h2>
      <div style={{ marginBottom: 20 }}>
        <Select showSearch placeholder="选择班级" style={{ width: 320 }} value={classId} onChange={setClassId}
          options={classes.map(c => ({ label: c.name, value: c.id }))} />
      </div>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}

      {!loading && students.length > 0 && (
        <div style={{ display: 'flex', gap: 16 }}>
          <Card title="学生列表" size="small" style={{ width: 250 }}>
            {students.map((s: any) => (
              <div key={s.student_id} onClick={() => setSelectedStudent(s)}
                style={{ padding: '8px 12px', cursor: 'pointer', borderRadius: 6, marginBottom: 4,
                  background: selectedStudent?.student_id === s.student_id ? '#e6f4ff' : 'transparent' }}>
                <Text strong>{s.name}</Text> <Text type="secondary">{s.student_no}</Text>
                <br /><Tag color={s.avg_grade >= 70 ? 'green' : s.avg_grade >= 60 ? 'orange' : 'red'}>{s.avg_grade}分</Tag>
              </div>
            ))}
          </Card>

          <div style={{ flex: 1 }}>
            {selectedStudent ? (
              <>
                <Descriptions bordered size="small" column={2} style={{ marginBottom: 16 }}>
                  <Descriptions.Item label="姓名">{selectedStudent.name}</Descriptions.Item>
                  <Descriptions.Item label="学号">{selectedStudent.student_no}</Descriptions.Item>
                  <Descriptions.Item label="班级">{selectedStudent.class_name}</Descriptions.Item>
                  <Descriptions.Item label="平均分">{selectedStudent.avg_grade} 分</Descriptions.Item>
                  <Descriptions.Item label="投入度">{selectedStudent.engagement_score}/100</Descriptions.Item>
                  <Descriptions.Item label="考试次数">{selectedStudent.total_exams}</Descriptions.Item>
                </Descriptions>
                <Card title="知识点掌握热力图" size="small" style={{ marginBottom: 16 }}>
                  <Table dataSource={selectedStudent.heatmap || []} rowKey="knowledge_point" pagination={false} size="small"
                    columns={[
                      { title: '知识点', dataIndex: 'knowledge_point' },
                      { title: '均分', dataIndex: 'avg_score', sorter: (a: any, b: any) => a.avg_score - b.avg_score },
                      { title: '趋势', dataIndex: 'trend', render: (v: string) => <Tag color={v === '上升' ? 'green' : v === '下降' ? 'red' : 'blue'}>{v}</Tag> },
                    ]} />
                </Card>
                <Row gutter={16}>
                  <Col span={12}>
                    <Card title="薄弱知识点" size="small">
                      {(selectedStudent.weak_points || []).map((w: any) => <Tag color="red" key={w.knowledge_point}>{w.knowledge_point}: {w.avg_score}</Tag>)}
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card title="优势知识点" size="small">
                      {(selectedStudent.strengths || []).map((s: any) => <Tag color="green" key={s.knowledge_point}>{s.knowledge_point}: {s.avg_score}</Tag>)}
                    </Card>
                  </Col>
                </Row>
              </>
            ) : <Empty description="点击左侧学生查看画像" />}
          </div>
        </div>
      )}
      {!loading && classId && students.length === 0 && <Empty description="该班级暂无学生数据" />}
    </div>
  );
}
