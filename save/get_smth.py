import os

def get_data() -> list:
    """returns all the html files in 'data' without the '.html' extension"""

    return _get_smth("data")

def get_ready_rooms() -> list:
    """returns all the html files in 'ready rooms' without the '.html' extension"""

    return _get_smth("ready rooms")

def get_saved_rooms() -> list:
    """returns all the html files in 'saved rooms' without the '.html' extension"""

    return _get_smth("saved rooms")

def _get_smth(path:str) -> list:
    """help for the other three 'get_[...]'"""

    x = os.listdir(path)   # get a list of all files in that directory

    to_remove = []
    for i in x:
        if i[-4:] == "json":
            to_remove.append(i)

    for i in to_remove:
        x.remove(i)

    for i in range(0, len(x), 1):
        x[i] = x[i].split(" ")      # split the entrys in x up, so that the numbers
                                    # can be used

    for i in range(0, len(x), 1):   
        temp = x[i]                 # get the entry
        temp[0] = int(temp[0])      # convert the first part in the entry (the number)
                                    # from str to int

    x.sort()                        # is sorted by numbers (low to high)

    # recombine
    for i in range(0, len(x), 1):   # loop through the entrys
        temp = ""

        for j in x[i]:              # add the parts of the entry together (with spaces)
            temp += str(j)
            temp += " "

        temp = temp[:-6]            # remove the extra space and ".html"
        x[i] = temp                 #  overwrite the entry in x

    return x