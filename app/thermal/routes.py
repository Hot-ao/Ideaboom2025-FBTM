from flask import Blueprint, jsonify, render_template, request

thermal_bp = Blueprint('thermal',__name__,url_prefix='/thermal')

latest_data = None

@thermal_bp.route('/upload_endpoint', methods=['POST'])
def upload():
    global latest_data
    content = request.get_json()
    latest_data = content['data']
    return jsonify({'status': 'success'})

@thermal_bp.route('/thermal-data')
def thermal_data():
    global latest_data
    if latest_data is None:
        return jsonify({'error': 'No data yet'}), 404
    return jsonify({'data': latest_data})

@thermal_bp.route('/thermal-visual')
def thermal_visual():
    return render_template('thermal.html')