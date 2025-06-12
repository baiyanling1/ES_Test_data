import React, { useEffect, useState } from 'react';
import { Card, Descriptions, Table, Tag, Progress, Row, Col, Statistic } from 'antd';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import moment from 'moment';

interface Task {
  id: number;
  title: string;
  status: string;
  priority: string;
  progress: number;
  expected_end_date: string;
  actual_hours: number;
  estimated_hours: number;
}

interface UserStats {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  pending_tasks: number;
  completion_rate: number;
  total_estimated_hours: number;
  total_actual_hours: number;
  tasks_with_time_deviation: number;
}

const UserProfile: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);
  const { user, token } = useAuth();

  useEffect(() => {
    if (user) {
      fetchUserData();
    }
  }, [user]);

  const fetchUserData = async () => {
    try {
      const [tasksResponse, statsResponse] = await Promise.all([
        axios.get(`http://localhost:5000/api/users/${user?.id}/tasks`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`http://localhost:5000/api/users/${user?.id}/statistics`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      setTasks(tasksResponse.data);
      setStats(statsResponse.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const colors: { [key: string]: string } = {
          pending: 'default',
          in_progress: 'processing',
          completed: 'success',
          delayed: 'error'
        };
        return <Tag color={colors[status]}>{status}</Tag>;
      }
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority: string) => {
        const colors: { [key: string]: string } = {
          high: 'red',
          medium: 'orange',
          low: 'green'
        };
        return <Tag color={colors[priority]}>{priority}</Tag>;
      }
    },
    {
      title: '进度',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress: number) => <Progress percent={progress} size="small" />
    },
    {
      title: '预计完成时间',
      dataIndex: 'expected_end_date',
      key: 'expected_end_date',
      render: (date: string) => moment(date).format('YYYY-MM-DD')
    },
    {
      title: '预计工时',
      dataIndex: 'estimated_hours',
      key: 'estimated_hours',
      render: (hours: number) => `${hours}h`
    },
    {
      title: '实际工时',
      dataIndex: 'actual_hours',
      key: 'actual_hours',
      render: (hours: number) => hours ? `${hours}h` : '-'
    }
  ];

  if (!user || !stats) {
    return null;
  }

  return (
    <div>
      <Card title="个人信息" loading={loading}>
        <Descriptions bordered>
          <Descriptions.Item label="用户名">{user.username}</Descriptions.Item>
          <Descriptions.Item label="邮箱">{user.email}</Descriptions.Item>
          <Descriptions.Item label="角色">{user.role}</Descriptions.Item>
        </Descriptions>
      </Card>

      <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总任务数"
              value={stats.total_tasks}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已完成任务"
              value={stats.completed_tasks}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="进行中任务"
              value={stats.in_progress_tasks}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="任务完成率"
              value={stats.completion_rate}
              precision={2}
              suffix="%"
              loading={loading}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="总预计工时"
              value={stats.total_estimated_hours}
              suffix="h"
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="总实际工时"
              value={stats.total_actual_hours}
              suffix="h"
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="工时偏差任务数"
              value={stats.tasks_with_time_deviation}
              loading={loading}
            />
          </Card>
        </Col>
      </Row>

      <Card title="我的任务" style={{ marginTop: '16px' }}>
        <Table
          columns={columns}
          dataSource={tasks}
          loading={loading}
          rowKey="id"
        />
      </Card>
    </div>
  );
};

export default UserProfile; 