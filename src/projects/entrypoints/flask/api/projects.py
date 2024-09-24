from projects.adapters.projects import repository as project_repository
from projects.service_layer.projects import handlers as project_handlers
from projects.entrypoints.flask.api.auth import token_auth
from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask.api.errors import bad_request
from projects.entrypoints.flask import db
from flask import jsonify, request
from projects.entrypoints.flask.schema import UserSchema

# Get all
@bp.route('/projects', methods=['GET'])
@token_auth.login_required
def get_projects():
    """
    ---
    get:
      summary: Retrieve all projects
      description: Get a list of all projects.
      responses:
        200:
          description: Successfully retrieved list of projects.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ProjectSchema'
        401:
          description: Unauthorized access.
    """
    repo = project_repository.SqlAlchemyProjectRepository(db.session)
    projects = project_handlers.get_projects(repo)
    data = [{"id": project.id, "name": project.name, "description": project.description} for project in projects]
    return jsonify(data)

# Getting a specific project by id
@bp.route('/projects/<int:id>', methods=['GET'])
@token_auth.login_required
def get_project(id):
    """
    ---
    get:
      summary: Retrieve a project by ID
      description: Get details of a specific project by its ID.
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the project to retrieve.
      responses:
        200:
          description: Successfully retrieved project details.
          content:
            application/json:
              schema: ProjectSchema
        404:
          description: Project not found.
        401:
          description: Unauthorized access.
    """
    repo = project_repository.SqlAlchemyProjectRepository(db.session)
    project = project_handlers.get_project(id, repo)
    if project:
        return jsonify({"id": project.id, "name": project.name, "description": project.description})
    else:
        return jsonify({"error": "Not Found"}), 404

# Create new
@bp.route('/projects', methods=['POST'])
@token_auth.login_required(role='manager')
def create_project():
    """
    ---
    post:
      summary: Create a new project
      description: Create a new project. Only users with manager role can create projects.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: The name of the new project.
                  example: "New Project"
                description:
                  type: string
                  description: A brief description of the project.
                  example: "This is a new project."
      responses:
        201:
          description: Project successfully created.
          content:
            application/json:
              schema: ProjectSchema
        400:
          description: Bad request, missing required fields.
        401:
          description: Unauthorized access.
    """
    data = request.get_json()
    if 'name' not in data :
        return bad_request('must include name')
    repo = project_repository.SqlAlchemyProjectRepository(db.session)
    project = project_handlers.create_project(data.get('name'), data.get("description"), repo)
    return jsonify({"id": project.id, "name": project.name, "description": project.description}), 201

# Update
@bp.route('/projects/<int:id>', methods=['PUT'])
@token_auth.login_required(role='manager')
def update_project(id):
    """
    ---
    put:
      summary: Update an existing project
      description: Update the details of an existing project by its ID. Only users with manager role can update projects.
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the project to update.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: The updated name of the project.
                description:
                  type: string
                  description: The updated description of the project.
      responses:
        200:
          description: Project successfully updated.
          content:
            application/json:
              schema: ProjectSchema
        400:
          description: Bad request, missing required fields.
        401:
          description: Unauthorized access.
        404:
          description: Project not found.
    """    
    data = request.get_json()
    repo = project_repository.SqlAlchemyProjectRepository(db.session)
    project = project_handlers.update_project(id, data["name"], data.get("description"), repo)
    return jsonify({"id": project.id, "name": project.name, "description": project.description})

# Remove project
@bp.route('/projects/<int:id>', methods=['DELETE'])
@token_auth.login_required(role='manager')
def delete_project(id):
    """
    ---
    delete:
      summary: Delete a project
      description: Delete a specific project by its ID. Only users with manager role can delete projects.
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the project to delete.
      responses:
        204:
          description: Project successfully deleted.
        401:
          description: Unauthorized access.
        404:
          description: Project not found.
    """   
    repo = project_repository.SqlAlchemyProjectRepository(db.session)
    project_handlers.delete_project(id, repo)
    return jsonify({"status": "Project deleted"}), 204

def register_routes_and_specs(app):
    with app.app_context(): 
        app.spec.path(view=get_projects)
        app.spec.path(view=get_project)
        app.spec.path(view=create_project)
        app.spec.path(view=update_project)
        app.spec.path(view=delete_project)