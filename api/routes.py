from flask import Blueprint, jsonify
from .task import task_bp

api_bp = Blueprint('api', __name__)

@api_bp.route('/hello', methods=['GET'])
def hello():
	return jsonify({'message': 'Hello, World!'})

# Register task blueprint under /api/task
api_bp.register_blueprint(task_bp, url_prefix='/task')
