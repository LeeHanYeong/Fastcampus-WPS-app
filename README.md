# Fastcampus Web Progamming School Applications

Fastcampus 웹 프로그래밍 스쿨의 실습 애플리케이션입니다.  
sqlite3 DB를 사용합니다.

---

## Structure

- django_app : Django project container폴더
	- fastcampus : settings.py가 있는 프로젝트 폴더
	- projects : 실습 프로젝트를 모아놓은 모듈
		- **blog** : 블로그 프로젝트
		- **video** : Youtube API 프로젝트
		- **sns** : Facebook API 프로젝트

---

## Installation

#### Homebrew
macOS 사용자는 [Homebrew를 설치해주세요](http://brew.sh)

-

### pyenv

파이썬 버전 및 가상환경 관리자인 [pyenv](https://github.com/yyuu/pyenv)를 설치해야합니다.
macOS 및 Ubuntu에서 각각 관련 라이브러리를 설치한 후에 pyenv를 설치해야 합니다.
[Common build problems](https://github.com/yyuu/pyenv/wiki/Common-build-problems)  
[Linux auto installer](https://github.com/yyuu/pyenv-installer)

**macOS:**

```
brew install readline xz
brew install pyenv
```

아래 내용을 shell 설정파일에 적어줍니다.

```
export PYENV_ROOT=/usr/local/var/pyenv
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
```

**Ubuntu:**

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

아래 내용을 shell 설정파일에 적어줍니다.

```
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

-

#### PostrgreSQL

본 프로젝트에서는 PostgreSQL을 사용하고 있지 않지만, DB를 교체할경우를 생각하여 미리 패키지를 설치해줍니다.

**Ubuntu:**

```
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
```

-

#### Pillow

Python이미지 라이브러리인 Pillow가 필요합니다.
macOS와 Ubuntu에서 각각 관련 라이브러리를 설치한 후에 Pillow를 설치해야 합니다.

**macOS:**

```
brew install libtiff libjpeg webp little-cms2
pip install Pillow
```


**Ubuntu14.04 LTS**  

```
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
pip install Pillow
```

위의 내용은 바뀔 수 있습니다. [Pillow 공식 설치방법](https://pillow.readthedocs.io/en/3.4.x/installation.html#basic-installation)

-

#### .conf폴더 추가

`settings.py`파일에서 두 파일의 내용을 참조합니다.  
로컬에서 `runserver`명령어로 테스트시, 배포용 설정파일은 필요하지 않습니다.  
디버그용 설정파일 : `django_app/.conf/settings_debug.json`  
배포용 설정파일 : `django_app/.conf/settings_deploy.json`

아래와 같이 작성한 후, `django_app`폴더 아래에 `.conf`폴더를 생성 후 `settings_debug.json`이라는 이름으로 저장해줍니다.  

```javascript
{
  "email": {
    "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
    "EMAIL_HOST": "smtp.gmail.com",
    "EMAIL_PORT": "587",
    "EMAIL_HOST_USER": <Gmail account>,
    "EMAIL_HOST_PASSWORD": <Gmail account password>,
    "EMAIL_USE_TLS": true
  },
  "facebook": {
    "FACEBOOK_APP_ID": <Facebook app id>,
    "FACEBOOK_SECRET_CODE": <Facebook secret code>
  },
  "allowedHosts": [
    ".<domain name>",
    ".amazonaws.com",
    ".elasticbeanstalk.com"
  ]
}
```
-

#### Install pre-requirements

필요한 Python패키지들을 설치해줍니다.

```
pip install -r requirements.txt
```

-

## Django runserver

```python
python manage.py runserver
```