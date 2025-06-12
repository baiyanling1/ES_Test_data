import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, Table, DatePicker } from 'antd';
import { Line } from '@ant-design/charts';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import moment from 'moment';

const { RangePicker } = DatePicker;

interface OverviewData {
  total_users: number;
  total_tasks: number;
  completed_tasks: number;
  completion_rate: number;
  recent_30_days: {
    new_tasks: number;
    completed_tasks: number;
    completion_rate: number;
  };
  hours: {
    total_estimated: number;
    total_actual: number;
    deviation_rate: number;
  };
  status_distribution: { [key: string]: number };
  priority_distribution: { [key: string]: number };
  tasks_with_time_deviation: number;
}

interface TrendData {
  monthly_completion: {
    month: string;
    total: number;
    completed: number;
    completion_rate: number;
  }[];
  monthly_hours: {
    month: string;
    estimated: number;
    actual: number;
    deviation_rate: number;
  }[];
}

const Statistics: React.FC = () => {
  const [overview, setOverview] = useState<OverviewData | null>(null);
  const [trends, setTrends] = useState<TrendData | null>(null);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [overviewResponse, trendsResponse] = await Promise.all([
        axios.get('http://localhost:5000/api/statistics/overview', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://localhost:5000/api/statistics/trends', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      setOverview(overviewResponse.data);
      setTrends(trendsResponse.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    } finally {
      setLoading(false);
    }
  };

  const completionConfig = {
    data: trends?.monthly_completion || [],
    xField: 'month',
    yField: 'completion_rate',
    point: {
      size: 5,
      shape: 'diamond',
    },
    label: {
      style: {
        fill: '#aaa',
      },
    },
  };

  const hoursConfig = {
    data: trends?.monthly_hours || [],
    xField: 'month',
    yField: 'value',
    seriesField: 'type',
    point: {
      size: 5,
      shape: 'diamond',
    },
    label: {
      style: {
        fill: '#aaa',
      },
    },
  };

  if (!overview || !trends) {
    return null;
  }

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总用户数"
              value={overview.total_users}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总任务数"
              value={overview.total_tasks}
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="任务完成率"
              value={overview.completion_rate}
              precision={2}
              suffix="%"
              loading={loading}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="工时偏差任务数"
              value={overview.tasks_with_time_deviation}
              loading={loading}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
        <Col span={12}>
          <Card title="任务完成趋势">
            <Line {...completionConfig} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="工时趋势">
            <Line {...hoursConfig} />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
        <Col span={12}>
          <Card title="任务状态分布">
            <Table
              dataSource={Object.entries(overview.status_distribution).map(([status, count]) => ({
                key: status,
                status,
                count,
                percentage: ((count / overview.total_tasks) * 100).toFixed(2) + '%'
              }))}
              columns={[
                {
                  title: '状态',
                  dataIndex: 'status',
                  key: 'status',
                },
                {
                  title: '数量',
                  dataIndex: 'count',
                  key: 'count',
                },
                {
                  title: '占比',
                  dataIndex: 'percentage',
                  key: 'percentage',
                }
              ]}
              pagination={false}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="任务优先级分布">
            <Table
              dataSource={Object.entries(overview.priority_distribution).map(([priority, count]) => ({
                key: priority,
                priority,
                count,
                percentage: ((count / overview.total_tasks) * 100).toFixed(2) + '%'
              }))}
              columns={[
                {
                  title: '优先级',
                  dataIndex: 'priority',
                  key: 'priority',
                },
                {
                  title: '数量',
                  dataIndex: 'count',
                  key: 'count',
                },
                {
                  title: '占比',
                  dataIndex: 'percentage',
                  key: 'percentage',
                }
              ]}
              pagination={false}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Statistics; 