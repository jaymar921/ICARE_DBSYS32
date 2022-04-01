import uuid
import hashlib


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
