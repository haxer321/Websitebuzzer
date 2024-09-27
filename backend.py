from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Initial state of the buzzer
buzzer_state = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buzzer', methods=['GET', 'POST'])
def control_buzzer():
    global buzzer_state
    if request.method == 'POST':
        data = request.get_json()
        if data:
            buzzer_state = data.get('buzzer', buzzer_state)
            return jsonify({'buzzer': buzzer_state}), 200
        return jsonify({'error': 'Invalid JSON data'}), 400
    else:
        return jsonify({'buzzer': buzzer_state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
