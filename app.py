from flask import Flask
from flask import render_template, request
from flask import redirect, url_for
from flask_wtf import Form
from wtforms import validators, StringField, HiddenField
from flask_basicauth import BasicAuth

import re

from utils import (claim_square, validate_square, get_squares, get_squares_validated, swap_squares, get_numbers)

class NameForm(Form):
	name = StringField('name', validators = [validators.DataRequired()])
	square = HiddenField('square')

class SwapForm(Form):
	square_a = StringField('square_a',
					validators = [
							validators.DataRequired(),
							validators.Regexp('^([0-9]{2})$', message = 'Invalid value for square. Square value must be 2 digit number from above')
							]
						)
	square_b = StringField('square_b',
					validators = [
							validators.DataRequired(),
							validators.Regexp('^([0-9]{2})$', message = 'Invalid value for square. Square value must be 2 digit number from above')
							]
						)

class SwapConfirmForm(Form):
	square_a = HiddenField('square_a')
	square_b = HiddenField('square_b')

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['BASIC_AUTH_USERNAME'] = 'superbowl'
app.config['BASIC_AUTH_PASSWORD'] = 'patriots'
basic_auth = BasicAuth(app)


### numbers format example
"""
numbers = {
		"patriots": {
			'q1': [0, 9, 8, 7, 6, 5, 4, 3, 2, 1],
			'q2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
			'q3': [0, 9, 8, 7, 6, 5, 4, 3, 2, 1],
			'q4': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
		},
		"eagles": {
			'q1': [0, 9, 8, 7, 6, 5, 4, 3, 2, 1],
			'q2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
			'q3': [0, 9, 8, 7, 6, 5, 4, 3, 2, 1],
			'q4': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
		}
	}
"""

@app.route('/')
def index():
	return "Hello World !!"

@app.route('/squares', methods=['GET'])
def squares():
	squares = get_squares()
	
	numbers = get_numbers()
	return render_template('squares.html', squares = squares, numbers = numbers)

@app.route('/squares_validated', methods=['GET'])
@basic_auth.required
def squares_validated():
	squares = get_squares()
	squares_validated = get_squares_validated()

	return render_template('squares_validated.html', squares = squares, squares_validated = squares_validated)

@app.route('/squares_swap', methods = ['GET', 'POST'])
@basic_auth.required
def squares_swap():
	squares = get_squares()
	numbers = get_numbers()

	swap_form = SwapForm()

	if (request.method == 'POST'):
		action = request.form['submit']
		if action == 'swap':
			if (swap_form.validate_on_submit()):
				form_data  = request.form.to_dict()
				square_a = form_data['square_a']
				square_b = form_data['square_b']

				index_a = [int(x) for x in list(square_a)]
				index_b = [int(x) for x in list(square_b)]
				
				swap_confirm_form = SwapConfirmForm(square_a = square_a, square_b = square_b)

				return render_template('squares_swap.html', 
										squares = squares,
										numbers = numbers, 
										swap_confirm_form = swap_confirm_form,
										action = 'confirm',
										index_a = index_a,
										index_b = index_b)

			else:
				return render_template('squares_swap.html', squares = squares, numbers = numbers, swap_form = swap_form, action = 'input')
		if (action == 'confirm'):			
			form_data = request.form.to_dict()
			square_a = form_data['square_a']
			square_b = form_data['square_b']
			swap_squares(square_a, square_b)

			return redirect(url_for('squares_swap'))
	else:
		swap_form = SwapForm()
		return render_template('squares_swap.html', squares = squares, numbers = numbers, swap_form = swap_form, action = 'input')

@app.route('/claim', methods = ['GET', 'POST'])
def claim():
	name_form = NameForm(request.form)
	if (request.method == 'POST'):
		if (name_form.validate_on_submit()):
			form_data = request.form.to_dict()
			square = form_data['square']
			name = form_data['name']
			claim_square(square, name)
			
			return redirect(url_for('squares'))
		else:
			return render_template('claim.html', form = name_form)
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


