import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, List, Tag, Progress } from 'antd';
import { useNavigate } from 'react-router-dom';
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

const Dashboard: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/tasks', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: { [key: string]: string } = {
      pending: 'default',
      in_progress: 'processing',
      completed: 'success',
      delayed: 'error'
    };
    return colors[status] || 'default';
  };

  const getPriorityColor = (priority: string) => {
    const colors: { [key: string]: string } = {
      high: 'red',
      medium: 'orange',
      low: 'green'
    };
    return colors[priority] || 'default';
  };

  const urgentTasks = tasks.filter(task => 
    task.status !== 'completed' && 
    moment(task.expected_end_date).isBefore(moment().add(3, 'days'))
  );

  const tasksWithDeviation = tasks.filter(task => 
    task.actual_hours && task.estimated_hours && 
    Math.abs((task.actual_hours - task.estimated_hours) / task.estimated_hours) > 0.2
  );

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总任务数"
              value={tasks.length}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="进行中任务"
              value={tasks.filter(t => t.status === 'in_progress').length}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已完成任务"
              value={tasks.filter(t => t.status === 'completed').length}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="工时偏差任务"
              value={tasksWithDeviation.length}
              loading={loading}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
        <Col span={12}>
          <Card title="紧急任务" loading={loading}>
            <List
              dataSource={urgentTasks}
              renderItem={task => (
                <List.Item
                  actions={[
                    <Tag color={getStatusColor(task.status)}>{task.status}</Tag>,
                    <Tag color={getPriorityColor(task.priority)}>{task.priority}</Tag>
                  ]}
                >
                  <List.Item.Meta
                    title={<a onClick={() => navigate(`/tasks/${task.id}`)}>{task.title}</a>}
                    description={`预计完成时间: ${moment(task.expected_end_date).format('YYYY-MM-DD')}`}
                  />
                  <Progress percent={task.progress} size="small" />
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="工时偏差任务" loading={loading}>
            <List
              dataSource={tasksWithDeviation}
              renderItem={task => (
                <List.Item
                  actions={[
                    <Tag color={getStatusColor(task.status)}>{task.status}</Tag>
                  ]}
                >
                  <List.Item.Meta
                    title={<a onClick={() => navigate(`/tasks/${task.id}`)}>{task.title}</a>}
                    description={`预计工时: ${task.estimated_hours}h, 实际工时: ${task.actual_hours}h`}
                  />
                  <Progress
                    percent={Math.round((task.actual_hours / task.estimated_hours) * 100)}
                    size="small"
                    status={task.actual_hours > task.estimated_hours ? 'exception' : 'normal'}
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 