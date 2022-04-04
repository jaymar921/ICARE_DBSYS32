import random
import uuid
import hashlib
from Entity.Entity import Account, LoginCredentials, Employee, Pet
from datetime import date


def get_configuration() -> dict:
    configuration: dict = {}
    data: list = []
    file = open("configuration.ini")

    for line in file:
        data.append(line.split(":")[1].strip(" \n\""))

    configuration["host"] = data[0]
    configuration["database"] = data[1]
    configuration["user"] = data[2]
    configuration["password"] = data[3]

    return configuration


def generateUUID() -> str:
    UUID: str = str(uuid.uuid4().hex)
    return UUID[0:30]


def hashData(data: str) -> str:
    result = hashlib.md5(data.encode()).hexdigest()
    return str(result)[0:30]


def parseNewAccount(data: dict, account_id: int) -> list:
    account: Account = Account(
        generateUUID(),
        data["lastname"],
        data["firstname"],
        data["birthdate"],
        data["house_no"],
        data["street"],
        data["barangay"],
        data["city"],
        data["zip"],
        str(date.today())
    )
    loginCred: LoginCredentials = LoginCredentials(
        login_id=account_id,
        acc_id=account.acc_id,
        username=data["username"],
        password=hashData(data["password"]),
        email=data["email"],
        contact=data["contact"]
    )
    return [account, loginCred]


def parseNewEmployeeAccount(data: dict, account_id: int) -> list:
    account: Employee = Employee(
        generateUUID(),
        data["lastname"],
        data["firstname"],
        data["birthdate"],
        data["house_no"],
        data["street"],
        data["barangay"],
        data["city"],
        data["zip"],
        str(date.today()),
        generateUUID(),
        data['position']
    )
    loginCred: LoginCredentials = LoginCredentials(
        login_id=account_id,
        acc_id=account.acc_id,
        username=data["username"],
        password=hashData(data["password"]),
        email=data["email"],
        contact=data["contact"]
    )
    return [account, loginCred]


def isEmail(username: str) -> bool:
    return len(username.split("@")) == 2 and len(username.split(".")) == 2


def parsePet(data: dict) -> Pet:
    pet: Pet = Pet(
        random.randint(0, 9999999),
        data['owner_id'],
        data['name'],
        data['age'],
        data['gender'],
        data['breed'],
        data['specie'],
        data['bloodtype'],
        data['weight'],
        date.today(),
        "OK"
    )
    return pet
