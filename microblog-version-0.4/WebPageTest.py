
# app = Flask(__name__)
# #the placement of the App.route in regards to the method matters


from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def hello():
	return 'sdfasd', request.method
@app.route('/<users>')
def index(users=None):
	return render_template('index.html',users=users)


@app.route('/User/<usr>')

def User(usr):
	return 'welcome back %s' %(usr)
@app.route('/NumTest/<int:numberTest>')
def blah(numberTest):
	return 'welcome back %s' %(numberTest)


@app.route('/profile/<name>')
def profile(name):
	return render_template("index.html",name=name)



@app.route('/SecondPage')

def secondPage():
	return '<h2>fbb </h2>'






if __name__== "__main__":
	app.run(debug=True)	
