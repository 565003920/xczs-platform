import { useState, useEffect } from 'react';
import { Card, Select, Spin, Empty, Tag, List, Typography, Progress, Descriptions } from 'antd';
import { SwapOutlined } from '@ant-design/icons';
import { getClasses } from '../api/endpoints';
import type { ClassModel } from '../types';

const { Text, Title } = Typography;

const getMigration = (classId: number) => fetch(`/api/v2/migration/recommend?target_class_id=${classId}`).then(r => r.json());

export default function ModeMigration() {
  const [classes, setClasses] = useState<ClassModel[]>([]);
  const [classId, setClassId] = useState<number | undefined>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { getClasses().then(setClasses); }, []);

  useEffect(() => {
    if (!classId) return;
    setLoading(true);
    getMigration(classId).then(setData).finally(() => setLoading(false));
  }, [classId]);

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>模式迁移推荐</h2>
      <div style={{ marginBottom: 20 }}>
        <Select showSearch placeholder="选择目标班级" style={{ width: 320 }} value={classId} onChange={setClassId}
          options={classes.map(c => ({ label: c.name, value: c.id }))} />
      </div>

      {loading && <Spin size="large" style={{ display: 'block', margin: '40px auto' }} />}
      {!loading && !data && <Empty description="请选择班级" />}

      {data && (
        <>
          <Card style={{ marginBottom: 16 }}>
            <Descriptions bordered size="small" column={2}>
              <Descriptions.Item label="目标班级">{data.target_class_name}</Descriptions.Item>
              <Descriptions.Item label="当前模式"><Tag color="blue">{data.current_mode}</Tag></Descriptions.Item>
            </Descriptions>
          </Card>

          {data.recommendations?.length > 0 ? (
            <List dataSource={data.recommendations} renderItem={(item: any) => (
              <Card hoverable style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                  <SwapOutlined style={{ fontSize: 24, color: '#722ED1' }} />
                  <div style={{ flex: 1 }}>
                    <Text strong style={{ fontSize: 16 }}>来自 {item.from_class}</Text>
                    <Tag color="purple" style={{ marginLeft: 8 }}>{item.mode}</Tag>
                    <div style={{ marginTop: 4 }}>
                      <Text type="secondary">{item.reason}</Text>
                    </div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <Progress type="circle" percent={Math.round(item.similarity * 100)} size={60} format={p => `${p}%`} />
                    <div style={{ fontSize: 11, color: '#888', marginTop: 4 }}>相似度</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <Title level={4} style={{ margin: 0, color: '#1677FF' }}>{item.avg_grade}</Title>
                    <div style={{ fontSize: 11, color: '#888' }}>平均分</div>
                  </div>
                </div>
              </Card>
            )} />
          ) : <Empty description="未找到可迁移的优质模式" />}
        </>
      )}
    </div>
  );
}
