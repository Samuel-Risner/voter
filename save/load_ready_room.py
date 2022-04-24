def load_ready_room(room_name:str) -> str:
    """returns the html content for the corresponding room name in 'ready rooms' as str
    if the room does not exist 404 is returned as str"""
    
    try:
        with open(f"ready rooms/{room_name}.html", "r") as d:
            html = d.read()
    except:
        with open("templates/404.html", "r") as d:
            html = d.read()

    return html