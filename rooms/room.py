from .user_handler import UserHandler
import json

class Room():
    def __init__(self, name:str):
        self.name = name

        self.user_handler = UserHandler()

        self.results = []

    def get_html(self) -> str:
        """return the the text from the corresponding html file in '/ready rooms'"""

        with open(f"ready rooms/{self.name}.html", "r") as d:
            html = d.read()

        return html

    def add_user(self, ip):
        """adds a user"""

        self.user_handler.add_user(ip)

    def add_result(self, result):
        """adds a result"""

        self.results.append(result)

    def load_results_html(self):
        """saves the results from the room"""
        
        questions = [] # makes it easier to edit in vs-code
        with open(f"ready rooms/{self.name}.json", "r") as d:
            questions = json.loads(d.read())
            """[[range or checkbox:str, length or range or 0 if checkbox:int, question name:str], ...]"""

        c = '{% extends "admin_base.html" %}'   # inheritance
        c += f'{"{"}% block title %{"}"} Results: {self.name} {"{"}% endblock %{"}"}'
        # page title
        c += "{% block content %}"      # start page content
        c += f"<h1>{self.name}</h1>"    # title

        for question_nr in range(0, len(questions), 1):   # goes through the questions
            c += f"<h2>{questions[question_nr][2]}</h2>"  # title for question
            
            # for result in self.results: # goes through the results

            if questions[question_nr][0] == "checkbox": # evaluate if checkbox
                p1 = 0  # people who checked
                p2 = 0  # people who did not check

                for i in self.results:  # how many people voted for what
                    if i[question_nr]:
                        p1 += 1 # people who checked
                    else:
                        p2 += 1 # people who did not check

                if len(self.results) != 0:
                    r1 = int((p1 / len(self.results)) * 100)    # percentages of people who checked
                    r2 = (100 - r1)                             # and of those who did not
                else:
                    r1 = 0
                    r2 = 0
                c += f"{r1}% checked and"   # description for progressbar
                c += "<br>"                 # --"--
                c += f"{r2}% did not."      # --"--

                c += f'<div id="progress_{str(question_nr)}">'  # empty progressbar
                c += f'<div id="bar_{str(question_nr)}"></div>'  # prograss
                c += "</div>"                                   # end empty progressbar

                c += "<style>"                                  # start styling the progressbars
                
                c+= f'#progress_{str(question_nr)} {"{"}'     # for empty progressbar
                c += "width: 1000px;"                           # fixed width/length
                c += "background-color: rgb(237, 225, 225);"    # colour
                c += "}"                                    # end for empty progressbar

                c += f'#bar_{str(question_nr)} {"{"}'         # for progress
                c += f"width: {str(r1 * 10)}px;"                # width/length dependend on voting percent
                c += "height: 30px;"                            # fixed height
                c += "background-color: green;"                 # colour
                c += "}"                                    # end for progress

                c += "</style>"                                 # end styling the progressbars

            elif questions[question_nr][0] == "range": # evaluateif range
                options = []    # options for answer

                # fill options
                for _ in range(0, questions[question_nr][1] + 1, 1):
                    options.append(0)

                # how many people voted for what
                for result in self.results:
                    options[result[question_nr]] += 1

                percentages = []    # of people who voted for smth

                # fill/calculate percentages
                for amount_of_people_who_voted in options:
                    if len(self.results) != 0:
                        percentages.append(int((amount_of_people_who_voted / len(self.results) * 100)))
                    else:
                        percentages.append(0)

                for option in range(0, len(percentages), 1):
                    c += f"{percentages[option]}%\t voted {option}"
                    
                    # similar to checkbox but:
                    #   more bars (one for each option)
                    c += f'<div id="progress_{str(question_nr)}_{str(option)}">'
                    c += f'<div id="bar_{str(question_nr)}_{str(option)}"></div>'
                    c += "</div>"

                    c += "<style>"
                    c += f'#progress_{str(question_nr)}_{str(option)} {"{"}'
                    c += "width: 1000px;"
                    c += "background-color: rgb(237, 225, 225);"
                    c += "}"
                
                    c += f'#bar_{str(question_nr)}_{str(option)} {"{"}'
                    c += f"width: {str(percentages[option] * 10)}px;"
                    c += "height: 30px;"
                    c += "background-color: green;"
                    c += "}"

                    c += "</style>"

        c += "{% endblock %}"           # end page content

        with open("data/amount.json", "r") as d:
            next_num = json.loads(d.read())

        with open("data/amount.json", "w") as d:
            d.write(json.dumps(next_num + 1))

        with open(f"data/{next_num} {self.name}.html", "w") as d:
            d.write(c)