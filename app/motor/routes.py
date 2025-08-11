from flask import Blueprint, render_template, request, jsonify

motor_bp = Blueprint('motor', __name__,url_prefix='/motor')

@motor_bp.route('/input_control',methods=['POST'])
def input_control():
    data = request.get_json()
    action = data.get('action')
    print(f"Received action: {action}")

    return jsonify({'status': 'ok', 'action':action})