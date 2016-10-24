# Fastcampus Web Progamming School Applications

Fastcampus 웹 프로그래밍 스쿨의 실습 애플리케이션입니다.  
sqlite3 DB를 사용합니다.

---

## Installation

#### Homebrew
macOS 사용자는 [Homebrew를 설치해주세요](http://brew.sh)

-

### pyenv

파이썬 버전 및 가상환경 관리자인 [pyenv](https://github.com/yyuu/pyenv)를 설치해야합니다
macOS 및 Ubuntu에서 각각 관련 라이브러리를 설치한 후에 pyenv를 설치해야 합니다.
[Common build problems](https://github.com/yyuu/pyenv/wiki/Common-build-problems)  
[Linux auto installer](https://github.com/yyuu/pyenv-installer)

**macOS:**

```
brew install readline xz
brew install pyenv
```

아래 내용을 shell 설정파일에 적어줍니다

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

아래 내용을 shell 설정파일에 적어줍니다

```
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
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

위의 내용은 바뀔 수 있습니다 [Pillow 공식 설치방법](https://pillow.readthedocs.io/en/3.4.x/installation.html#basic-installation)

-

#### Install pre-requirements

필요한 Python패키지들을 설치해줍니다.

```
pip install -r requirements.txt
```
