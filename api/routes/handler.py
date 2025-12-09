from flask import Blueprint, request, jsonify

handler_bp = Blueprint('handler', __name__)

@handler_bp.route('/handle', methods=['POST'])
def handle_task():
    data = request.get_json()
    # Here you would process the task (e.g., update status, start a run, etc.)
    # For now, just echo the received data
    return jsonify({
        'received': data,
        'message': 'Task handler processed the task.'
    }), 200
