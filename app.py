from flask import Flask
from flask import render_template, request
from flask import redirect, url_for
from wtforms import Form, validators, StringField, HiddenField

from flask_basicauth import BasicAuth
from utils import (claim_square, validate_square, get_squares, get_squares_validated)

class NameForm(Form):
	name = StringField('name', validators = [validators.DataRequired()])
	square = HiddenField('square')

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['BASIC_AUTH_USERNAME'] = 'superbowl'
app.config['BASIC_AUTH_PASSWORD'] = 'patriots'
basic_auth = BasicAuth(app)


@app.route('/')
def index():
	return "Hello World !!"

@app.route('/squares', methods=['GET'])
def squares():
	squares = get_squares()
	print (squares)

	return render_template('squares.html', squares = squares)

@app.route('/squares_validated', methods=['GET'])
@basic_auth.required
def squares_validated():
	squares = get_squares()
	squares_validated = get_squares_validated()

	return render_template('squares_validated.html', squares = squares, squares_validated = squares_validated)

@app.route('/claim', methods = ['GET', 'POST'])
def claim():
	name_form = NameForm(request.form)
	if (request.method == 'POST'):
		if (name_form.validate()):
			form_data = request.form.to_dict()
			square = form_data['square']
			name = form_data['name']
			claim_square(square, name)

			return redirect(url_for('squares'))
	else:
		square = request.args.get('s')
		name_form = NameForm(square = square)
		return render_template('claim.html', form = name_form)

@app.route('/validate', methods = ['GET'])
@basic_auth.required
def validate():
	if (request.method == 'GET'):
		square = request.args.get('s')
		validate_square(square)
		return redirect(url_for('squares_validated'))


if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 8100)


