class Account:

    def __init__(self, acc_id: str, lastname: str, firstname: str, birthdate: str, house_no: str, street: str, barangay: str, city: str, zip: str, registry_date: str):
        self.acc_id = acc_id
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.house_no = house_no
        self.street = street
        self.barangay = barangay
        self.city = city
        self.zip = zip
        self.registry_date = registry_date

    def __str__(self) -> str:
        return self.acc_id + " " + self.firstname + " " + self.lastname


class Employee(Account):

    def __init__(self, acc_id: str, lastname: str, firstname: str, birthdate: str, house_no: str, street: str, barangay: str, city: str, zip: str, registry_date: str, emp_id: str, position: str):
        Account.__init__(self, acc_id, lastname, firstname, birthdate, house_no, street, barangay, city, zip, registry_date)
        self.emp_id = emp_id
        self.position = position


class LoginCredentials:

    def __init__(self, login_id: int, acc_id: str, username: str, password: str, email: str, contact: str):
        self.login_id = login_id
        self.acc_id = acc_id
        self.username = username
        self.password = password
        self.email = email
        self.contact = contact

    def __str__(self) -> str:
        return self.username + " " + self.password


class Pet:

    def __init__(self, pet_id: int, owner_id: str, name: str, age: int, gender: str, breed: str, specie: str, blood_type: str, weight: str, registry_date: str, status: str):
        self.pet_id = pet_id
        self.owner_id = owner_id
        self.name = name
        self.age = age
        self.gender = gender
        self.breed = breed
        self.specie = specie
        self.blood_type = blood_type
        self.weight = weight
        self.registry_date = registry_date
        self.status = status

    def __str__(self) -> str:
        return self.name + " " + self.breed
