# socialup

- Django 설정
    1. virtualenv(가상환경) 설치
    
    > `sudo pip3 install virtualenv`
    
    > `virtualenv venv`
    
    > `source venv/bin/activate`

    2. Django & 라이브러리 설치
    
    > `sudo pip install -r requirements.txt`

    3. Run Server
    
    > `cd server`
    
    > `python manage.py migrate`
    
    > `python manage.py runserver`

    4. localhost:8000 접속