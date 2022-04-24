import json

def check_user_input(room_name:str, answ:dict) -> tuple:
    """checks if the answer-dict matches the corresponding info in the json_file for the room
    and evaluates the the answer
    first part of tuple:
        True: if the json-file could be opened and the answer successfully evaluated
        False: if not
    second part:
        None if the first part is False
        list if the first part is True
            False or True if checkbox is checked or is not (not in answer)
            int corresponding the value of range
    Potential risk of correct evaluation if a checkbox is missing, since if it is not checked it
    also is not in the answer"""

    answ_eval = []

    # try to read json
    try:
        with open(f"ready rooms/{room_name}.json", "r") as d:
            json_content = json.loads(d.read())
    except:
        return (False, None)

    # evaluate answer corresponding to json-file (list)
    for i in range(0, len(json_content), 1):
        if json_content[i][0] == "checkbox":
            if f"q{i}" in answ:
                answ_eval.append(True)
            else:
                # if box is not checked it does not appear in the answer
                answ_eval.append(False)

        elif json_content[i][0] == "range":
            if f"q{i}" in answ:
                r = answ.get(f"q{i}")
                try:
                    r = int(r)
                    answ_eval.append(r)
                except:
                    # just in case
                    answ_eval.append(0)
            else:
                return (False, True)

    return (True, answ_eval)