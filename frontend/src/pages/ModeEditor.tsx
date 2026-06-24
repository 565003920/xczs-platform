import { useState } from 'react';
import { Card, Form, Input, Button, Select, message, Space, Row, Col, InputNumber } from 'antd';
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons';
import { createCustomMode } from '../api/endpoints';

const { TextArea } = Input;

export default function ModeEditor() {
  const [form] = Form.useForm();
  const [saving, setSaving] = useState(false);

  const onFinish = async (values: any) => {
    setSaving(true);
    try {
      const stages = (values.stages || []).map((s: any, i: number) => ({
        name: s.name || `环节${i + 1}`,
        duration: s.duration || 10,
        activity_type: s.activity_type || '讲授',
        teacher_action: s.teacher_action || '',
        student_action: s.student_action || '',
      }));
      await createCustomMode({ ...values, stages, category: 'custom', created_by: 'teacher' });
      message.success('自定义教学模式创建成功！');
      form.resetFields();
    } catch (e: any) {
      message.error('创建失败：' + (e?.message || '未知错误'));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>创建自定义教学模式</h2>
      <Card style={{ maxWidth: 800 }}>
        <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{ stages: [{ name: '', duration: 10, activity_type: '讲授' }] }}>
          <Form.Item name="name" label="模式名称" rules={[{ required: true, message: '请输入模式名称' }]}>
            <Input placeholder="例：我的混合式教学模式" />
          </Form.Item>
          <Form.Item name="description" label="模式描述">
            <TextArea rows={3} placeholder="描述该教学模式的核心思想和适用场景" />
          </Form.Item>

          <Form.Item label="教学环节">
            <Form.List name="stages">
              {(fields, { add, remove }) => (
                <>
                  {fields.map(({ key, name, ...rest }, index) => (
                    <Card key={key} size="small" style={{ marginBottom: 12, background: '#fafafa' }}
                      title={`环节 ${index + 1}`}
                      extra={fields.length > 1 && <Button type="link" danger icon={<DeleteOutlined />} onClick={() => remove(name)} />}
                    >
                      <Row gutter={12}>
                        <Col span={8}><Form.Item name={[name, 'name']} label="名称" rules={[{ required: true }]}><Input placeholder="导入/讲授/讨论/练习..." /></Form.Item></Col>
                        <Col span={6}><Form.Item name={[name, 'duration']} label="时长(分钟)"><InputNumber min={1} max={120} style={{ width: '100%' }} /></Form.Item></Col>
                        <Col span={10}><Form.Item name={[name, 'activity_type']} label="活动类型"><Select options={[
                          { label: '讲授', value: '讲授' }, { label: '讨论', value: '讨论' }, { label: '练习', value: '练习' },
                          { label: '展示', value: '展示' }, { label: '测评', value: '测评' }, { label: '实践', value: '实践' },
                          { label: '导入', value: '导入' }, { label: '总结', value: '总结' },
                        ]} /></Form.Item></Col>
                      </Row>
                      <Row gutter={12}>
                        <Col span={12}><Form.Item name={[name, 'teacher_action']} label="教师行为"><Input placeholder="教师做什么" /></Form.Item></Col>
                        <Col span={12}><Form.Item name={[name, 'student_action']} label="学生行为"><Input placeholder="学生做什么" /></Form.Item></Col>
                      </Row>
                    </Card>
                  ))}
                  <Button type="dashed" onClick={() => add({ name: '', duration: 10, activity_type: '讲授' })} block icon={<PlusOutlined />}>
                    添加环节
                  </Button>
                </>
              )}
            </Form.List>
          </Form.Item>

          <Form.Item name="suitable_scenarios" label="适用场景">
            <Input placeholder="例：概念性知识较多、学生自主学习能力较强的课程" />
          </Form.Item>
          <Form.Item name="strengths" label="优势"><Input placeholder="该模式的核心优势" /></Form.Item>
          <Form.Item name="limitations" label="局限"><Input placeholder="该模式的局限性" /></Form.Item>

          <Button type="primary" htmlType="submit" loading={saving} block>创建教学模式</Button>
        </Form>
      </Card>
    </div>
  );
}
