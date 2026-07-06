from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head><title>Innovartus SaaS App</title></head>
        <body>
            <h1>🚀 Innovartus Technologies</h1>
            <p>Welcome to our SaaS application!</p>
            <p>Server Time: {}</p>
            <p>✅ Application is live and running!</p>
        </body>
    </html>
    """.format(datetime.datetime.now())

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": str(datetime.datetime.now())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)