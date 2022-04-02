# iCARE [IMDBSYS32]
> Group Members
- Abejar, Jayharron Mar (Leader)
- Barro, Gladys
- Elim, Daisy May
- Ministerio, Jemaica
- Quirante, Yrrech Gerson
## Database: icare_dbsys32
```sql
create database icare_dbsys32;
```
## ACCOUNT
```sql
create table account(acc_id varchar(30) primary key, lastname varchar(30) not null, firstname varchar(30) not null, birthdate date not null, house_no varchar(5), street varchar(30) not null, barangay varchar(30) not null, city varchar(30) not null, zip varchar(6) not null, registry_date date not null) engine=innodb;
```
- ACC_ID: VARCHAR(30) PRIMARY KEY
- LASTNAME: VARCHAR(30)
- FIRSTNAME: VARCHAR(30)
- BIRTHDATE: DATE
- HOUSE_NO: VARCHAR(5) NULL
- STREET: VARCHAR(30)
- BARANGAY: VARCHAR(30)
- CITY: VARCHAR (30)
- ZIP: VARCHAR(6)
- REGISTRY_DATE: DATE
## EMPLOYEE
```sql
create table employee(emp_id varchar(30) primary key, acc_id varchar(30), position varchar(30) not null, foreign key(acc_id) references account(acc_id) on delete restrict on update restrict)  engine = innodb;
```
- EMP_ID: VARCHAR(30) PRIMARY KEY
- ACC_ID: VARCHAR(30) FOREIGN KEY REFERENCES account(ACC_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
- POSITION: VARCHAR(30)
## LOGIN_CREDENTIALS
```sql
create table login_credentials(login_id int(11) primary key,acc_id varchar(30) not null, foreign key(acc_id) references account(acc_id) on delete restrict on update restrict, username varchar(30) not null, password varchar(30) not null, email varchar(30) not null, contact_no varchar(11)) engine = innodb;
```
- LOGIN_ID: INT PRIMARY KEY
- ACC_ID: VARCHAR(30) FOREIGN KEY REFERENCES account(ACC_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
- USERNAME: VARCHAR(30)
- PASSWORD: VARCHAR(30)
- EMAIL: VARCHAR(50)
- CONTACT_NO: VARCHAR(11) NULL
## PET
```sql
create table pet(pet_id int(11) primary key, owner_id varchar(30) not null, name varchar(30) not null, age int(2) not null, gender varchar(1) not null, breed varchar(30) not null, specie varchar(30) not null, blood_type varchar(3), weight decimal(5,2), registry_date date not null, status varchar(10) not null, foreign key(owner_id) references account(acc_id) on delete restrict on update restrict) engine = innodb;
```
- PET_ID: INT PRIMARY KEY
- OWNER_ID: VARCHAR(30) FOREIGN KEY REFERENCES account(ACC_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
- NAME: VARCHAR(20)
- AGE: INT(2)
- GENDER: VARCHAR(1)
- BREED: VARCHAR(30)
- SPECIE: VARCHAR(30)
- BLOOD_TYPE: VARCHAR(3) NULL
- WEIGHT: DECIMAL(5,2) NULL
- REGISTRY_DATE: DATE
- STATUS: VARCHAR(10)
## SERVICE
```sql
create table service(service_code varchar(2) primary key, description varchar(100) not null, price decimal(10,2) not null) engine = innodb;
```
- SERVICE_CODE: VARCHAR(2) PRIMARY KEY
- DESCRIPTION: VARCHAR(100)
- PRICE: DECIMAL(10,2)
## SERVICE_RECORDS
```sql
create table service_records(record_id int(11) primary key, pet_id int not null, service_code varchar(2) not null, date date not null, venue varchar(50) not null, status varchar(30) not null, remarks varchar(100) not null, foreign key(pet_id) references pet(pet_id) on delete restrict on update restrict, foreign key(service_code) references service(service_code) on delete restrict on update restrict) engine = innodb;
```
- RECORD_ID: INT(11) PRIMARY KEY
- PET_ID: INT FOREIGN KEY REFERENCES pet(PET_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
- SERVICE_CODE: VARCHAR(2) FOREIGN KEY REFERENCES service(SERVICE_CODE) ON DELETE RESTRICT ON UPDATE RESTRICT
- DATE: DATE
- VENUE: VARCHAR(50)
- STATUS: VARCHAR(30)
- REMARKS: VARCHAR(100)
## TRANSACTION
```sql
create table transaction(transact_id int(11) primary key, acc_id varchar(30) not null, amount decimal(10,2) not null, status varchar(15) not null, foreign key(acc_id) references account(acc_id) on delete restrict on update restrict) engine = innodb;
```
- TRANSACT_ID: INT(11) PRIMARY KEY
- ACC_ID: VARCHAR(30) FOREIGN KEY REFERENCES account(ACC_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
- AMOUNT: DECIMAL(10,2)
- STATUS: VARCHAR(15)
## ACTIVITY_RECORD
```sql
create table activity_record(transact_id int(11) not null, record_id int(11) not null, foreign key(transact_id) references transaction(transact_id), foreign key(record_id) references service_records(record_id)) engine = innodb;
```
- TRANSACT_ID: INT(11) FOREIGN KEY REFERENCES transaction(TRANSACT_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
- RECORD_ID: INT(11) FOREIGN KEY REFERENCES service_records(RECORD_ID) ON DELETE RESTRICT ON UPDATE RESTRICT
## EMPLOYEE_ACTIVITY
```sql
create table employee_activity(activity_code varchar(30) primary key, emp_id varchar(30) not null, login_time time not null, logout_time time not null, date date not null, interaction varchar(100) not null, foreign key(emp_id) references employee(emp_id) on delete restrict on update restrict) engine = innodb;
```
- ACTIVITY_CODE: VARCHAR(30) PRIMARY KEY
- EMP_ID: VARCHAR(30) FOREIGN KEY REFERENCES employee(EMP_ID)
- LOGIN_TIME: TIME
- LOGOUT_TIME: TIME
- DATE: DATE
- INTERACTION: VARCHAR(100)
## Describe all tables
```sql
use icare_dbsys32;
describe account;
describe employee;
describe login_credentials;
describe pet;
describe service;
describe service_records;
describe transaction;
describe activity_record;
describe employee_activity;
```
## Show all entities from tables
```sql
select * from account;
select * from employee;
select * from login_credentials;
select * from pets;
select * from service;
select * from service_records;
select * from transaction;
select * from activity_record;
select * from employee_activity;
```
