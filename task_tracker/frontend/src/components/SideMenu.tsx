import React from 'react';
import { Layout, Menu } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  TaskOutlined,
  UserOutlined,
  BarChartOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';

const { Sider } = Layout;

const SideMenu: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘'
    },
    {
      key: '/tasks',
      icon: <TaskOutlined />,
      label: '任务管理'
    },
    {
      key: '/statistics',
      icon: <BarChartOutlined />,
      label: '统计分析',
      disabled: user?.role !== 'admin'
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: '个人中心'
    }
  ];

  const handleMenuClick = (key: string) => {
    if (key === 'logout') {
      logout();
      navigate('/login');
    } else {
      navigate(key);
    }
  };

  return (
    <Sider
      breakpoint="lg"
      collapsedWidth="0"
      style={{
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0
      }}
    >
      <div style={{ height: '32px', margin: '16px', background: 'rgba(255, 255, 255, 0.2)' }} />
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[location.pathname]}
        items={[
          ...menuItems,
          {
            key: 'logout',
            icon: <LogoutOutlined />,
            label: '退出登录',
            danger: true
          }
        ]}
        onClick={({ key }) => handleMenuClick(key)}
      />
    </Sider>
  );
};

export default SideMenu; 