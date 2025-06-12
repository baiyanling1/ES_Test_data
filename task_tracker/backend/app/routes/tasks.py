from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.task import Task
from app.models.user import User
from datetime import datetime

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        estimated_hours=data.get('estimated_hours'),
        expected_end_date=datetime.fromisoformat(data['expected_end_date']) if 'expected_end_date' in data else None,
        assignee_id=data['assignee_id'],
        creator_id=current_user_id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role == 'admin':
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter(
            (Task.assignee_id == current_user_id) | 
            (Task.creator_id == current_user_id)
        ).all()
    
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    for key, value in data.items():
        if key in ['start_date', 'expected_end_date', 'actual_end_date'] and value:
            value = datetime.fromisoformat(value)
        setattr(task, key, value)
    
    task.last_updated = datetime.utcnow()
    db.session.commit()
    
    return jsonify(task.to_dict())

@bp.route('/<int:task_id>/progress', methods=['PUT'])
@jwt_required()
def update_progress(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    task.progress = data['progress']
    if task.progress == 100:
        task.status = 'completed'
        task.actual_end_date = datetime.utcnow()
    
    task.last_updated = datetime.utcnow()
    db.session.commit()
    
    return jsonify(task.to_dict())

@bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    pending_tasks = Task.query.filter_by(status='pending').count()
    in_progress_tasks = Task.query.filter_by(status='in_progress').count()
    
    # 计算工时偏差
    tasks_with_deviation = Task.query.filter(
        Task.actual_hours.isnot(None),
        Task.estimated_hours.isnot(None)
    ).all()
    
    deviation_count = sum(1 for task in tasks_with_deviation if task.check_time_deviation())
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'tasks_with_time_deviation': deviation_count
    }) 