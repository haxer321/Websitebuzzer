from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Initial state of the buzzer
buzzer_state = False

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Buzzer Control</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <h1>Buzzer Control</h1>
            <button id="toggleBuzzer">Turn Buzzer ON</button>

            <script>
                const toggleBuzzerButton = document.getElementById('toggleBuzzer');

                // Function to update button state based on server response
                async function updateButtonState() {
                    const response = await fetch('/buzzer');
                    if (response.ok) {
                        const data = await response.json();
                        toggleBuzzerButton.innerText = data.buzzer ? 'Turn Buzzer OFF' : 'Turn Buzzer ON';
                    }
                }

                // Event listener for button click
                toggleBuzzerButton.addEventListener('click', async () => {
                    const currentBuzzerState = toggleBuzzerButton.innerText === 'Turn Buzzer ON' ? false : true;
                    const newBuzzerState = !currentBuzzerState;

                    toggleBuzzerButton.innerText = newBuzzerState ? 'Turn Buzzer OFF' : 'Turn Buzzer ON';

                    await updateBuzzerState(newBuzzerState);
                });

                // Function to update the buzzer state
                async function updateBuzzerState(buzzer) {
                    const response = await fetch('/buzzer', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ buzzer: buzzer }),
                    });

                    if (!response.ok) {
                        console.error('Failed to update buzzer state:', response.statusText);
                    }
                }

                // Check the buzzer state every second
                setInterval(updateButtonState, 1000);
            </script>
        </body>
        </html>
    ''')

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
