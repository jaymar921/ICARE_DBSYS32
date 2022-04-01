from database import createAccount
from utility import generateUUID, hashData
from ProjectFiles.Entity.Entity import Account,LoginCredentials


# Run test
def sample_account():
    account: Account = Account(
        str(generateUUID()+""),
        "Barro",
        "Gladys",
        "2000-01-01",
        "123",
        "Cebu",
        "Cebu",
        "Cebu",
        "6000",
        "2022-04-01"
    )
    loginCred: LoginCredentials = LoginCredentials(
        6,
        account.acc_id,
        "Glady544",
        hashData("#h3ll0_123"),
        "glady@testemail.com",
        "09123123456"
    )
    print(account)
    print(loginCred)
    createAccount(account, loginCred)


if __name__ == '__main__':
    sample_account()
