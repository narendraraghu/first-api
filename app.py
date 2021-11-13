from flask_restful import Api
from flask import jsonify, Flask
from flaskext.mysql import MySQL
import os
import requests

app = Flask(__name__)
api = Api(app)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Kareli@123'
app.config['MYSQL_DATABASE_DB'] = 'flaskapi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
mysql.init_app(app)


@app.route("/message/<string:message_string>", methods=["GET"])
def message(message_string):
    """Function to set message of a specific user in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO message(message) " "VALUES(%s)", message_string)
        row = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        query = {'message_string': message_string, 'message_id': row}
        response = requests.get('http://192.168.166.72:3001/concatenation', params=query)
        print("response " + response.text)
        return jsonify(response.text)
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
