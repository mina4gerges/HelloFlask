from flask import Flask, request
import mysql.connector
from mysql.connector import Error
from version2.dataBase import host, user, dbname, password

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello"


@app.route('/data', methods=['POST', 'GET'])
def data():
    global conn, cursor

    try:
        conn = mysql.connector.connect(host=host,
                                       database=dbname,
                                       user=user,
                                       password=password)
        if conn.is_connected():
            cursor = conn.cursor()

            if request.method == 'POST':
                params = request.json

                title = params.get('intro_title')
                desc = params.get('intro_desc')
                image = params.get('intro_image')

                query = "INSERT INTO screens (intro_title, intro_desc, intro_image) VALUES (%s, %s, %s);"

                cursor.execute(query, (title, desc, image))
                conn.commit()

                return "Inserted 1 row"

            if request.method == 'GET':
                query = "SELECT * FROM screens;"

                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                return str(rows)

    except Error as e:
        return 'error occurred', e
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")


@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):
    global conn, cursor

    try:
        conn = mysql.connector.connect(host=host,
                                       database=dbname,
                                       user=user,
                                       password=password)
        if conn.is_connected():
            cursor = conn.cursor()

            if request.method == 'GET':
                query = "SELECT * FROM screens WHERE intro_id = %s ;"

                cursor.execute(query, id)
                rows = cursor.fetchall()
                return str(rows)

            if request.method == 'DELETE':
                query = "DELETE FROM screens WHERE intro_id = %s;"

                cursor.execute(query, id)
                conn.commit()
                return "deleted"

            if request.method == 'PUT':
                params = request.json

                title = params.get('intro_title')
                desc = params.get('intro_desc')
                image = params.get('intro_image')

                query = "UPDATE screens SET intro_title = %s,intro_desc =%s,intro_image=%s WHERE intro_id = %s;"

                cursor.execute(query, (title, desc, image, id))
                conn.commit()
                return "updated"

    except Error as e:
        return 'error occurred', e
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    app.run(debug=True)
