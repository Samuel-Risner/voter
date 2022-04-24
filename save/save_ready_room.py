import json

def save_ready_room(name_wip:str, *, name_finished:str=None)-> int:
    """
    converts a room from 'saved rooms' to a ready room into 'ready rooms'
    0 -> success
    1 -> file already exists
    2 -> could not open requested file
    3 -> no questions
    4 -> could not decipher question input types
    """

    if name_finished is None:
        name_finished = name_wip

    # if file is already in existence
    try:
        with open(f"ready rooms/{name_finished}.html", "r") as d:
            d.read()
        file_already_exists = True
    except:
        file_already_exists = False

    if file_already_exists:
        return 1

    # read wip
    try:
        with open(f"saved rooms/{name_wip}.html", "r") as d:
            html_wip = d.read()
    except:
        return 2
    
    # get room name from file
    to_find = '<input type="text" placeholder="Please enter room name." name="roomname" value="'
    found = 0
    pos = 0
    for i in html_wip:
        pos += 1
        if i == to_find[found]:
            if found >= len(to_find) - 1:
                break
            found += 1
        else:
            found = 0

    name = ""
    pos1 = pos
    while True:
        part = html_wip[pos1]

        if part == '"':
            break
        else:
            name += part

        pos1 += 1

    # get question from file
    to_find = "let question_ids = "
    found = 0
    pos = 0
    for i in html_wip:
        pos += 1
        if i == to_find[found]:
            if found >= len(to_find) - 1:
                break
            found += 1
        else:
            found = 0

    list_ = ""
    pos1 = pos
    while True:
        part = html_wip[pos1]

        if part == ';':
            break
        else:
            list_ += part

        pos1 += 1

    list_ = list_[1:-1]
    if len(list_) <= 0:
        return 3

    list_ = list_.split(",")

    # values for input_number
    question_names = []
    for i in list_:
        to_find = f'question_input{i}.value = "'
        found = 0
        pos = 0
        for i in html_wip:
            pos += 1
            if i == to_find[found]:
                if found >= len(to_find) - 1:
                    break
                found += 1
            else:
                found = 0

        q = ""
        pos1 = pos
        while True:
            part = html_wip[pos1]

            if part == '"':
                break
            else:
                q += part

            pos1 += 1

        question_names.append(q)

    # input types
    # f"change_input_type({number});" 
    #   -> 1 time   -> "range"
    #   -> 2 times  -> "checkbox"
    input_types = []
    for i in list_:
        temp = html_wip.split(f"change_input_type({i});")
        if len(temp) == 2:
            input_types.append("range")
        elif len(temp) == 3:
            input_types.append("checkbox")
        else:
            return 4

    # max values for range
    max_values = []
    for i in range(0, len(list_), 1):
        if input_types[i] == "range":

            to_find = f'input_type{list_[i]}.max = "'
            found = 0
            pos = 0
            for i in html_wip:
                pos += 1
                if i == to_find[found]:
                    if found >= len(to_find) - 1:
                        break
                    found += 1
                else:
                    found = 0

            temp = ""
            pos1 = pos
            while True:
                part = html_wip[pos1]

                if part == '"':
                    break
                else:
                    temp += part

                pos1 += 1
            max_values.append(int(temp))
        else:
            max_values.append(None)

    # write
    content = '{% extends "base.html" %}\n'
    content += '{% block title %}'
    content += f'{name}'
    content += '{% endblock %}'
    content += "{% block content %}"
    content += f'<h1>{name}</h1>\n'
    content += '<form method="post">\n'

    for i in range(0, len(list_), 1):
        i = int(i)

        if input_types[i] == "range":
            c = f"""<p>
{question_names[i]}
<br>
<input type="range" min="0" max="{max_values[i]}" value="0" name="q{i}">
</p>"""
        elif input_types[i] == "checkbox":
            c = f"""<p>
{question_names[i]}
<br>
<input type="checkbox" name="q{i}">
</p>"""

        content += c

    content += '<button class="btn btn-primary" type="submit">Submit</button></form>'
    content += "{% endblock %}"

    with open(f"ready rooms/{name_finished}.html", "w") as d:
        d.write(content)

    # save question types and data in json
    to_json = []

    for i in range(0, len(list_), 1):
        i = int(i)

        if input_types[i] == "range":
            to_json.append(("range", max_values[i], question_names[i]))
        elif input_types[i] == "checkbox":
            to_json.append(("checkbox", 0, question_names[i]))

    with open(f"ready rooms/{name_finished}.json", "w") as d:
        d.write(json.dumps(to_json))

    # end
    return 0