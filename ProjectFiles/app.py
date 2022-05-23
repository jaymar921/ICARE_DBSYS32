from datetime import datetime, date

import ProjectFiles.EmailRequestAPI

from database import employeeActivity
from database import createAccount, generateAccountID, createEmployee, loginAccount, registerPet, getPets, getServices
from database import scheduleService, getPendingSchedules, getAdminPendingSchedules, updateAdminPendingSchedules
from database import getAdminApprovedDeclinedSchedules, addTransactions, getClients, getTransactions
from flask import Flask, render_template, request, redirect, url_for, session
from utility import generateUUID, parseNewAccount, parseNewEmployeeAccount, isEmail, hashData, parsePet

app = Flask('__main__')
app.secret_key = '39cm85yu234m98'
uuid_data: dict = {}


@app.route("/")
def homepage():
    if "username" in session and session['username'] in uuid_data:
        return render_template("homepage.html", account=session['username'], login="none", logout="block")
    return render_template("homepage.html", login="block", logout="none")


@app.route("/login")
def login():
    return render_template("login.html", log_remark="")


@app.route("/login_account", methods=['POST'])
def login_account():
    data: list = loginAccount(request.form['email'], hashData(request.form['psw']), isEmail(request.form['email']))
    if len(data) >= 2:
        session['username'] = data[1].username
        uuid_data[data[1].username] = data[1].acc_id
        return redirect(url_for("homepage"))
    else:
        return render_template("login.html", log_remark="Invalid Credentials")


@app.route("/admin_login")
def login_admin():
    return render_template("admin.html")


@app.route("/administration", methods=['POST'])
def administration_login():
    data: list = loginAccount(request.form['email'], hashData(request.form['psw']), isEmail(request.form['email']))
    if len(data) == 3:
        session['username'] = data[1].username
        uuid_data[data[1].username] = data[2].emp_id
        employeeActivity(
            data[2].emp_id,
            datetime.now().strftime("%H:%M:%S"),
            "",
            date.today().strftime("%Y-%m-%d"),
            "Account Login"
        )
        return redirect(url_for("admin_pending_services"))
    else:
        return render_template("login.html", log_remark="Invalid Credentials")


@app.route("/pending_services")
def admin_pending_services():
    data: dict = getAdminPendingSchedules()
    return render_template("adminPendingServices.html", services=data, services_1=getAdminApprovedDeclinedSchedules(),
                           account=uuid_data[session['username']])


@app.route("/update_pending_service", methods=['POST'])
def update_inquiry():
    data: dict = {
        "record_id": request.form['record_id'],
        "pet_id": request.form['pet_id'],
        "pet_owner": request.form['owner_id'],
        "service": request.form['service'],
        "date": request.form['date'],
        "venue": request.form['venue'],
        "remark": request.form['remark']
    }
    if data['remark'] == 'approved' or data['remark'] == 'declined':
        updateAdminPendingSchedules(data)
    elif data['remark'] == 'paid' or data['remark'] == 'cancelled' or data['remark'] == 'cancelled':
        addTransactions(data)
    employeeActivity(
        uuid_data[session['username']],
        "",
        "",
        date.today().strftime("%Y-%m-%d"),
        f"{data['remark']} record -> {data['record_id']}"
    )
    return redirect(url_for("admin_pending_services"))


@app.route("/accounts_admin")
def accountsList():
    employeeActivity(
        uuid_data[session['username']],
        "",
        "",
        date.today().strftime("%Y-%m-%d"),
        "View Client List"
    )
    return render_template("adminClients.html", clients=getClients(), account=uuid_data[session['username']])


@app.route("/transactions_admin")
def transactList():
    employeeActivity(
        uuid_data[session['username']],
        "",
        "",
        date.today().strftime("%Y-%m-%d"),
        "View Transactions"
    )
    return render_template("adminTransaction.html", transact=getTransactions(), account=uuid_data[session['username']])


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
    try:
        vax = request.form['service_vax_type']
    except:
        vax = ''
    data: dict = {
        'pet_owner': uuid_data[request.form['pet_owner']],
        'pet_id': request.form['pet_id'],
        'service_code': request.form['service_code'],
        'date': request.form['schedule_date'],
        'venue': request.form['venue'],
        'vax_type': vax
    }
    scheduleService(data)
    return render_template("InquirySent.html", account=request.form['pet_owner'])


@app.route("/pets/")
def pets_invalid():
    return redirect(url_for("login"))


@app.route('/pets/<account>')
def pets(account):
    if account == session['username']:
        data = getPets(account)
        inquiry = getPendingSchedules()
        for x in data:
            for y in inquiry:
                if x['pet_id'] == y['pet_id']:
                    x['inquiry'] = x['pet_id']
        return render_template("Pets.html", account=account, pets=data)
    return redirect(url_for("login"))


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/admin_register")
def admin_register():
    return render_template("registration_admin.html")


@app.route("/inquiry/<account>/<pet_id>")
def inquiries(account: str, pet_id: int):
    pet_data: list = []
    server_data = getPendingSchedules()
    for data in server_data:
        if int(data['pet_id']) == int(pet_id):
            for s_c in getServices():
                if data['service_code'] == s_c['service_code']:
                    data['service_code'] = s_c['description']
                    new_data: dict = {
                        'service_code': data['service_code'],
                        'date': data['date'],
                        'venue': data['venue'],
                        'status': data['status'],
                    }
                    pet_data.append(new_data)
                    print(data)

    return render_template('PetInquiry.html', account=account, pet_data=pet_data)


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


@app.route("/employee/logout/<account>")
def logout_employee(account):
    if account in uuid_data[session['username']]:
        print("logged out " + uuid_data[session['username']])
        employeeActivity(
            account,
            "",
            datetime.now().strftime("%H:%M:%S"),
            date.today().strftime("%Y-%m-%d"),
            "Account Logout"
        )
        uuid_data[session['username']] = {}
        session.clear()
        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("not_found"))


@app.route("/logout/")
def logout_invalid():
    return redirect(url_for("homepage"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
