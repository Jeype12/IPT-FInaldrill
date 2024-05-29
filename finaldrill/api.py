from flask import Flask, make_response, jsonify,request
from flask_mysqldb import MySQL


app = Flask(__name__)
# MySQL configurations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "kwikkwikcafe"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)  # Create an instance of MySQL and bind it to the Flask app

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/employee", methods=["GET"])
def get_employee():
    cur = mysql.connection.cursor()
    query = """SELECT * FROM kwikkwikcafe.employee"""
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)

@app.route("/employee/<int:id>", methods=["GET"])
def get_employee_id(id):
    cur = mysql.connection.cursor()
    query = """SELECT * FROM kwikkwikcafe.employee where EmployeeID = {}""".format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

@app.route("/employee", methods=["POST"])
def add_employee():
    cur = mysql.connection.cursor()
    info = request.get_json()
    Branch_ID = info["Branch_ID"]
    Name = info['Name']
    Date_of_Birth = (info['Date_of_Birth'])

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO EMPLOYEE (Branch_ID, Name, Date_of_Birth)
        VALUES (%s, %s, %s)
    """, (Branch_ID, Name, Date_of_Birth))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "Branch added successfully",
                                  "rows_affected": rows_affected}), 201)

if __name__ == "__main__":
    app.run(debug=True)