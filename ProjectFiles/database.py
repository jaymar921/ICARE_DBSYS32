from mysql import connector
import utility
from Entity import Entity

# connect to the database
database = connector.connect(
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
        cursor = database.cursor()
        cursor.execute(sql)
        database.commit()
        cursor.close()
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
    cursor = database.cursor()
    cursor.execute(sql)
    database.commit()
    cursor.close()
