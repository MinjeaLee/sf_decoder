from flask import Flask, render_template, render_template_string
from flask import request, session, flash
import os
from model import db, User, Post
from service import encode_base64


app = Flask(__name__)


with open('flag.txt', 'r') as f:
	flag = f.read()
app.secret_key = str(flag)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(base_dir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# secret_key

@app.route('/')
def index():
	if session.get('username') is None:
		return render_template('login.html')
	else:
		return about()



@app.route('/service_post', methods=['POST', 'GET'])
def service_post():
	if session.get('username') is None:
		return render_template('login.html')
	if request.method == 'POST':
		user_input = request.form['content']
		result = encode_base64(user_input)
		return about(content=user_input, result=result)
	

@app.route("/about")
def about(content=None, result=None):
	if session.get('username') is None:
		return render_template('login.html')
	with open("./templates/2.html") as f:
		thisistemp = f.read()

	# filter_by user_id
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
	
		# content를 Jinja2 템플릿으로 렌더링합니다.
		content = render_template_string(content)
		# -- patch --
		# content = render_template('2.html', content=content)
		# -- patch --
	return render_template('2.html', name=name, datas=datas, content=content, result=result)
	# --- patch ---
	# return render_template('2.html', name=name, datas=datas, content=content, result=result)
	# --- patch ---

# login
@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		print(request.form)
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username, password=password).first()
		if user is not None:
			session['username'] = username
			return about()
		else:
			flash('Login failed')
			return render_template('login.html', message='Login failed')
	return render_template('login.html')

# register
@app.route('/register', methods=['POST', 'GET'])
def register():
	# db model User
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user is None:
			user = User(username=username, password=password)
			db.session.add(user)
			db.session.commit()
			return render_template('login.html', message='Register successfully')
		else:
			flash('User already exists')
			return render_template('login.html', message='User already exists')
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return render_template('login.html')


db.init_app(app)
db.app = app
with app.app_context():
	db.create_all()


app.run(port=9000, debug=True)

