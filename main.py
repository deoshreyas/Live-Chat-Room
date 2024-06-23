from flask import Flask, render_template, request, session, redirect, url_for 
from flask_socketio import SocketIO, join_room, leave_room, send
import random 
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "ihjagfssguijk"
socketio = SocketIO(app)

rooms = {}

def GenerateCode(length):
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))
        if code not in rooms:
            break
    return code

@app.route("/", methods=["POST", "GET"])
def index():
    session.clear()

    if request.method=="POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
    
        if not name:
            return render_template("index.html", error="Please enter a name!", code=code, name=name)
        if join!=False:
            if not code:
                return render_template("index.html", error="Please enter a code!", code=code, name=name)

        room = code 
        if create!=False:
            room = GenerateCode(5)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("index.html", error="Invalid code!", code=code, name=name)

        session["room"] = room 
        session["name"] = name

        return redirect(url_for("room"))

    return render_template("index.html")

@app.route("/room/")
def room():
    room = session.get("room")
    name = session.get("name")
    if room is None or name is None or room not in rooms:
        return redirect(url_for("index"))
    return render_template("room.html", room=room, messages=rooms[room]["messages"])

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return 
    join_room(room)
    send({"tag": "announcement", "name": name, "message": "has joined!"}, to=room)
    rooms[room]["members"] += 1

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"]<=0:
            del rooms[room]  
    send({"tag": "announcement", "name": name, "message": "has left!"}, to=room)

@socketio.on("message")
def message(data):
    room = session.get("room")
    name = session.get("name")
    if room not in rooms:
        return 
    content = {
        "tag": "message",
        "name": name,
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append({"name": name, "message": data["data"]})

if __name__ == "__main__":
    socketio.run(app, debug=True)