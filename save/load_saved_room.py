def load_saved_room(room_name:str) -> str:
    """returns the html content for the corresponding room name in 'saved rooms' as str
    if the room does not exist 404 is returned as str"""

    try:
        with open(f"saved rooms/{room_name}.html", "r") as d:
            html = d.read()
    except:
        with open("templates/404.html", "r") as d:
            html = d.read()

    return html