from projects.adapters.tasks import repository as task_repository
from projects.service_layer.tasks import handlers as task_handlers
from projects.entrypoints.flask.api.auth import token_auth
from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask import db
from flask import jsonify, request

# Get all tasks for a specific project
@bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks(project_id):
    repo = task_repository.SqlAlchemyTaskRepository(db.session)
    tasks = task_handlers.get_tasks_for_project(project_id, repo)
    data = [{"id": task.id, "name": task.name, "status": task.status} for task in tasks]
    if not len(data):
        return  jsonify({"error": "Not Found"}), 404
    return jsonify(data), 200

# Adding a new task to a project
@bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@token_auth.login_required(role='manager')
def create_task(project_id):
    data = request.get_json()
    repo = task_repository.SqlAlchemyTaskRepository(db.session)
    task = task_handlers.create_task(project_id, data.get("name"),  data.get("status"), repo)
    return jsonify({"id": task.id, "name": task.name, "status": task.status}), 201

# Changing task status
@bp.route('/projects/<int:project_id>/tasks/<int:task_id>', methods=['PUT'])
@token_auth.login_required(role='manager')
def update_task_status(project_id, task_id):
    data = request.get_json()
    repo = task_repository.SqlAlchemyTaskRepository(db.session)
    task = task_handlers.update_task_status(project_id, task_id, data["status"], repo)
    return jsonify({"id": task.id, "name": task.name, "status": task.status})