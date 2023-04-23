from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from dataclasses import dataclass, field
from helpers import generateRandomId

@dataclass
class Message:
    author: str
    content: str

@dataclass
class Chat:
    history: list[Message] = field(default_factory=list)

@dataclass
class Room:
    name: str
    host_username: str
    user_names: list[str] = field(default_factory=list)
    chat: Chat = Chat()



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Boze jak ja kocham placki'
socketio = SocketIO(app)


rooms: dict[str, Room] = {}


@app.route("/", methods=["POST", "GET"])
def mainPage():
    session.clear()
    return render_template("home.html")


@app.route("/join/<join_code>", methods=["POST", "GET"])
def joinPage(join_code: str):

    room_exists = join_code in rooms

    if request.method == "POST" and room_exists:

        if (name := request.form.get("name")) is not None \
            and not name in rooms[join_code].user_names:
            # JOIN A ROOM

            session["room_id"] = join_code
            session["username"] = name
            
            return redirect("/room")
        
        else:
            return redirect("/")

    return render_template("join.html", join_code = join_code, room_exists = room_exists)


@app.route("/create_room", methods=["POST", "GET"])
def createRoomPage():

    error = None

    if request.method == "POST":
        
        if (username := request.form.get("name")) is not None \
            and (room_name := request.form.get("room_name")) is not None:

            room_id = generateRandomId()
            rooms[room_id] = Room(room_name, username)

            session["room_id"] = room_id
            session["username"] = username

            print(f"Created room: {room_id}")
            
            return redirect("/room")

        else:
            error = "All form fields are required"

    
    return render_template("create_room.html", error=error)


@app.route("/room")
def roomPage():

    if session.get("username") is None \
        or (room_id := session.get("room_id")) is None \
            or not room_id in rooms:

        session.clear()
        return redirect("/")
    

    return render_template("room.html", room = rooms.get(session["room_id"]), username = session["username"])


@socketio.on("connect")
def onConnect():
    
    room = session.get("room_id")
    username = session.get("username")

    if not room or not username \
        or not room in rooms:
        return 

    join_room(room)
    # send({"name": username, "message": "Joined the room"}, to=room)
    emit("user_joined", {"username": username}, to=room)
    rooms[room].user_names.append(username)
    print(f"User {username} entered the room: {room}")


@socketio.on("disconnect")
def onDisconnect():

    room = session.get("room_id")
    username = session.get("username")

    leave_room(room)

    if room in rooms:
        rooms[room].user_names.remove(username)

        if len(rooms[room].user_names) == 0:
            del rooms[room]

    emit("user_left", {"username": username}, to=room)
    print(f"User: {username} left room: {room}")
    session.clear()


@socketio.on("play_video")
def onPlayVideo(data):

    room = session.get("room_id")
    if not room in rooms:
        return
    
    print(f"User played video")
    emit("play", to=room)


@socketio.on("stop_video")
def onStopVideo(data):

    room = session.get("room_id")
    if not room in rooms:
        return
    
    print(f"User stopped video")
    emit("stop", to=room)


@socketio.on("change_time")
def onChangeTime(data):

    room = session.get("room_id")
    time = data.get("time")

    if not room in rooms \
        or not time:
        return
    
    print(f"User changed video time to: {time}")
    
    emit("time_change", {"time": time}, to=room)



if __name__ == '__main__':
    socketio.run(app)