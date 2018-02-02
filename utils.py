import os
import simplejson as json

script_dir = os.path.dirname(os.path.abspath(__file__))
squares_dir = os.path.abspath(script_dir + '/.squares')

if not os.path.exists(squares_dir):
	os.makedirs(squares_dir)

def read_square_json(file_path):
	fp = open(file_path, 'r')
	value = json.load(fp)
	fp.close()

	return value

def write_square_json(file_path, value):
	fp = open(file_path, 'w')
	json.dump(value	, fp)
	fp.close()

def claim_square(square, name):
	file_path = squares_dir + '/' + square + '.json'
	value = {
				'square': square, 
			 	'name': name,
			 	'validated': False
			 }

	write_square_json(file_path, value)

def get_squares():
	square_files = os.listdir(squares_dir)
	squares = {}
	for f in square_files:
		value = read_square_json(squares_dir + '/' + f)

		square = value['square']
		name = value['name']

		squares[square] = name

	return squares

def get_squares_validated():
	square_files = os.listdir(squares_dir)
	squares = {}
	for f in square_files:
		value = read_square_json(squares_dir + '/' + f)

		square = value['square']
		validated = value['validated']

		squares[square] = validated

	return squares

def validate_square(square):
	file_path = squares_dir + '/' + square + '.json'

	value = read_square_json(file_path)
	value['validated'] = True

	write_square_json(file_path, value)

def swap_squares(square_a, square_b):
	square_a_val = read_square_json(squares_dir + '/' + square_a + '.json')
	square_b_val = read_square_json(squares_dir + '/' + square_b + '.json')

	square_a_val['square'] = square_b
	square_b_val['square'] = square_a

	write_square_json(squares_dir + '/' + square_a + '.json', square_b_val)
	write_square_json(squares_dir + '/' + square_b + '.json', square_a_val)

def get_numbers():
	numbers = {}
	numbers_file = script_dir + '/numbers.json'
	if (os.path.exists(numbers_file)) & (os.path.isfile(numbers_file)):
		fp = open(numbers_file, 'r')
		numbers = json.load(fp)
		fp.close()
	
	return numbers

if __name__ == '__main__':
	get_squares()