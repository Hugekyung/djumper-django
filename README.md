# djumper-django
본 저장소는 E-commerce 웹 서비스 Djumper의 Backend 관련 코드입니다.<br> 
--> [Frontend 이동](https://github.com/Hugekyung/djumper-vue)<br><br/>
### Overview
---
프로젝트의 목적은 백엔드에서 구현한 API를 프론트엔드에서 어떻게 활용하는지, 백-프론트 사이의 통신 방법과 비동기 처리 방식을 비롯한 전체 웹 서비스 구축 프로세스를 경험하기 위함입니다.<br><br/>

#### Environment
```
OS                            Version
----------------------------- ---------
Ubuntu                        20.04 LTS(WSL)

Package                       Version  
----------------------------- ---------
              [Back-end]
Django                        3.2.6
django-cors-headers           3.8.0                
djangorestframework   
Pillow       
djoser

              [Front-end]
vue(with cli)
axios
bulma
```
<br><br/>

### Usage(Back)
---
```
// 1. Python 가상환경 생성
$ sudo apt-get update
$ sudo apt-get install python3-venv
$ (프로젝트 폴더 내에서)python3 -m venv myvenv

// 2. 가상환경 내에서 Django 및 라이브러리 설치
$ source myvenv/bin/activate
$ pip install -r requirements.txt

// 3. Django server 실행(개발용)
$ python manage.py runserver
```

#### Django settings
```
# settings.py

# ENV 설정 ----------------------------------------------

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

# 결제 API 정보
KAKAO_ADMIN_KEY = env('KAKAKAO_ADMIN_KEY')

앱과 CORS 설정 -------------------------------------------

INSTALLED_APPS = [
	...,
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    ...,
]
```

<br><br/>

### ERD
---
images
