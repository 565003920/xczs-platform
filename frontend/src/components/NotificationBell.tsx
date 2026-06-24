import { useState, useEffect } from 'react';
import { Badge, Popover, List, Button, Typography, Empty, Spin } from 'antd';
import { BellOutlined } from '@ant-design/icons';
import { getNotifications, markNotificationRead, markAllNotificationsRead } from '../api/endpoints';

const { Text } = Typography;

export default function NotificationBell() {
  const [unread, setUnread] = useState(0);
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const fetchNotifications = () => {
    setLoading(true);
    getNotifications(true).then(d => {
      setUnread(d.unread_count || 0);
      setItems(d.items || []);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { fetchNotifications(); const t = setInterval(fetchNotifications, 30000); return () => clearInterval(t); }, []);

  const markRead = (id: number) => {
    markNotificationRead(id).then(fetchNotifications);
  };

  const markAllRead = () => {
    markAllNotificationsRead().then(() => { setUnread(0); setOpen(false); });
  };

  const content = (
    <div style={{ width: 320, maxHeight: 400, overflow: 'auto' }}>
      {loading ? <Spin style={{ display: 'block', padding: 20 }} /> : (
        items.length === 0 ? <Empty description="暂无通知" /> : (
          <List dataSource={items.slice(0, 10)} renderItem={(item: any) => (
            <List.Item onClick={() => markRead(item.id)} style={{ cursor: 'pointer', background: item.is_read ? 'transparent' : '#e6f4ff', padding: '8px 12px' }}>
              <div><Text strong={!item.is_read}>{item.title}</Text>
                <div><Text type="secondary" style={{ fontSize: 12 }}>{item.content}</Text></div>
              </div>
            </List.Item>
          )} footer={unread > 0 ? <Button type="link" block onClick={markAllRead}>全部已读</Button> : null} />
        )
      )}
    </div>
  );

  return (
    <Popover content={content} trigger="click" open={open} onOpenChange={setOpen} placement="bottomRight">
      <Badge count={unread} size="small"><BellOutlined style={{ fontSize: 18, cursor: 'pointer', color: '#666' }} /></Badge>
    </Popover>
  );
}
