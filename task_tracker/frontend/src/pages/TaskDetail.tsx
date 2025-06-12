import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Descriptions, Button, Space, Tag, Progress, Form, Input, InputNumber, DatePicker, Select, message } from 'antd';
import { EditOutlined, SaveOutlined, CloseOutlined } from '@ant-design/icons';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import moment from 'moment';

const { Option } = Select;

interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  progress: number;
  start_date: string;
  expected_end_date: string;
  actual_end_date: string;
  actual_hours: number;
  estimated_hours: number;
  assignee_id: number;
  creator_id: number;
}

interface User {
  id: number;
  username: string;
}

const TaskDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [task, setTask] = useState<Task | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();
  const { token, user: currentUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTask();
    fetchUsers();
  }, [id]);

  const fetchTask = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/tasks/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTask(response.data);
      form.setFieldsValue({
        ...response.data,
        expected_end_date: moment(response.data.expected_end_date),
        start_date: response.data.start_date ? moment(response.data.start_date) : null,
        actual_end_date: response.data.actual_end_date ? moment(response.data.actual_end_date) : null
      });
    } catch (error) {
      console.error('Error fetching task:', error);
      message.error('获取任务详情失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/users', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleUpdateTask = async (values: any) => {
    try {
      await axios.put(
        `http://localhost:5000/api/tasks/${id}`,
        {
          ...values,
          expected_end_date: values.expected_end_date.format('YYYY-MM-DD'),
          start_date: values.start_date?.format('YYYY-MM-DD'),
          actual_end_date: values.actual_end_date?.format('YYYY-MM-DD')
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      message.success('任务更新成功');
      setEditing(false);
      fetchTask();
    } catch (error) {
      console.error('Error updating task:', error);
      message.error('任务更新失败');
    }
  };

  const handleUpdateProgress = async (progress: number) => {
    try {
      await axios.put(
        `http://localhost:5000/api/tasks/${id}/progress`,
        { progress },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      message.success('进度更新成功');
      fetchTask();
    } catch (error) {
      console.error('Error updating progress:', error);
      message.error('进度更新失败');
    }
  };

  if (!task) {
    return null;
  }

  const canEdit = currentUser?.role === 'admin' || currentUser?.id === task.creator_id;

  return (
    <Card
      title={task.title}
      loading={loading}
      extra={
        canEdit && (
          <Space>
            {editing ? (
              <>
                <Button
                  type="primary"
                  icon={<SaveOutlined />}
                  onClick={() => form.submit()}
                >
                  保存
                </Button>
                <Button
                  icon={<CloseOutlined />}
                  onClick={() => {
                    setEditing(false);
                    form.resetFields();
                  }}
                >
                  取消
                </Button>
              </>
            ) : (
              <Button
                icon={<EditOutlined />}
                onClick={() => setEditing(true)}
              >
                编辑
              </Button>
            )}
          </Space>
        )
      }
    >
      {editing ? (
        <Form
          form={form}
          layout="vertical"
          onFinish={handleUpdateTask}
        >
          <Form.Item
            name="title"
            label="标题"
            rules={[{ required: true, message: '请输入任务标题' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea />
          </Form.Item>

          <Form.Item
            name="status"
            label="状态"
            rules={[{ required: true, message: '请选择状态' }]}
          >
            <Select>
              <Option value="pending">待处理</Option>
              <Option value="in_progress">进行中</Option>
              <Option value="completed">已完成</Option>
              <Option value="delayed">已延期</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="priority"
            label="优先级"
            rules={[{ required: true, message: '请选择优先级' }]}
          >
            <Select>
              <Option value="high">高</Option>
              <Option value="medium">中</Option>
              <Option value="low">低</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="estimated_hours"
            label="预计工时"
            rules={[{ required: true, message: '请输入预计工时' }]}
          >
            <InputNumber min={0} step={0.5} />
          </Form.Item>

          <Form.Item
            name="actual_hours"
            label="实际工时"
          >
            <InputNumber min={0} step={0.5} />
          </Form.Item>

          <Form.Item
            name="start_date"
            label="开始时间"
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="expected_end_date"
            label="预计完成时间"
            rules={[{ required: true, message: '请选择预计完成时间' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="actual_end_date"
            label="实际完成时间"
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="assignee_id"
            label="负责人"
            rules={[{ required: true, message: '请选择负责人' }]}
          >
            <Select>
              {users.map(user => (
                <Option key={user.id} value={user.id}>{user.username}</Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      ) : (
        <>
          <Descriptions bordered>
            <Descriptions.Item label="状态">
              <Tag color={
                task.status === 'completed' ? 'success' :
                task.status === 'in_progress' ? 'processing' :
                task.status === 'delayed' ? 'error' : 'default'
              }>
                {task.status}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="优先级">
              <Tag color={
                task.priority === 'high' ? 'red' :
                task.priority === 'medium' ? 'orange' : 'green'
              }>
                {task.priority}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="进度">
              <Progress percent={task.progress} />
            </Descriptions.Item>
            <Descriptions.Item label="预计工时">
              {task.estimated_hours}h
            </Descriptions.Item>
            <Descriptions.Item label="实际工时">
              {task.actual_hours ? `${task.actual_hours}h` : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="开始时间">
              {task.start_date ? moment(task.start_date).format('YYYY-MM-DD') : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="预计完成时间">
              {moment(task.expected_end_date).format('YYYY-MM-DD')}
            </Descriptions.Item>
            <Descriptions.Item label="实际完成时间">
              {task.actual_end_date ? moment(task.actual_end_date).format('YYYY-MM-DD') : '-'}
            </Descriptions.Item>
          </Descriptions>

          <div style={{ marginTop: 16 }}>
            <h4>描述</h4>
            <p>{task.description || '暂无描述'}</p>
          </div>
        </>
      )}
    </Card>
  );
};

export default TaskDetail; 