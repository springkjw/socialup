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
    
- Deploy
    1. AWS 계정
    > `ID` : `snssnsking@gmail.com`
      `PW` : `wodnjs2010Dbwls1804`
        
    2. Setup Virtual Environment
    ```bash
    source bin/activate
    pip install -r requirements
    ```
     
    3. IAM setting
    `~/.aws/config` 파일에 추가
    
    ```bash
    [profile socialup-cli]
    aws_access_key_id = AKIAIQD2UOWVAZSG4SAQ
    aws_secret_access_key = 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
    ```
        
    4. EB CLI setting
    
    ```bash
    eb init
    ```
    ```bash
    Select a default region
    10) cn-north-1 : China (Beiging)
    (default is 3) : 
    # select seoul region
    ```
    ```bash
    (aws-access-id): <your access_key_id>
    (aws-secret_key): <your secret_access_key>
    ```
    ```bash
    Select an application to use
    1) Socialup
    # select socialup application
    ```
    
    5. Setup EB Extension:
    - Create new folter called `.extensions` in the root of your virtualenv where the `.elasticbeanstalk` directory.
    - Add new file called `01_awsbean.config` in `.ebextensions` with contents of :
    ```roboconf
    option_settings:
        option_settings:
        "aws:elasticbeanstalk:application:environment":
            DJANGO_SETTINGS_MODULE: "socialup.settings"
            PYTHONPATH: "/opt/python/current/app/src:$PYTHONPATH"
        "aws:elasticbeanstalk:container:python":
            WSGIPath: "socialup/wsgi.py"
    ```
    - Add new file called `02_packages.config` in `.ebextensions` with conteht of
    ```roboconf
    packages:
        yum:
            git: []
            libtiff-devel: []
            libjpeg-turbo-devel: []
            libzip-devel: []
            freetype-devel: []
            lcms2-devel: []
            libwebp-devel: []
            tcl-devel: []
    ```
    - Add new file called `03_python.config` in `.ebextensions` with conteht of
    ```roboconf
    container_commands:
        01_migrate:
            command: "python manage.py makemigrations --noinput"
            command: "python manage.py migrate --noinput"
            leader_only: true
        02_makesuper:
            command: "python manage.py makesuper"
            leader_only: true
        03_collectstatic:
            command: "python manage.py collectstatic --noinput"
            leader_only: true
        04_http_to_https_redirect:
            command:
                sed -i '/\<VirtualHost \*:80\>/a RewriteEngine On\nRewriteCond %{HTTP:X-Forwarded-Proto} !https\nRewriteRule \!/robots.txt https://%{SERVER_NAME}%{REQUEST_URI} [L,R=301]' /opt/python/ondeck/wsgi.conf
    ```
    - Add new file called `elasticbeanstalk.config` in `.ebextensions` with conteht of
    ```roboconf
    <VirtualHost *:80>
      <Proxy *>
        Order deny,allow
        Allow from all
      </Proxy>
    
      ProxyPass / http://localhost:8000/ retry=0
      ProxyPassReverse / http://localhost:8000/
      ProxyPreserveHost on
    
      RewriteEngine On
      RewriteCond %{HTTP:X-Forwarded-Proto} !https
      RewriteRule !/status https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
    
      LogFormat "%h (%{X-Forwarded-For}i) %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
      ErrorLog /var/log/httpd/elasticbeanstalk-error_log
      TransferLog /var/log/httpd/elasticbeanstalk-access_log
    </VirtualHost>
    ```
    
    5. deploy
    commit git and deploy
    ```bash
    git add .
    git commit -m "test"
    ```
    
    ```bash
    eb deploy
    ```
        
        
    
    