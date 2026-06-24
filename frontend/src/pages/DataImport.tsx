import { useState } from 'react';
import { Upload, Card, message, Tabs, Typography, Space, Button } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import {
  importCourses, importClasses, importStudents,
  importGrades, importObservations, importEvaluations,
} from '../api/endpoints';

const { Dragger } = Upload;
const { Text, Paragraph } = Typography;

interface ImportItem {
  key: string;
  label: string;
  desc: string;
  importFn: (file: File) => Promise<{ imported: number; errors: string[] }>;
}

const items: ImportItem[] = [
  { key: 'courses', label: '课程数据', desc: 'CSV列：name, code, department, credits, teacher_name, semester', importFn: importCourses },
  { key: 'classes', label: '班级数据', desc: 'CSV列：name, course_id, semester, student_count', importFn: importClasses },
  { key: 'students', label: '学生数据', desc: 'CSV列：name, student_no, class_id', importFn: importStudents },
  { key: 'grades', label: '成绩数据', desc: 'CSV列：student_id, class_id, exam_name, score, knowledge_point, max_score', importFn: importGrades },
  { key: 'observations', label: '课堂观察', desc: 'CSV列：class_id, date, observer, interaction_frequency, question_depth, student_participation, lecture_ratio, discussion_ratio, practice_ratio, teaching_style_label, notes', importFn: importObservations },
  { key: 'evaluations', label: '教学评价', desc: 'CSV列：class_id, semester, dimension, score', importFn: importEvaluations },
];

export default function DataImport() {
  const [uploading, setUploading] = useState<Record<string, boolean>>({});

  const handleUpload = async (item: ImportItem, file: File) => {
    setUploading((p) => ({ ...p, [item.key]: true }));
    try {
      const result = await item.importFn(file);
      if (result.errors.length > 0) {
        message.warning(`导入完成，但存在 ${result.errors.length} 个错误`);
      } else {
        message.success(`成功导入 ${result.imported} 条${item.label}`);
      }
    } catch (e: any) {
      message.error(`导入失败：${e?.message || '未知错误'}`);
    } finally {
      setUploading((p) => ({ ...p, [item.key]: false }));
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>数据导入</h2>
      <Paragraph type="secondary" style={{ marginBottom: 20 }}>
        请按顺序导入数据（课程 → 班级 → 学生 → 成绩/观察/评价）。请确保CSV文件使用UTF-8编码，第一行为列名。
      </Paragraph>

      <Tabs
        tabPosition="left"
        items={items.map((item) => ({
          key: item.key,
          label: item.label,
          children: (
            <Card title={`导入${item.label}`}>
              <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
                {item.desc}
              </Text>
              <Dragger
                accept=".csv"
                maxCount={1}
                showUploadList={false}
                beforeUpload={(file) => {
                  handleUpload(item, file);
                  return false;
                }}
                disabled={uploading[item.key]}
              >
                <p className="ant-upload-drag-icon"><InboxOutlined /></p>
                <p className="ant-upload-text">点击或拖拽CSV文件到此处</p>
                <p className="ant-upload-hint">支持 .csv 格式</p>
              </Dragger>
              {uploading[item.key] && <p style={{ marginTop: 12, color: '#1677FF' }}>导入中...</p>}
            </Card>
          ),
        }))}
      />
    </div>
  );
}
