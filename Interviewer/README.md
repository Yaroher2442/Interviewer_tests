# INTERVIEWER
## Django interview system

Here is a short description

Programing languages
- Python (Django)
- Html5, css (bootstrap)
- Javascript (jQuery)

# Features

- Create/edit/delite TEST for interviewing users
- Create/delite Questions for TESTs
- For User : Answering to questions and see answers after

# Installation
## First we need a virtual (or physical) machine on linux (!!!)
1. Update system
    1. `$sudo apt update; sudo apt upgrade `
2. Instal python, postgresql
    1. `$sudo apt-get install -y postgresql `
    2. `$sudo apt-get install -y python3 python3-pip python3-venv python-dev`
3. Configure Postgresql
    1. `$sudo su postgres `
    2. `$createuser testuser`
    3. `$createdb testdb `
    4. `$alter user testuser with encrypted password '<you_password>'; `
    5. `$grant all privileges on database testdb to testuser;`
4. Change host postgresql  
    1. `$sudo nano /etc/postgresql/<version>/main/pg_hba.conf`
    2. Change host to ```# IPv4 local connections: host all all 0.0.0.0/0 md5```
    3. `$sudo service postgresql restart`
5. Python-Django settings
    1. `$cd /home/<your name>`
    2. `$git clone https://github.com/Yaroher2442/Interviewer_tests`
    3. `$cd Interviewer_tests`
    4. `$python3 -m venv env `
    5. `$source env/bin/activate `
    6. `$cd Interviewer/`
    7. `$pip3 install -r requirements.txt`
    8. `$python3 manage.py migrate`
    9. `$python3 manage.py createsuperuser`
    10. follow console instructions
    11. `$/Interviewer_tests/Interviewer$ cd inter/ `
    12. Change django host `$ sudo nano settings.py `
    13. Change MY_IP on IP of your server like 192.168.0.0 (to find out your ip use ifconfig anywhere on the console)
    14. `$cd .. `
    15. `$python3 manage.py runserver 0.0.0.0:80000`
6. Testing in browser

 ## API (views)  
 BASIC_ip is <you_server_ip>:5000
1. For User 
    1.  BASIC_ip/register-register new usual user
    2.  BASIC_ip/login -register  usual user
    3.  BASIC_ip/logout -register  usual user
    4.  BASIC_ip/test/all -see all test in system user
    5.  BASIC_ip/test/user/ -branch tied on controller
        1.  BASIC_ip/test/user/<test_id> -to see answering form on test
        2.  BASIC_ip/test/user/show/<test_id> -to see already answered test
    6.  BASIC_ip/test/user/<test_id> -user use this for see information
2. For Admins (django superuser)
    1.  BASIC_ip/register-register new Admins
    2.  BASIC_ip/logout -register Admins
    3.  BASIC_ip/test/all -see all test in system Admins
    4.  BASIC_ip/test/create -create new test
    5.  BASIC_ip/test/edit/<test_id> -edit one test
    6.  BASIC_ip/test/delite/<test_id> -delite one test

### How test 
Now you need to take any other computer , open a browser.
If you need to test Admin part :  BASIC_ip/login and use django-seperuser creds.
If you need to test User part :  BASIC_ip/register and create usual user (after that auto-redirect to login).











