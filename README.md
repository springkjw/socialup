# socialup

에디터 : pycharm 추천 (sublime text 또는 atom도 무방)

- Django 설정
    1. virtualenv(가상환경) 설치
    ```bash
    sudo pip3 install virtualenv
    virtualenv venv
    ```
    
    ```bash
    $ source venv/bin/activate
    ```

    2. Django & 라이브러리 설치
    
    ```bash
    $ sudo pip install -r requirements.txt
    ```

    3. Run Server
    ```bash
    $ python manage.py migrate
    $ python manage.py runserver
    ```

    4. localhost:8000 접속
    5. 관리자 계정 생성
    ```bash
    $ python manage.py createsuperuser
    ```
    
    localhost:8000/admin 으로 관리자 페이지 접속