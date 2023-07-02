from flask import Flask, render_template, render_template_string
from flask import request, session, flash, redirect, url_for
import os
from model import db, User, Post
from service import encode_base64, str_to_qrcode

app = Flask(__name__)


if not os.path.exists('flag.txt'):
	print('flag.txt not found!')
	exit(0)
else:
	with open('flag.txt', 'r') as f:
		flag = f.read()
	app.secret_key = str(flag)
	str_to_qrcode(app.secret_key)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(base_dir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SESSION_COOKIE_NAME'] = 'SF_SESSION'


@app.route('/')
def index():
	if session.get('username') is None:
		return render_template('login.html', host_url=request.host_url)
	else:
		return about()

@app.route('/service_post', methods=['POST', 'GET'])
def service_post():
	if session.get('username') is None:
		return render_template('login.html', host_url=request.host_url)
	if request.method == 'POST':
		user_input = request.form['content']
		result = encode_base64(user_input)
		return about(content=user_input, result=result)
	
@app.route("/about")
def about(content=None, result=None):
	if session.get('username') is None:
		return render_template('login.html', host_url=request.host_url)
	with open("./templates/encoder.html") as f:
		thisistemp = f.read()

	try:
		user_id = User.query.filter_by(username=session.get('username')).first().id
		name = session.get('username')
		datas = Post.query.filter_by(user_id=user_id).all()
	except:
		user_id = None
		name = None
		datas = None
	
	if content is not None:
		post = Post(content=content, result=result, user_id=user_id)
		db.session.add(post)
		db.session.commit()
	
		content = render_template_string(content)
		# -- patch --
		# content = render_template('encoder.html', content=content)
		# -- patch --
	return render_template('encoder.html', name=name, datas=datas, content=content, result=result, host_url=request.host_url)
	# --- patch ---
	# return render_template('encoder.html', name=name, datas=datas, content=content, result=result)
	# --- patch ---

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username, password=password).first()
		if user is not None and user.username != 'emperor':
			session['username'] = username
			return about()
		elif user is None and username == 'emperor' and password == app.secret_key:
			session['username'] = username
			flash("hi emperor, do you want to go to emperor page?")
		else:
			flash('Login failed, check your username or password')
			return render_template('login.html', message='Login failed', host_url=request.host_url)
	return render_template('login.html', host_url=request.host_url)

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user is None and username != 'emperor' and username != '' and password != '':
			user = User(username=username, password=password)
			db.session.add(user)
			db.session.commit()
			return render_template('login.html', message='Register successfully', host_url=request.host_url)
		elif username == 'emperor':
			flash("황제를 등록하는 것은 경솔한 행동이다")
			return render_template('login.html', message='황제를 등록하는 것은 경솔한 행동이다', host_url=request.host_url)
		elif username == '' or password == '':
			flash('Username or password is empty')
			return render_template('login.html', message='Username or password is empty', host_url=request.host_url)
		else:
			flash('User already exists')
			return render_template('login.html', message='User already exists', host_url=request.host_url)
	return render_template('login.html', host_url=request.host_url)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return render_template('login.html', host_url=request.host_url)

@app.route('/emperor')
def emperor():
	if session.get('username') is None:
		flash("login first")
		return render_template('login.html', host_url=request.host_url)
	if session.get('username') != 'emperor' and session.get('username'): 
		flash('your not emperor')
		return about()
	users = User.query.all()
	count_contents = []
	for user in users:
		count_contents.append(len(Post.query.filter_by(user_id=user.id).all()))
	datas = zip(users, count_contents)
	return render_template('emperor.html', datas=datas, host_url=request.host_url)

@app.route('/delete_content/<int:user_id>')
def del_content(user_id):
	post = Post.query.filter_by(user_id=user_id).all()
	for p in post:
		db.session.delete(p)
	db.session.commit()
	return redirect(url_for('emperor'))

@app.route('/delete_user/<int:user_id>')
def del_user(user_id):
	# 유저가 작성한 글 삭제
	post = Post.query.filter_by(user_id=user_id).all()
	for p in post:
		db.session.delete(p)
	# 유저 삭제
	user = User.query.filter_by(id=user_id).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('emperor'))

db.init_app(app)
db.app = app
with app.app_context():
	db.create_all()


app.run(host="0.0.0.0", port=4242, debug=True)

