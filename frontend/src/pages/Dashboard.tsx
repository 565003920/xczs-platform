import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Statistic, Spin, Empty } from 'antd';
import { BookOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import { getCourses, getClasses } from '../api/endpoints';
import type { Course, ClassModel } from '../types';

export default function Dashboard() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([getCourses(), getClasses()]).then(([c, cl]) => {
      setCourses(c);
      setClasses(cl);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) return <Spin size="large" style={{ display: 'block', margin: '80px auto' }} />;

  const totalStudents = classes.reduce((s, c) => s + c.student_count, 0);

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>教师工作台</h2>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card><Statistic title="课程总数" value={courses.length} prefix={<BookOutlined />} /></Card>
        </Col>
        <Col span={8}>
          <Card><Statistic title="班级总数" value={classes.length} prefix={<TeamOutlined />} /></Card>
        </Col>
        <Col span={8}>
          <Card><Statistic title="学生总数" value={totalStudents} prefix={<UserOutlined />} /></Card>
        </Col>
      </Row>

      <h3 style={{ marginBottom: 16 }}>我的课程</h3>

      {courses.length === 0 ? (
        <Empty description="暂无课程数据，请先导入数据" />
      ) : (
        <Row gutter={[16, 16]}>
          {courses.map((course) => {
            const courseClasses = classes.filter((c) => c.course_id === course.id);
            return (
              <Col key={course.id} xs={24} sm={12} lg={8} xl={6}>
                <Card
                  hoverable
                  title={course.name}
                  onClick={() => {
                    if (courseClasses.length > 0) {
                      navigate(`/profile?class_id=${courseClasses[0].id}`);
                    }
                  }}
                  style={{ cursor: 'pointer' }}
                >
                  <p><strong>代码：</strong>{course.code}</p>
                  <p><strong>院系：</strong>{course.department}</p>
                  <p><strong>教师：</strong>{course.teacher_name}</p>
                  <p><strong>学分：</strong>{course.credits}</p>
                  <p><strong>学期：</strong>{course.semester}</p>
                  <p><strong>班级数：</strong>{courseClasses.length}</p>
                </Card>
              </Col>
            );
          })}
        </Row>
      )}
    </div>
  );
}
