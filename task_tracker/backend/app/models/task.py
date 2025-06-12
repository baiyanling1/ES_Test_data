from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='pending')
    priority = db.Column(db.String(20), nullable=False, default='medium')
    
    # 时间相关字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime)
    expected_end_date = db.Column(db.DateTime)
    actual_end_date = db.Column(db.DateTime)
    
    # 工时相关字段
    estimated_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float)
    
    # 外键关系
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 进度追踪
    progress = db.Column(db.Integer, default=0)  # 0-100
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'expected_end_date': self.expected_end_date.isoformat() if self.expected_end_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'assignee_id': self.assignee_id,
            'creator_id': self.creator_id,
            'progress': self.progress,
            'last_updated': self.last_updated.isoformat()
        }
        
    def check_time_deviation(self):
        """检查工时偏差"""
        if self.actual_hours and self.estimated_hours:
            deviation = ((self.actual_hours - self.estimated_hours) / self.estimated_hours) * 100
            return abs(deviation) > 20  # 偏差超过20%返回True
        return False 