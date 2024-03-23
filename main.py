from flask import Flask,render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random # to generate random ROOM codes 
from string import ascii_uppercase

# name the pthon module 
app = Flask(__name__)
# configure the app with the random any secret-key 
app.config["SECRET_KEY"] = "kbhkljnbpkmn"
socketio = SocketIO(app)

# create a dict for storing a different rooms (check exist or not -- no duplicate)
rooms = {} 

# create a random unique id of 4 
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        # but if already room exists, -- duplicate 
        if code is not rooms:
            break
    
    return code    
                
    
# create a route for home page and render the html 
@app.route("/", methods=["POST", "GET"])
def home():
    # clear the session 
    session.clear()
    # we want name , code and join and create => name attributes from FORM
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        # to avoid error => get() => if not return False set default
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        
        # CHECK THAT USER GIVES ME A NAME 
        if not name:
            return render_template("home.html", error="Please Enter a Name", code=code, name=name)
            
        # CHECK THAT USER joins , but GIVES ME no code for ROOM
        if join != False and not code:
            return render_template("home.html", error="Please Enter a Room Code" ,code=code, name=name)
        
        # now we need to see what room user entered , check it exists , if not generate , is yes then join 
        room = code 
        # if not exist , creating new 
        if create != False:
            # generate a random code with 4 numbers
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
            
        # user is joining the room , but the code does not exist only 
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist ", code=code, name=name)
                
        session["room"] = room  
        session["name"] = name
        
        return redirect(url_for("room"))  
        
    return render_template("home.html")

# create a route for room 
@app.route("/room")
def room():
    room = session.get("room")
    # u need to provide the above code for what it is  , dont just directly goto room.html 
    if room is None or session.get("name") is None or room  not in rooms:
        return redirect(url_for("home"))
    
    # keep history of the messages , so messages=...
    return render_template("room.html", code=room, messages = rooms[room]["messages"])

# listen the message from our-flask-server side => to transmit to everyone 
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    # send the message and also keep track of name 
    content = {
        "name": session.get("name"),
        "message": data["data"]
    } 
    # send it to everyone
    send(content, to=room)
    # we want history of all messages 
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said:{data:['data']}")
    ...
# handle the socket stuff 
@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    
    # we want safety , so no one should by pass the home page and connect 
    if not name or not room:
        return
    
    # if they are in room , but not valid 
    if room not in  rooms:
        leave_room(room)
        return
    
    # but if everything is fine , put the user in the socket-room ,
    # to=room => we are sending the message to room => confirmation 
    join_room(room)
    send({"name":name, "message": "has entered the room"}, to=room)
    # keep track of the members inside the room 
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

# handle the leaving room 
@socketio.on("disconnect")
def disconnnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    
    # if the room user left ,is it in our rooms , if s delete that 
    if room in rooms:
        rooms[room]["members"] -=1
        # if everyone has left that room , no purpose so delete 
        if rooms[room]["members"] <=0:
            del rooms[room]
    
    send({"name":name, "message": "has leaved the room"}, to=room)        
    print(f"{name} has left room {room}")
    

if __name__ == "__main__":
    socketio.run(app, debug=True)