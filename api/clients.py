import os
from google.cloud import datastore, tasks_v2

# Datastore client
_datastore_client = None

def get_datastore_client():
    global _datastore_client
    if _datastore_client is None:
        _datastore_client = datastore.Client()
    return _datastore_client

# Cloud Tasks client
_tasks_client = None

def get_tasks_client():
    global _tasks_client
    if _tasks_client is None:
        _tasks_client = tasks_v2.CloudTasksClient()
    return _tasks_client

# Helper to get project/location/queue

def get_task_queue_info():
    project = os.getenv('GOOGLE_CLOUD_PROJECT', 'olance-480609')
    location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    queue = 'olance-task-queue'
    return project, location, queue
