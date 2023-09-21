import logging
import sqlite3
from os.path import exists


from flask import Flask, render_template, send_from_directory, request, url_for, redirect

from main import config
from main import database
from main.config import *


legalName =""


def create_app():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    app = Flask('app')
   

    # Register 404 handler
    app.register_error_handler(404, page_not_found)

    # Routes:
    @app.route('/')
    def home():
        users = database.get_data()
        return render_template('login.html', users=users)

    # @app.route('/login')
    # def login():
       
    #     return render_template('login.html')
    

    @app.route('/checkin', methods=['POST'])
    def user_form():
        if request.method == 'POST':
            users = database.get_data()

            # get variables from request
            name = request.form['name']
            email = request.form['email']
            role = request.form['role']
            description = request.form['description']
           
            # insert into database
            database.insert_user(name, email, role, description)
            users = database.get_data()

            return redirect(url_for("home"))

    
    @app.route('/dutyBoard')
    def dutyBoard():
        users = database.get_data()
        return render_template('dutyBoard.html', users=users)

    @app.route('/delete', methods=["POST"])
    def deleteUser():
        email = request.form["getEmail"]
        print(email)
        database.delete_user(email)
        return redirect(url_for("home"))
        
    @app.route('/forceDelete', methods=['POST', 'GET'])
    def force_delete():
        database.force_delete_table()
        return "okay"

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   )

    initialise_db(app.root_path)


    return app


def page_not_found(error):
    return render_template('error.html'), 404


def initialise_db(directory_path):
    """Function to connect to SQLite DB, including DB creation and config if required"""

    # create path to DB file and store in config
    path_to_db_file = os.path.join(directory_path, 'app.sqlite')
    database.set_path_to_db_file(path_to_db_file)

    # check if DB file already exists - if not, execute DDL to create table
    if not exists(path_to_db_file):
        database.create_table()


if __name__ == '__main__':
    web_app = create_app()

    logging.info(f"Running on http://localhost:{get_port()}")
    web_app.run(debug=True, port=get_port(), host='0.0.0.0')


