from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


def index():
    if request.values.get('name', None):
        session['name'] = request.form['name']
        return redirect(url_for('name'))
    return render_template('index.html')


def chat():
    if session.get('name'):
        return render_template('chat.html')
    return redirect(url_for('index'))


def join1(data):
    print('data: ' + str(data))
    room = data['room']
    session['room'] = room
    join_room(data['room'])
    emit('status', {'code': '200', 'msg': 'welcome' + str(session['name']) + 'join room! '
                    }, room=room)


def message(data):
    room = data.get('room')
    msg = data.get('message')
    emit('status', {'code': '200', 'msg': 'msg'}, room=room)


def handle_message(message):
    print('received : ' + message['data'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
