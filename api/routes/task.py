from google.cloud import datastore
from google.cloud import tasks_v2
import os
from api.models import Task, TaskRun, TaskLog


from flask import Blueprint, request, jsonify
from api.clients import get_datastore_client, get_tasks_client, get_task_queue_info
from datetime import datetime
from .handler import handler_bp

task_bp = Blueprint('task', __name__)
task_bp.register_blueprint(handler_bp, url_prefix='/handler')

# Initialize Datastore client (expects GOOGLE_APPLICATION_CREDENTIALS env var to be set)
datastore_client = get_datastore_client()

@task_bp.route('/register', methods=['POST'])
def register_task():
	data = request.get_json()
	# Required fields
	description = data.get('description')
	task_id = data.get('task_id')
	# Optional fields
	url = data.get('url')
	repo_url = data.get('repo_url')

	if not description or not task_id:
		return jsonify({'error': 'Missing required fields: description and task_id'}), 400

	# Use user-provided task_id as Datastore key name
	task_obj = Task(
		task_id=str(task_id),
		description=description,
		url=url if url else '',
		repo_url=repo_url if repo_url else ''
	)
	task_entity = datastore.Entity(key=datastore_client.key('Task', str(task_id)))
	task_entity.update(task_obj.__dict__)
	datastore_client.put(task_entity)

	# Add task to Google Cloud Task queue
	tasks_client = get_tasks_client()
	project, location, queue = get_task_queue_info()
	parent = tasks_client.queue_path(project, location, queue)

	# Construct the payload for the task
	payload = {
		'task_id': task_obj.task_id,
		'description': task_obj.description,
		'url': task_obj.url,
		'repo_url': task_obj.repo_url,
		'created_at': task_obj.created_at,
		'status': task_obj.status
	}

	# Create the Cloud Task
	task_handler_url = os.getenv('TASK_HANDLER_URL', 'http://localhost:3000/api/task/handler/handle')
	task = {
		'http_request': {
			'http_method': 1,  # tasks_v2.HttpMethod.POST
			'url': task_handler_url,
			'headers': {'Content-Type': 'application/json'},
			'body': str(payload).encode()
		}
	}
	tasks_client.create_task(parent=parent, task=task)

	return jsonify(task_obj.__dict__), 201

@task_bp.route('/<task_id>', methods=['GET'])
def get_task_detail(task_id):
	key = datastore_client.key('Task', str(task_id))
	task_entity = datastore_client.get(key)
	if not task_entity:
		return jsonify({'error': 'Task not found'}), 404

	# Fetch TaskRuns for this task
	# query = datastore_client.query(kind='TaskRun')
	# query.add_filter('task_id', '=', str(task_id))
	# task_runs = list(query.fetch())
	# runs = []
	# for run in task_runs:
	# 	# Fetch TaskLogs for this run
	# 	log_query = datastore_client.query(kind='TaskLog')
	# 	log_query.add_filter('task_run_id', '=', run.key.name)
	# 	logs = list(log_query.fetch())
	# 	log_objs = [
	# 		TaskLog(
	# 			log_id=log.key.name,
	# 			task_run_id=run.key.name,
	# 			step=log.get('step', ''),
	# 			status=log.get('status', ''),
	# 			started=log.get('started', ''),
	# 			finished=log.get('finished', ''),
	# 			output=log.get('output', ''),
	# 			created=log.get('created', '')
	# 		) for log in logs
	# 	]
	# 	run_obj = TaskRun(
	# 		run_id=run.key.name,
	# 		task_id=task_id,
	# 		status=run.get('status', ''),
	# 		started_at=run.get('started_at', ''),
	# 		finished_at=run.get('finished_at', ''),
	# 		logs=log_objs
	# 	)
	# 	runs.append(run_obj)

	task_obj = Task(
		task_id=task_entity['task_id'],
		description=task_entity['description'],
		url=task_entity.get('url', ''),
		repo_url=task_entity.get('repo_url', ''),
		created_at=task_entity['created_at'],
		status=task_entity['status']
	)
	# Serialize dataclasses to dicts for JSON response
	return jsonify({
		**task_obj.__dict__
		# 'runs': [
		# 	{
		# 		**run.__dict__,
		# 		'logs': [log.__dict__ for log in run.logs]
		# 	} for run in runs
		# ]
	})
