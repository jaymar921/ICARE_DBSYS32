from database import createAccount, generateAccountID, createEmployee, loginAccount, registerPet, getPets, getServices
from flask import Flask, render_template, request, redirect, url_for, session
from utility import parseNewAccount, parseNewEmployeeAccount, isEmail, hashData, parsePet

app = Flask('__main__')
app.secret_key = '39cm85yu234m98'
uuid_data: dict = {}


@app.route("/")
def homepage():
    if "username" in session:
        return render_template("homepage.html", account=session['username'], login="none", logout="block")
    return render_template("homepage.html", login="block", logout="none")


@app.route("/login")
def login():
    return render_template("login.html", log_remark="")


@app.route("/login_account", methods=['POST'])
def login_account():
    data: list = loginAccount(request.form['email'], hashData(request.form['psw']), isEmail(request.form['email']))
    if len(data) == 2:
        session['username'] = data[1].username
        uuid_data[data[1].username] = data[1].acc_id
        return redirect(url_for("homepage"))
    else:
        return render_template("login.html", log_remark="Invalid Credentials")


@app.route("/services/")
def services_invalid():
    return redirect(url_for("login"))


@app.route('/services/<account>')
def services(account: str):
    if account == session['username']:
        data = getServices()
        _service_: dict = {}
        for x in data:
            _service_[x['service_code']] = x
        return render_template("services.html", account=account, data=_service_, pets=getPets(account))
    return redirect(url_for("not_found"))


@app.route("/inquiry", methods=['POST'])
def inquiry():
    data: dict = {
        'pet_owner': request.form['pet_owner'],
        'pet_name': request.form['pet_name'],
        'service_code': request.form['serv_code'],
        'date': request.form['schedule_date'],
        'venue': request.form['venue']
    }
    pass


@app.route("/pets/")
def pets_invalid():
    return redirect(url_for("login"))


@app.route('/pets/<account>')
def pets(account):
    if account == session['username']:
        data = getPets(account)
        return render_template("Pets.html", account=account, pets=data)
    return redirect(url_for("login"))


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
    if request.form['password'] != request.form['confirm']:
        return render_template("registration.html", register_remark="Password mismatch!")
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


@app.route("/register_pet", methods=['POST'])
def register_pet():
    data: dict = {
        'name': request.form['name'],
        'specie': request.form['specie'],
        'age': request.form['age'],
        'gender': request.form['gender'],
        'breed': request.form['breed'],
        'bloodtype': request.form['bloodtype'],
        'weight': request.form['weight'],
        'owner_id': uuid_data[request.form['user']]
    }
    registerPet(parsePet(data))
    return redirect(url_for('pets', account=request.form['user']))


@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store,no-cache,must-revalide,post-check=0,pre-check=0')
    return response


@app.route("/404")
def not_found():
    return "Uh oh... page not found"


@app.route("/logout/<account>")
def logout(account):
    if account in session['username']:
        uuid_data[session['username']] = {}
        session.clear()
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("not_found"))


@app.route("/logout/")
def logout_invalid():
    return redirect(url_for("homepage"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
