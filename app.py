
from flask import Flask, render_template, request, jsonify
import google.genai as genai

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyBAnW2y7hjfJjzMT75JLdvSoSzriyVZLuU")  

@app.route('/')
def index():
    return render_template('page.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    max_retries = 3
    wait_time = 2

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message
            )
            return jsonify({'reply': response.text})
        except genai.errors.ClientError as e:
            if e.status_code == 503 and attempt < max_retries - 1:
                time.sleep(wait_time)
                wait_time *= 2
            else:
                return jsonify({'reply': f"Error: {str(e)}"}), 503

if __name__ == '__main__':
    app.run(debug=True)
