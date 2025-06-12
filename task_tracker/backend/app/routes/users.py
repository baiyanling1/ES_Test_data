from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.task import Task

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@bp.route('/<int:user_id>/tasks', methods=['GET'])
@jwt_required()
def get_user_tasks(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    tasks = Task.query.filter_by(assignee_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/<int:user_id>/statistics', methods=['GET'])
@jwt_required()
def get_user_statistics(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(assignee_id=user_id).all()
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == 'completed')
    in_progress_tasks = sum(1 for task in tasks if task.status == 'in_progress')
    pending_tasks = sum(1 for task in tasks if task.status == 'pending')
    
    total_estimated_hours = sum(task.estimated_hours or 0 for task in tasks)
    total_actual_hours = sum(task.actual_hours or 0 for task in tasks)
    
    tasks_with_deviation = [task for task in tasks if task.check_time_deviation()]
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'total_estimated_hours': total_estimated_hours,
        'total_actual_hours': total_actual_hours,
        'tasks_with_time_deviation': len(tasks_with_deviation)
    }) 