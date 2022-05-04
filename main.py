from flask import Flask, render_template, request, flash, redirect, url_for, render_template_string
from rooms import RoomHandler, check_user_input
from get_info import get_info
from admin import Admins
from save import save_room_wip, load_saved_room, get_saved_rooms, save_ready_room, get_ready_rooms, load_ready_room, get_data

secret_key, admin_password, port, host = get_info()

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key

room_handler = RoomHandler()
admins = Admins(admin_password)

#
# - for normal users
#

# enter room
@app.route("/", methods=["GET", "POST"])
def home():
    """Page for entering rooms
     - input:  room name
     - submit: redirect to room if it exists, else flash an error"""

    if request.method == "POST":
        room_name = request.form.get("room")

        if room_handler.get_room(room_name): # is not None          # success
            return redirect(url_for(".vote", room_name=room_name))
        else:                                                       # error
            flash("Room does not exist.", category="error")

    return render_template("index.html")                            # default

# vote
@app.route("/vote/<room_name>", methods=["GET", "POST"])
def vote(room_name:str):
    """Voting page for room
    redirect to home if room is not opened"""

    ip = request.remote_addr
    answer = room_handler.add_user(room_name, ip)

    # room exists
    if answer[0]: # is True
        room = answer[1]
    # room does not exist
    else:
        flash("Room does not exist.", category="error")
        return redirect(url_for("home"))

    if request.method == "POST":
        r = request.form
        result = check_user_input(room_name, r)

        # successfully evaluated
        if result[0]:
            # successfully voted
            if room_handler.add_result(room_name, result[1]):
                flash("You succesfully voted.", category="success")
            # room is closed
            else:
                flash("Room is already closed.", category="error")
            
            return redirect(url_for("home"))

        # some other error
        else:
            flash("Do not mess with me.", category="error")

    return render_template_string(room.get_html())

#
# - admin
#

# login as admin
@app.route("/admin", methods=["GET", "POST"])
def admin():
    """page to login as admin
    admin role is bound to ip"""

    if request.method == "POST":
        password = request.form.get("password")

        # password is correct
        if password == admins.password:
            ip = request.remote_addr
            admins.add_admin(ip)
            flash("Signed in as admin.", category="success")
        # password is incorrect
        else:
            flash("Invalid password.", category="error")

    # page stays the same, since the navbar is already visible
    return render_template("admin.html")

#
# - admin pages with checking if user is admin (accessible in nav bar)
#

# !!! important note:
#     admin pages have less error handeling, since the admins are expected to behave

# create a new room
@app.route("/create room", methods=["GET", "POST"])
def create_room():
    """create a new room"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        if request.method == "POST":
            r = request.form

            # save the room data in "saved rooms"
            file_name = save_room_wip(r)
            flash(f'Saved room as "{file_name}" in "saved rooms".', category="success")

        return render_template("admin_create_room.html")

    else:
        flash("You are not an admin.", category="error")
        # in case a normal user wandered of (accidently)
        return redirect(url_for("home"))

@app.route("/saved rooms")
def saved_rooms():
    """shows a list of all saved rooms in 'saved rooms'
    links in html page redirect to '/edit room/room name'"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        return render_template("admin_saved_rooms.html", files=get_saved_rooms())

    else:
        flash("You are not an admin.", category="error")
        return redirect(url_for("home"))

