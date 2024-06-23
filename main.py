from flask import Flask, render_template, request, session, redirect 
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
    if request.method=="POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
    
    if not name:
        return render_template("index.html", error="Please enter a name!")
    if join:
        if not code:
            return render_template("index.html", error="Please enter a code!")
        return redirect(f"/room/{code}")

    room = code 
    if create!=False:
        room = GenerateCode(5)
        rooms[room] = {"members": 0, "messages": []}
    elif code not in rooms:
        return render_template("index.html", error="Invalid code!")

    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)