import json

def save_room_wip(r:dict) -> str:
    """saves the inputed form 'create_room()' (in 'main.py') to 'saved rooms'
    and increases the count in 'amount.json' (in 'saved rooms')"""

    with open("templates/admin_create_room.html", "r") as d:
        raw_html = d.read()

    raw_html = part1(raw_html, r)
    raw_html = part2(raw_html, r)
    raw_html = part3(raw_html, r)
    raw_html = part4(raw_html, r)

    with open("saved rooms/amount.json", "r") as d:
        file_name = json.loads(d.read()) + 1

    with open("saved rooms/amount.json", "w") as d:
        d.write(json.dumps(file_name))

    file_name = str(file_name)

    x = r.get("roomname")
    if x == "":
        file_name += " no name"
    else:
        file_name += " "
        file_name += x

    with open(f"saved rooms/{file_name}.html", "w") as d:
        d.write(raw_html)

    return file_name

# the other functions are for helping ^

def part1(raw_html:str, r:dict) -> str:
    # find str '<input type="text" placeholder="Please enter room name." name="roomname"'(>)
    # add f' value="{x}"' infront of the '>'
    x = r.get("roomname")
    if (x != "") and (x is not None):
        pos = 0
        to_find = '<input type="text" placeholder="Please enter room name." name="roomname"'
        found = 0
        for i in raw_html:
            pos += 1
            if i == to_find[found]:
                found += 1
                if found >= len(to_find):
                    p1 = raw_html[:pos]
                    p2 = f' value="{x}"'
                    p3 = raw_html[pos:]

                    raw_html = p1 + p2 + p3
                    break
            else:
                found = 0

    return raw_html

def part2(raw_html:str, r:dict) -> str:
    def comile_question(nr:int) -> str:
        if f"type{nr}" in r:
            change_type = ""
        else:
            change_type = f"change_input_type({nr});"

        return f"""const par{nr} = document.createElement("P");
par{nr}.id = "paragraph" + {nr};
const question_input{nr} = document.createElement("INPUT");
question_input{nr}.type = "text";
question_input{nr}.name = "question" + {nr};
question_input{nr}.id = question_input{nr}.name;
question_input{nr}.placeholder = "Please enter question.";
question_input{nr}.value = "{r[f"question{nr}"]}"
const button_remove{nr} = document.createElement("BUTTON");
button_remove{nr}.addEventListener('click', () => {"{"}
    remove("paragraph" + {nr});
    for(let i = 0; i < question_ids.length; i++){"{"} 
        if( question_ids[i] == {nr}){"{"} 
            question_ids.splice(i, 1); 
        {"}"}
    {"}"}
    document.getElementById("ids_list").value = question_ids;
    event.preventDefault();
{"}"});
button_remove{nr}.innerHTML = "<span>&times;</span>";
const input_type{nr} = document.createElement("INPUT");
input_type{nr}.type = "range";
input_type{nr}.min = "0";
input_type{nr}.max = "{r[f"numbers{nr}"]}";
input_type{nr}.value = "0";
input_type{nr}.id = "type" + {nr};
input_type{nr}.name = "type" + {nr};
const range_numbers{nr} = document.createElement("INPUT");
range_numbers{nr}.type = "number";
range_numbers{nr}.min = "2";
range_numbers{nr}.value = "{r[f"numbers{nr}"]}";
range_numbers{nr}.id = "numbers" + {nr};
range_numbers{nr}.name = "numbers" + {nr};
range_numbers{nr}.oninput = () => {"{"}
    if(input_type{nr}.type == "range"){"{"}
        input_type{nr}.max = range_numbers{nr}.value;
    {"}"};
{"}"};
const button_change_input_type{nr} = document.createElement("BUTTON");
button_change_input_type{nr}.addEventListener('click', () => {"{"}
    change_input_type({nr});
    event.preventDefault();
{"}"});
button_change_input_type{nr}.innerText = "Change input type";
par{nr}.appendChild(document.createElement("HR"))
par{nr}.appendChild(question_input{nr});
par{nr}.appendChild(button_remove{nr});
par{nr}.appendChild(document.createElement("BR"));
par{nr}.appendChild(input_type{nr});
par{nr}.appendChild(document.createElement("BR"));
par{nr}.appendChild(range_numbers{nr});
par{nr}.appendChild(document.createElement("BR"));
par{nr}.appendChild(button_change_input_type{nr});
document.getElementById("questions").appendChild(par{nr});
{change_type}
"""
    # add questions
    x = r.get("ids_list")
    if (x != ""):
        try:
            x = list(x)
            to_remove = []
            for i in x:
                if i == ",":
                    to_remove.append(i)
            for i in to_remove:
                x.remove(i)
        except:
            return raw_html

        script = "\n"
        for i in x:
            try:
                i = int(i)
            except:
                return raw_html

            script += comile_question(i)
            script += "\n"

        script += 'document.getElementById("ids_list").value = question_ids;\n'
        script += "</script>\n"

        l = len(raw_html) - len("\t</script>\n{% endblock %}")
        p1 = raw_html[:l]
        raw_html = p1 + script + "{% endblock %}"

    return raw_html

def part3(raw_html:str, r:dict):
    # change "question_id = 0;" to f"question_id = {int(x[-1])};"
    x = r.get("ids_list")
    if (x != ""):
        try:
            x = list(x)
        except:
            return raw_html

    pos = 0
    to_find = 'question_id = 0;'
    found = 0
    for i in raw_html:
        pos += 1
        if i == to_find[found]:
            found += 1
            if found >= len(to_find):
                p1 = raw_html[:(pos - len(to_find))]
                p2 = f"question_id = {int(x[-1])};"
                p3 = raw_html[pos:]

                raw_html = p1 + p2 + p3
                break
        else:
            found = 0

    return raw_html

def part4(raw_html:str, r:dict):
    # change "question_ids = [];" to f"question_ids = {r.get("ids_list")};"
    x = r.get("ids_list")

    pos = 0
    to_find = 'question_ids = [];'
    found = 0
    for i in raw_html:
        pos += 1
        if i == to_find[found]:
            found += 1
            if found >= len(to_find):
                p1 = raw_html[:(pos - len(to_find))]
                p2 = f'question_ids = [{r.get("ids_list")}];'
                p3 = raw_html[pos:]

                raw_html = p1 + p2 + p3
                break
        else:
            found = 0

    return raw_html