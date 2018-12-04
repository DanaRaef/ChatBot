

from flask import Flask, render_template
from flask_socketio import SocketIO, send

from myChatbot import myChatbot
myChatbot = myChatbot()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
print('please visit : http://127.0.0.1:5000/')

@app.route( '/' )
def hello():
    return render_template( '/index.html' )

@socketio.on('message')
def handleMessage(msg):
    reply = myChatbot.callmefromsocket(msg)
    # print('Message: ' + reply)
    send(reply, broadcast=True)

if __name__ == '__main__':
	socketio.run(app)