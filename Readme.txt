install -- pip install Flask
install -- pip install flask-socketio

comcepts 
socket-server => runs on flask web server 
different clients - web browsers (like chrome ) ==> connect to our flask server 

clients send the message to flask server ,flask sever =>  looks at what chat room , they are at and then 
transmit them to that chatroom, 

use javaScript for the frontend and listening purpose 

render_template => to rendert the html code 

STEPS 
1. include the required packages 

2. Setting Up the Flask App:

app = Flask(__name__)
app.config["SECRET_KEY"] = "kbhkljnbpkmn"
socketio = SocketIO()

Creates a Flask web application instance.
Configures the application with a secret key. The secret key is used for securely signing session cookies.
Initializes a SocketIO instance. debug= True => to provide info about each part of the error => no need to run the server  again and again 

http://127.0.0.1:5000/ => 5000 is the port number oin which flask runs 

idea => 
1st create a home page , then a room page(joining the chat )

3. creating the routes for the home page using decorator app (use get and post methods )
@app.route("/", methods=["POST", "GET"])
def home():
    render_template(" the html") 

create a templates folder , otherwise it will not work to render html => templates > home.html , base.html 
(base template ) , room.html(for chat purpose)

create a static folder -> then css -> style.css  => here u can put inside the static folder static like 
things like images, icons, css etc  => static assets 

url_for => generate a dynamic url 

4 include the socketIo in => <script> for javascript 
GOOGLE => flask socket io connect  => to connect 

u can use the below code anywhere u want => {% block content %}{% endblock  %} => this is in base.html
{% extends 'base.html'%}  and then 
{% block content %}
 ... write your code here to render here ... 
{% endblock  %}
to use the above code in home.html

frontend part connected using name attribute inside input
value="{{name}}" => for backup if user gives wrong name , we dont want them to loose their actual data , so 
render the name , means reinject the name, so no loss issues   and then submit code 

error :   {% comment %}  => wrong in flask (true in django )  , 
fopr flask => use {# #} => {# .. comment here ..  #} , 

get(, False) => to avoid error , dictionary is searchde otherwise returns None , but we dont want None , so 
false

render_template() => REFRESH THE PAGE => SO AGAIN PASS THE PARAMETERS code and name 

5 . instead of authentication => create session to store temporary data 
session["room"] = room  
session["name"] = name

end if => wrong in flask , endif = correct 
room = session.get("room") => this part will actually get the room , otherwise routing will not take place 

6. socket-io STUFF

@socketio.on('connect') => 
Receiving Messages
When using SocketIO, messages are received by both parties as events. On the client side Javascript callbacks 
are used. With Flask-SocketIO the server needs to register handlers for these events, similarly to how routes 
are handled by view functions.

7 WHEN MORE THAN 1 USER => REFERESH THE PAGE, NOTHING IS GONE , 
but if 1 person  => redirect to home page when refreshed chat room  

8.  listen for the server event message and then callback function data(has name and message) => now we are 
able to see the joined and left messages on the scren 
    socketio.on("message", (data) => {
        createMessage(data.name, data.message);
    })

9. to send messages , our flask server should listen     
emit(event, *args, **kwargs)
Emit a server generated SocketIO event.