import threading
import time

from mysql import connector
import utility
from ProjectFiles.Entity.Entity import LoginCredentials, Account
from Entity import Entity


# connect to the database
def database() -> connector:
    return connector.connect(
        host=utility.get_configuration()["host"],
        user=utility.get_configuration()["user"],
        password=utility.get_configuration()["password"],
        database=utility.get_configuration()["database"]
    )


def createAccount(account: Entity.Account, login_credential: Entity.LoginCredentials):
    try:
        acc_id: str = account.acc_id
        sql: str = f"INSERT INTO `account` (" \
                   f"`acc_id`," \
                   f"`lastname`," \
                   f"`firstname`,`" \
                   f"birthdate`,`" \
                   f"house_no`," \
                   f"`street`," \
                   f"`barangay`," \
                   f"`city`," \
                   f"`zip`," \
                   f"`registry_date`) VALUES(" \
                   f"'{acc_id}'," \
                   f"'{account.lastname}'," \
                   f"'{account.firstname}'," \
                   f"'{account.birthdate}'," \
                   f"'{account.house_no}'," \
                   f"'{account.street}'," \
                   f"'{account.barangay}'," \
                   f"'{account.city}'," \
                   f"'{account.zip}'," \
                   f"'{account.registry_date}');"
        db = database()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close
        registerCredentials(login_credential)
    except Exception as e:
        print(e)


def registerCredentials(login_credential: Entity.LoginCredentials):
    sql: str = f"insert into `login_credentials` (" \
               f"`login_id`," \
               f"`acc_id`," \
               f"`username`," \
               f"`password`," \
               f"`email`," \
               f"`contact_no`) values (" \
               f"'{login_credential.login_id}'," \
               f"'{login_credential.acc_id}'," \
               f"'{login_credential.username}'," \
               f"'{login_credential.password}'," \
               f"'{login_credential.email}'," \
               f"'{login_credential.contact}')"
    db = database()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def generateAccountID() -> int:
    sql: str = f"select * from `login_credentials`"
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data: list = cursor.fetchall()
    data = data[len(data) - 1]
    cursor.close()
    db.close()
    return data['login_id'] + 1


def generateRecordID() -> int:
    try:
        sql: str = f"select * from `service_records`"
        db = database()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        data: list = cursor.fetchall()
        data = data[len(data) - 1]
        cursor.close()
        db.close()
        return data['record_id'] + 1
    except Exception:
        return 1


def generateTransactionID() -> int:
    try:
        sql: str = f"select * from `transaction`"
        db = database()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        data: list = cursor.fetchall()
        data = data[len(data) - 1]
        cursor.close()
        db.close()
        return data['transact_id'] + 1
    except Exception:
        return 1


def createEmployee(account: Entity.Employee, login_cred: Entity.LoginCredentials):
    try:
        acc_id: str = account.acc_id
        sql: str = f"INSERT INTO `account` (" \
                   f"`acc_id`," \
                   f"`lastname`," \
                   f"`firstname`,`" \
                   f"birthdate`,`" \
                   f"house_no`," \
                   f"`street`," \
                   f"`barangay`," \
                   f"`city`," \
                   f"`zip`," \
                   f"`registry_date`) VALUES(" \
                   f"'{acc_id}'," \
                   f"'{account.lastname}'," \
                   f"'{account.firstname}'," \
                   f"'{account.birthdate}'," \
                   f"'{account.house_no}'," \
                   f"'{account.street}'," \
                   f"'{account.barangay}'," \
                   f"'{account.city}'," \
                   f"'{account.zip}'," \
                   f"'{account.registry_date}');"
        db = database()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        registerCredentials(login_cred)
        createEmployeeAccount(account)
    except Exception as e:
        print(e)


def createEmployeeAccount(account: Entity.Employee):
    sql: str = f"insert into `employee` (`emp_id`,`acc_id`,`position`) values ('{account.emp_id}','{account.acc_id}','{account.position}')"
    db = database()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def loginAccount(username: str, password: str, is_email: bool = False) -> list:
    if is_email:
        sql = f"select * from `login_credentials` where email='{username}' and password='{password}'"
    else:
        sql = f"select * from `login_credentials` where username='{username}' and password='{password}'"
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data: list = cursor.fetchall()
    cursor.close()
    if len(data) != 0:
        loginCred: LoginCredentials = LoginCredentials(
            login_id=data[0]['login_id'],
            acc_id=data[0]['acc_id'],
            username=data[0]['username'],
            password=data[0]['password'],
            email=data[0]['email'],
            contact=data[0]['contact_no']
        )
        sql: str = f"select * from `account` where acc_id='{loginCred.acc_id}'"
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        data: dict = cursor.fetchall()
        cursor.close()
        account: Account = Account(
            data[0]["acc_id"],
            data[0]["lastname"],
            data[0]["firstname"],
            data[0]["birthdate"],
            data[0]["house_no"],
            data[0]["street"],
            data[0]["barangay"],
            data[0]["city"],
            data[0]["zip"],
            data[0]["registry_date"]
        )
        sql: str = f"select * from `employee` where acc_id='{loginCred.acc_id}'"
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        data: dict = cursor.fetchall()
        cursor.close()
        if len(data) != 0:
            employee: Entity.Employee = Entity.Employee(
                account.acc_id,
                account.lastname,
                account.firstname,
                account.birthdate,
                account.house_no,
                account.street,
                account.barangay,
                account.city,
                account.zip,
                account.registry_date,
                data[0]['emp_id'],
                data[0]['position'],
            )
            db.close()
            return [account, loginCred, employee]
        db.close()
        return [account, loginCred]
    db.close()
    return []


