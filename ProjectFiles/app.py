from database import createAccount, generateAccountID, createEmployee, loginAccount
from ProjectFiles.Entity.Entity import Account, LoginCredentials
from flask import Flask, render_template, request, redirect, url_for
from utility import parseNewAccount, parseNewEmployeeAccount, isEmail, hashData

app = Flask('__main__')


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_account", methods=['POST'])
def login_account():
    data: list = loginAccount(request.form['email'], hashData(request.form['psw']), isEmail(request.form['email']))
    if len(data) == 2:
        return f"Logged IN {data[0]}"
    else:
        return f"Invalid account"


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/admin_register")
def admin_register():
    return render_template("registration_admin.html")


@app.route("/register_account_employee", methods=['POST'])
def admin_registration():
    data: dict = {
        'lastname': request.form['lastname'],
        'firstname': request.form['firstname'],
        'birthdate': request.form['birthdate'],
        'house_no': request.form['house_no'],
        'street': request.form['street'],
        'barangay': request.form['barangay'],
        'city': request.form['city'],
        'zip': request.form['zip'],
        'username': request.form['username'],
        'password': request.form['password'],
        'email': request.form['email'],
        'contact': request.form['number'],
        'position': request.form['position']
    }
    new_account: list = parseNewEmployeeAccount(data, generateAccountID())
    createEmployee(new_account[0], new_account[1])
    return redirect(url_for("login"))


@app.route("/register_account", methods=['POST'])
def register_account():
    data: dict = {
        'lastname': request.form['lastname'],
        'firstname': request.form['firstname'],
        'birthdate': request.form['birthdate'],
        'house_no': request.form['house_no'],
        'street': request.form['street'],
        'barangay': request.form['barangay'],
        'city': request.form['city'],
        'zip': request.form['zip'],
        'username': request.form['username'],
        'password': request.form['password'],
        'email': request.form['email'],
        'contact': request.form['number'],
    }
    new_account: list = parseNewAccount(data, generateAccountID())
    createAccount(new_account[0], new_account[1])
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
