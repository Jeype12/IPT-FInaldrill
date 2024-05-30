from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth
import dicttoxml


app = Flask(__name__)
# MySQL configurations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "kwikkwikcafe"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


mysql = MySQL(app)
auth = HTTPBasicAuth()

users = {"admin1": "root1", "admin2": "root2"}


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None



@app.route("/")
def hello_world():

    style = """
        <style>
            p {
                font-family: Times New Roman, sans-serif;
                font-size: 100px;
                color: white;
                text-align: center;
                background-color: black;
                
                
            }
        </style>
    """
    return f"{style} <p>WELCOME TO KWIKKWIK DATABASE</p>"


@app.route("/employee", methods=["GET"])
@auth.login_required
def get_employee():
    cur = mysql.connection.cursor()
    query = """SELECT * FROM kwikkwikcafe.employee"""
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)


@app.route("/employee/<int:id>", methods=["GET"])
@auth.login_required
def get_employee_id(id):
    cur = mysql.connection.cursor()
    query = """SELECT * FROM kwikkwikcafe.employee where EmployeeID = {}""".format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)


@app.route("/employee", methods=["POST"])
@auth.login_required
def add_employee():
    cur = mysql.connection.cursor()
    info = request.get_json()
    Branch_ID = info["Branch_ID"]
    Name = info["Name"]
    Date_of_Birth = info["Date_of_Birth"]

    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO EMPLOYEE (Branch_ID, Name, Date_of_Birth)
        VALUES (%s, %s, %s)
    """,
        (Branch_ID, Name, Date_of_Birth),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Employee added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/employee/<int:id>", methods=["PUT"])
@auth.login_required
def update_employee(id):
    info = request.get_json()
    Branch_ID = info["Branch_ID"]
    Name = info["Name"]
    Date_of_Birth = info["Date_of_Birth"]

    cur = mysql.connection.cursor()
    cur.execute(
        """
        UPDATE employee SET Branch_ID = %s, Name = %s, Date_of_Birth =%s
        WHERE EmployeeID = %s
    """,
        (Branch_ID, Name, Date_of_Birth, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Employee updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/employee/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_employee(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE EmployeeID = %s", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Employee deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
