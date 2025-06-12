import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Tag, Modal, Form, Input, DatePicker, InputNumber, Select, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
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
  expected_end_date: string;
  actual_hours: number;
  estimated_hours: number;
  assignee_id: number;
}

interface User {
  id: number;
  username: string;
}

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const { token } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
    fetchUsers();
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

  const handleCreateTask = async (values: any) => {
    try {
      await axios.post(
        'http://localhost:5000/api/tasks',
        {
          ...values,
          expected_end_date: values.expected_end_date.format('YYYY-MM-DD')
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      message.success('任务创建成功');
      setModalVisible(false);
      form.resetFields();
      fetchTasks();
    } catch (error) {
      console.error('Error creating task:', error);
      message.error('任务创建失败');
    }
  };

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: (text: string, record: Task) => (
        <a onClick={() => navigate(`/tasks/${record.id}`)}>{text}</a>
      )
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
      render: (progress: number) => `${progress}%`
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

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setModalVisible(true)}
        >
          新建任务
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={tasks}
        loading={loading}
        rowKey="id"
      />

      <Modal
        title="新建任务"
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          onFinish={handleCreateTask}
          layout="vertical"
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
            name="expected_end_date"
            label="预计完成时间"
            rules={[{ required: true, message: '请选择预计完成时间' }]}
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

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                创建
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default TaskList; 