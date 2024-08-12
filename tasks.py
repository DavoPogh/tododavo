from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from flask_login import login_required, current_user
from models import db, Task
from auth import logout_user

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
@login_required
def index():
    # Render a template that shows the tasks
    return render_template('tasks.html')

@tasks_bp.route('/all', methods=['GET'])
@login_required
def all_tasks():
    # Fetch all tasks for the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/', methods=['POST'])
@login_required
def add_task():
    new_task = request.json.get('text')
    if not new_task:
        return jsonify({'error': 'Task content is required'}), 400
    
    task = Task(title=new_task, user_id=current_user.id)
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'status': 'success'}), 201

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({'status': 'success'}), 200

@tasks_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