@app.route("/ready rooms", methods=["GET", "POST"])
def ready_rooms():
    """shows the rooms in 'ready rooms'
    through the input rooms in 'saved rooms' rooms can be made ready
    ready rooms can be opened for voting"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        if request.method == "POST":
            r = request.form
            file_name = r.get("file_name")
            if file_name in get_ready_rooms():
                flash("This file was already processed.", category="error")
                return render_template("admin_ready_rooms.html", files=get_saved_rooms())
            else:
                a = save_ready_room(file_name)

                # success
                if a == 0:
                    flash('Saved room in "ready rooms"', category="success")

                # other errors
                elif a == 1:
                    flash("This file already exists.", category="error")
                elif a == 2:
                    flash("Could not open requested file.", category="error")
                elif a == 3:
                    flash("No questions.", category="error")
                elif a == 4:
                    flash("Could not decipher question input types.", category="error")

        return render_template("admin_ready_rooms.html", files=get_ready_rooms())

    else:
        flash("You are not an admin.", category="error")
        return redirect(url_for("home"))

@app.route("/opened rooms", methods=["GET", "POST"])
def opened_rooms():
    """through the input ready rooms can be opened
    open rooms are accessible for voting"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        if request.method == "POST":
            r = request.form
            room = r.get("room_to_open")

            if room in get_ready_rooms():
                # could open room
                if room_handler.open_room(room):
                    flash("Opened room.", category="success")
                # room is already open
                else:
                    flash("Room is already open.", category="error")
            # no ready room / does not exist
            else:
                flash("Room does not exist or is not ready.", category="error")

        return render_template("admin_opened_rooms.html", opened_rooms=room_handler.get_opened_rooms())

    else:
        flash("You are not an admin.", category="error")
        return redirect(url_for("home"))

@app.route("/closed rooms", methods=["GET", "POST"])
def closed_rooms():
    """close an opened room
    when closing a room it is automatically evaluated
    links in html lead to the evaluated content"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        if request.method == "POST":
            r = request.form
            room_name = r.get("room_to_close")

            # if room is open
            if room_name in room_handler.get_opened_rooms():
                room_handler.close_room(room_name)
                flash("Closed room.", category="success")
            
            # if room is not open / does not exist
            else:
                flash("Room is not opened or does not exist room.", category="error")

        return render_template("admin_closed_rooms.html", evaluated_rooms=get_data())

    else:
        flash("You are not an admin.", category="error")
        return redirect(url_for("home"))

#
# - admin - pages for displaying content (not directly accessible in nav bar)
#

# chance to edit rooms again after creating them
@app.route("/edit room/<room_name>", methods=["GET", "POST"])
def edit_room(room_name):
    """responsible for editing already created rooms in 'saved rooms'
    (similar to 'create_room()')
    404 if room does not exist"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        if request.method == "POST":
            r = request.form

            file_name = save_room_wip(r)
            flash(f'Saved room as "{file_name}" in "saved rooms".', category="success")        

        # show html of the corresponding room
        # "load_saved_room(room_name)" returns 404 if room does not exist
        return render_template_string(load_saved_room(room_name))

    else:
        flash("You are not an admin.", category="error")
        return redirect(url_for("home"))

# look at rooms ready for voting
@app.route("/view room/<room_name>")
def view_room(room_name):
    """responsible for showing rooms that are ready for voting (in 'ready rooms')
    404 if room is not ready / does not exist"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        # show html of the corresponding room
        # "load_ready_room(room_name)" returns 404 if room does not exist
        return render_template_string(load_ready_room(room_name))

    else:
        flash("You are not an admin.", category="error")
        return redirect(url_for("home"))

# results from voting
@app.route("/evaluated rooms/<room_name>")
def evaluated_rooms(room_name):
    """responsible for showing voting data from closed rooms
    redirects to '/closed rooms' if data does not exist"""

    ip = request.remote_addr
    if admins.is_admin(ip):
        # data exists
        if room_name in get_data():
            with open(f"data/{room_name}.html", "r") as d:
                html = d.read()

            return render_template_string(html)

        # data does not exist
        else:
            flash("Data was not found.", category="error")
            return redirect(url_for("closed_rooms"))

    else:
        flash("You are not an admin.", category="error")
        return redirect(url_for("home"))

# misc
@app.errorhandler(404)
def not_found(e):
    """404"""
    return render_template("404.html")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(port=port, host=host)
    # app.run(debug=True, port=port, host=host)
