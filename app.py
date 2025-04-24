from flask import Flask, make_response, request, jsonify
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import mysql.connector

SERVER_NAME = "localhost"
USERNAME = "root"
PASSWORD = "password"

def connectSql(database_name):
    return mysql.connector.connect(host=SERVER_NAME, user=USERNAME, password=PASSWORD, database=database_name)

def returnQueryResults(query, params=None):
    connection = connectSql("")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        retval = cursor.fetchall()
    except mysql.connector.Error as e:
        retval = make_response(f"Query Execution Error: {e}", 400)
    finally:
        cursor.close()
        connection.close()
    return retval

def executeQuery(query, params=None):
    connection = connectSql("lab3")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        retval = {"success": "Customer added"}
    except mysql.connector.Error as e:
        retval = {"error": f"Query Execution Error: {e}"}
    finally:
        cursor.close()
        connection.close()
    return make_response(jsonify(retval), 201 if 'success' in retval else 400)

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>OURVLE CLONE API</h1>"


if __name__ == '__main__':
    app.run(port=8000, debug=True)