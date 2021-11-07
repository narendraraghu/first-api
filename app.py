from flask_restful import Resource, Api
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL
import os

app = Flask(__name__)
api = Api(app)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'flaskapi'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.14'
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
        resp = jsonify("Message created successfully!", row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
