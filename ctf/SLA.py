import requests
from bs4 import BeautifulSoup
import random
import base64
import time

#todo
#! TODO : 1. 로그인 회원가입 절차 확인
#! TODO : 1-2. Emperor 회원 가입 불가 확인
#TODO : 2. 인코딩 서비스 무결성, 가용성 확인
#TODO : 3. 로그아웃 절차 확인
#TODO : 4. Emperor 계정 확인
#TODO : 5. Emperor page 접속 확인
#TODO : 5-2. Emperor page에서 추가한 유저 정보 일치 여부 확인
#TODO : 5-3. 추가한 유저, 작성 글 삭제 여부 확인
#TODO : 5-4. flag qr 코드 확인


def encode_base64(data):
	bytes = data.encode('utf-8')
	encoded = base64.b64encode(bytes)
	result = encoded.decode('ascii')
	return result

check_url = "http://localhost:4242"

user = {
    'username' : "SLA" + str(random.randint(1, 100000)),
    'password' : "SLA" + str(random.randint(1, 100000))
}

flag = open("../flag.txt", "r").read()
emperor = {
	'username': "emperor",
	'password': flag
}
print(emperor['password'])

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
# print(login.text)

for i in range(3):
	#random string 생성
	random_string = str(random.randint(1, 10000000000))
	result = encode_base64(random_string)
	# request
	data = {'content': random_string}
	cookies = session.cookies.get_dict()
	# 시간 측정
	start = time.time()
	response = requests.post(check_url + "/service_post", data=data, cookies=cookies)
	end = time.time()
	elapse = end - start
	data = response.text
	soup = BeautifulSoup(data, 'html.parser')
	# media-body인 모든 요소를 가져옴
	text = soup.find_all('div', {'class': 'media-body'})
	# print(plain)
	if i == 0:
		plain_text = text[1].text.strip()
		encode_text = text[2].text.strip()
	else:
		plain_text = text[2 * i].text.strip()
		encode_text = text[2 * i + 1].text.strip()
	if plain_text != random_string:
		print("plain_text is not same random_string")
		exit()
	if encode_text != result:
		print("encode_text is not same result")
		exit()
	if elapse > 0.5:
		print("elapse time is too long")
		exit()

#TODO : 3. 로그아웃 절차 확인
logout = session.get(check_url + "/logout")
# 쿠키 확인
cookies = session.cookies.get_dict()
if cookies != {}:
	print("logout failed")
	exit()

#TODO : 4. Emperor 계정 확인
# login
emperor["password"] = flag
session = requests.Session()
login = session.post(check_url + "/login", data=emperor)
cookies = session.cookies.get_dict()
if cookies == {}:
	print("login failed")
	exit()

# emperor 페이지 확인
connect_emperor = session.get(check_url + "/emperor")
# print(connect_emperor.text)
soup = BeautifulSoup(connect_emperor.text, 'html.parser')
# td
emperor_check = soup.find_all('td')
id = emperor_check[0].text.strip()
pw = emperor_check[1].text.strip()
if id != user['username']:
	print("emperor page incorrect runnig")
	exit()
if pw != user['password']:
	print("emperor page incorrect runnig")
	exit()


# about 페이지 확인
# response = session.get(check_url + "/about")