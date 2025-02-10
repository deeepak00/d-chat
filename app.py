from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

# Serve the chat page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('name')
        session['username'] = username  # Store the username in session
        return render_template("chat.html")
    return render_template("index.html")

# Handle incoming messages
@socketio.on("message")
def handle_message(msg):
    username = session.get('username', 'Anonymous')  # Retrieve username from session
    print(f"Received message: {msg}")
    formatted_msg = f"<span class='username'>{username}: </span>{msg}"
    send(formatted_msg, broadcast=True)  # Broadcast message to all clients

# Handle user joining the chat
@socketio.on('connect')
def handle_connect():
    username = session.get('username', 'Anonymous')  # Retrieve username from session
    join_msg = f"<span class='join-message'>{username} has joined the chat!</span>"
    print(join_msg)
    send(join_msg, broadcast=True)  # Broadcast the join message to all clients

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
