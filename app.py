import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sai-95'
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    users[request.sid] = data['username']
    emit('user_joined', {'username': data['username']}, broadcast=True)
    emit('user_list', {'users': list(users.values())}, broadcast=True)

@socketio.on('message')
def on_message(data):
    emit('new_message', {'username': users.get(request.sid), 'message': data['message']}, broadcast=True)

@socketio.on('disconnect')
def on_disconnect():
    users.pop(request.sid, None)
    emit('user_list', {'users': list(users.values())}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)