def registerPet(pet: Entity.Pet):
    sql: str = f"insert into `pet` (`pet_id`,`owner_id`,`name`,`age`,`gender`,`breed`,`specie`,`blood_type`,`weight`," \
               f"`registry_date`,`status`) values" \
               f"(" \
               f"'{pet.pet_id}'," \
               f"'{pet.owner_id}'," \
               f"'{pet.name}'," \
               f"'{pet.age}'," \
               f"'{pet.gender}'," \
               f"'{pet.breed}'," \
               f"'{pet.specie}'," \
               f"'{pet.blood_type}'," \
               f"'{pet.weight}'," \
               f"'{pet.registry_date}'," \
               f"'{pet.status}'" \
               f")"
    db = database()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def getPets(username: str) -> list:
    sql: str = f"select `name`,`age`,`gender`,`breed`,`specie`,`blood_type`,`weight`," \
               f"`registry_date`,`status`,`pet_id` from `pet` " \
               f"p, `login_credentials` l where l.username = '{username}' and p.owner_id = l.acc_id and status='OK'; "
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def getServices() -> list:
    sql: str = "select * from service"
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    print(data)
    return data


def scheduleService(data: dict):
    print(data['vax_type'])
    sql: str = f"insert into `service_records` (`record_id`,`pet_id`,`service_code`,`date`,`venue`,`status`,`remarks`) values ('{generateRecordID()}','{data['pet_id']}','{data['service_code']}','{data['date']}','{data['venue']}','PENDING','{data['vax_type']}');"
    db = database()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def getPendingSchedules() -> list:
    sql: str = "select * from `service_records`;"
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data: list = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def getAdminPendingSchedules() -> list:
    sql: str = "select record_id, p.pet_id, owner_id, description as service, date, venue, s.status, s.remarks from service_records s, pet p, service where p.pet_id = s.pet_id and s.service_code = service.service_code and s.status = 'PENDING';"
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data: list = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def employeeActivity(e_id: str, log_in: str, log_out: str, today: str, interaction: str):
    print([e_id, log_in, log_out, today, interaction])
    db = database()
    cursor = db.cursor()
    sql: str = f"insert into employee_activity values ('NULL','{e_id}','{log_in}','{log_out}','{today}','{interaction}');"
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def getAdminApprovedDeclinedSchedules() -> list:
    sql: str = "select sr.record_id, sr.pet_id, p.owner_id, s.description as service, sr.date, sr.venue, sr.status from service_records sr, pet p,service s where p.pet_id = sr.pet_id and s.service_code = sr.service_code and sr.remarks='CHECKED';"
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data: list = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def updateAdminPendingSchedules(data: dict):
    sql: str = f"update service_records set status='{data['remark']}', remarks='CHECKED' where record_id='{data['record_id']}'; "
    db = database()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def addTransactions(data: dict):
    transact_id: int = generateTransactionID()
    sql: str = f"update service_records set status='{data['remark']}', remarks='{transact_id}' where record_id='{data['record_id']}'; "
    db = database()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    for service in getServices():
        if str(service['description']) == str(data['service']):
            data['price'] = service['price']
    sql: str = f"insert into `transaction` (`transact_id`,`acc_id`,`amount`,`status`) values ({transact_id},'{data['pet_owner']}','{data['price']}','{data['remark']}');"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def getClients() -> list:
    sql: str = "select a.acc_id as UUID, lastname, firstname, birthdate, house_no, street, barangay, city, zip, " \
               "registry_date, case when a.acc_id = e.acc_id then 'YES' else '' end as ADMIN from account a, " \
               "employee e; "
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def getTransactions() -> list:
    sql: str = "select t.transact_id,a.lastname,a.firstname,p.name,s.description,t.amount,t.status from transaction t, account a, pet p, service s, service_records sr where t.acc_id = a.acc_id and p.owner_id = t.acc_id and sr.service_code = s.service_code and p.pet_id = sr.pet_id and sr.remarks = t.transact_id order by t.transact_id asc;"
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data
