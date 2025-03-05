from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send
import eventlet

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('name')
        session['username'] = username
        return render_template("chat.html")
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg):
    username = session.get('username', 'Anonymous')
    formatted_msg = f"<span class='username'>{username}: </span>{msg}"
    send(formatted_msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    username = session.get('username', 'Anonymous')
    join_msg = f"<span class='join-message'>{username} has joined the chat!</span>"
    send(join_msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000, debug=True)

