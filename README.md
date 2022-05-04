# voter
Voting platform built with Python-Flask
# setup
Create a new folder named "ready rooms" in "/voter"
# requirements
Python 3.10
Flask
# files in project
## /data
This is where the results from voting are stored.
**amount.json** contains a number to keep the results unique.
All the html files in this directory can be deleted if you wish too. But **not** the json file.
## /default settings
Contains the default setting for when you start the server.
All the file names should make it obvious for what they contain.
Please change the contents in those files.
## /rooms
Contains Python code.
## /save
Contains more Python code.
## /saved rooms
Contains rooms that aren't finished jet, meaning they are still being worked at.
**amount.json** contains a number to keep the rooms unique.
All the html files in this directory can be deleted if you wish too. But **not** the json file.
## /templates
A bunch of html files for the server pages.
## /tools
Python files for clearing **/data**, **/ready rooms** and **/saved rooms**
They also reset the content in the json files for the corresponding directorys.
To use the files move them up one directory.
## /ready rooms
(Don't forget to create this folder!)
Contains the compiled rooms for voting.
# using the voter
## voting
To vote direct to the homepage (e.g. "http://localhost:5000").
## signing in as admin
To sign in as admin go to **/admin** (e.g. "http://localhost:5000/admin") and enter the admin password.
When you're on **/admin** you can see a navbar at the top, pressing any of the links in there will redirect you to the homepage if you aren't an admin.
## using admin tools
### creating rooms
Go to **/create%20room** (e.g. "http://localhost:5000/create%20room") (the first link in the nav bar).
You need to enter thr room name in the **Please enter room name.** input field.
You can add questions using the **Add question** button.
When you add an question you can enter it's description in **Please enter question.** input field.
Pressing the **x** button next to the input field (^) you can remove the question.
Next there are a range bar and an input for changing its length **or** a checkbox.
The last thing is the **Change input type** button which switches between the two modes (^).
At the button there's a **Submit** button, this does nothing unless the **Please enter room name.** input field and all the **Please enter question.** input field are filled in and there is at least one question.
## viewing unfinished rooms
Go to **/saved%20rooms** (e.g. "http://localhost:5000/saved%20rooms") (the second link in the nav bar).
Here you can see a bunch of links for each saved room, pressing one will redirect you and allow you to edit it.
## compiling rooms for voting
Go to **/ready%20rooms** (e.g. "http://localhost:5000/ready%20rooms") (the third link in the nav bar).
You can enter a room name in the input field and compile the room by pressing the **Add room** button.
You can use the names from **/saved%20rooms**.
Beneth the input field and the button you can see some links (if you already compiled rooms) which when pressed lead you to a preview for the room when it's opened for voting.
## opening rooms for voting
Go to **/opened%20rooms** (e.g. "http://localhost:5000/opened%20rooms") (the fourth link in the nav bar).
You can enter a room name in the input field and open the room by pressing the **Open** button.
You can use the names from **/ready%20rooms**.
## closing rooms after voting
Go to **/closed%20rooms** (e.g. "http://localhost:5000/closed%20rooms") (the fifth and last link in the nav bar).
You can enter a room name in the input field and close the room by pressing the **Close** button.
When a room is closed it's automatically evaluated.
You can view the evaluations py pressing the links below the input field (if you already closed some rooms) and the button.
# starting the server
After executing **main.py** you will see following output:

Do you want to follow the default startup (1), use a custom one (2) or host in your local network (3)?
        |
  
Entering **1** will start the server with the default setting on localhost.
Entering **2** will allow you to uniquely enter a few things.
Entering **3** will start the server visible and accessable to your local network, for the rest the default settings are used.
# closing the server
Just kill the programm (Ctrl + C).
