# Squares
Squares is a board games. Just for fun.

# To run this function, you need to do as follows:

* Install Python Interpreter. Python 2.7 or Python 3.4 is recommended.
* run: `virtualenv venv`
* `source venv/bin/activate` or `source venv/Scripts/activate` if you run on a Windows System.
* `pip install -r requirements.txt`
* `cp .env.example .env`
* create a mysql database `squares`
* `make upgrade`
* `python manager runserver`
* Then your program is running and listening on the port 5000. Try to post a request to your server.
