import requests
from bs4 import BeautifulSoup
import random
import base64

#todo
#! TODO : 1. 로그인 회원가입 절차 확인
#! TODO : 1-2. Emperor 회원 가입 불가 확인
#TODO : 2. 인코딩 서비스 무결성, 가용성 확인
#TODO : 3. 로그아웃 절차 확인
#TODO : 4. Emperor 계정 확인
#TODO : 5. 


def encode_base64(data):
	# bytes = data.encode('ascii')
	bytes = data.encode('utf-8')
	encoded = base64.b64encode(bytes)
	result = encoded.decode('ascii')
	return result

check_url = "http://localhost:4242"

user = {
    'username' : "SLA" + str(random.randint(1, 100000)),
    'password' : "SLA" + str(random.randint(1, 100000))
}

# 로그인 회원가입 절차 확인
try:
	register = requests.post(check_url + "/register", data=user)
	session = requests.Session()
	login = session.post(check_url + "/login", data=user)
except:
	print("register or login process failed")
	exit()

# 로그인 성공 여부, 계정명 같은 지 확인
response = session.get(check_url + "/about")

soup = BeautifulSoup(response.text, 'html.parser')

username_check = soup.find(
	'h4', {'class': 'card-title'}).strong.text

if username_check.split(" ")[3] != user['username']:
	print("is not same username")
	exit()

#TODO : 1-2. Emperor 회원 가입 불가 확인
flag = open("../flag.txt", "r").read()
emperor = {
	'username' : "emperor",
	'password' : flag
}

register = requests.post(check_url + "/register", data=emperor)
soup = BeautifulSoup(register.text, 'html.parser')
register_check = soup.find(
	'script')
if register_check == None:
	print("Emperor 회원 가입 가능")
	exit()

#잘못된 Emperor 계정으로 로그인 시도 확인
emperor["password"] = random.randint(1, 100000)
login = session.post(check_url + "/login", data=emperor)
soup = BeautifulSoup(login.text, 'html.parser')
mis_emperor_login = soup.find('script').text.strip()
if mis_emperor_login != "alert(\"Login failed, check your username or password\");":
	print("잘못된 Emperor 계정 로그인 가능")
	exit()

#TODO : 2. 인코딩 서비스 무결성, 가용성 확인
# login
session = requests.Session()
login = session.post(check_url + "/login", data=user)

for i in range(1):
	#random string 생성
	random_string = str(random.randint(1, 10000000000))
	# request
	target_url = "http://localhost:4242/service_post"
	data = {'content': random_string}
	cookies = session.cookies.get_dict()
	response = requests.post(target_url, data=data, cookies=cookies)
	data = response.text
	print(data)
