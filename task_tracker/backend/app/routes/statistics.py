from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.task import Task
from sqlalchemy import func, case
from datetime import datetime, timedelta

bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_overview():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # 总体统计
    total_users = User.query.count()
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    
    # 最近30天的统计
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_tasks = Task.query.filter(Task.created_at >= thirty_days_ago).count()
    recent_completed = Task.query.filter(
        Task.status == 'completed',
        Task.actual_end_date >= thirty_days_ago
    ).count()
    
    # 工时统计
    total_estimated_hours = db.session.query(func.sum(Task.estimated_hours)).scalar() or 0
    total_actual_hours = db.session.query(func.sum(Task.actual_hours)).scalar() or 0
    
    # 任务状态分布
    status_distribution = db.session.query(
        Task.status,
        func.count(Task.id)
    ).group_by(Task.status).all()
    
    # 优先级分布
    priority_distribution = db.session.query(
        Task.priority,
        func.count(Task.id)
    ).group_by(Task.priority).all()
    
    # 工时偏差统计
    tasks_with_deviation = Task.query.filter(
        Task.actual_hours.isnot(None),
        Task.estimated_hours.isnot(None)
    ).all()
    
    deviation_count = sum(1 for task in tasks_with_deviation if task.check_time_deviation())
    
    return jsonify({
        'total_users': total_users,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'recent_30_days': {
            'new_tasks': recent_tasks,
            'completed_tasks': recent_completed,
            'completion_rate': (recent_completed / recent_tasks * 100) if recent_tasks > 0 else 0
        },
        'hours': {
            'total_estimated': total_estimated_hours,
            'total_actual': total_actual_hours,
            'deviation_rate': ((total_actual_hours - total_estimated_hours) / total_estimated_hours * 100) if total_estimated_hours > 0 else 0
        },
        'status_distribution': dict(status_distribution),
        'priority_distribution': dict(priority_distribution),
        'tasks_with_time_deviation': deviation_count
    })

@bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # 获取最近6个月的数据
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    
    # 按月统计任务完成情况
    monthly_stats = db.session.query(
        func.date_trunc('month', Task.created_at).label('month'),
        func.count(Task.id).label('total'),
        func.sum(case([(Task.status == 'completed', 1)], else_=0)).label('completed')
    ).filter(
        Task.created_at >= six_months_ago
    ).group_by(
        func.date_trunc('month', Task.created_at)
    ).order_by(
        func.date_trunc('month', Task.created_at)
    ).all()
    
    # 按月统计工时情况
    monthly_hours = db.session.query(
        func.date_trunc('month', Task.created_at).label('month'),
        func.sum(Task.estimated_hours).label('estimated'),
        func.sum(Task.actual_hours).label('actual')
    ).filter(
        Task.created_at >= six_months_ago,
        Task.actual_hours.isnot(None)
    ).group_by(
        func.date_trunc('month', Task.created_at)
    ).order_by(
        func.date_trunc('month', Task.created_at)
    ).all()
    
    return jsonify({
        'monthly_completion': [{
            'month': stat.month.strftime('%Y-%m'),
            'total': stat.total,
            'completed': stat.completed,
            'completion_rate': (stat.completed / stat.total * 100) if stat.total > 0 else 0
        } for stat in monthly_stats],
        'monthly_hours': [{
            'month': hour.month.strftime('%Y-%m'),
            'estimated': hour.estimated or 0,
            'actual': hour.actual or 0,
            'deviation_rate': ((hour.actual - hour.estimated) / hour.estimated * 100) if hour.estimated and hour.estimated > 0 else 0
        } for hour in monthly_hours]
    }) 