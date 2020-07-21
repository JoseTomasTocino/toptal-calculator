import os
import sys

from flask import Flask, request, jsonify, current_app
from flask_cors import CORS

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from calculator.evaluator import evaluate

app = Flask(__name__, static_folder='static')
CORS(app)


@app.route("/", methods=['GET'])
def index():
    return current_app.send_static_file('index.html')


@app.route("/evaluate", methods=['GET'])
def eval():
    expression = request.args.get('expression', '')
    notation = request.args.get('notation', 'standard')

    try:
        retval = {
            'expression': expression,
            'notation': notation,
            'result': evaluate(expression, notation == 'rpn'),
            'error': False,
            'error_str': ''
        }

    except RuntimeError as e:
        retval = {
            'expression': expression,
            'notation': notation,
            'result': '',
            'error': True,
            'error_str': str(e)
        }

    except BaseException as e:
        retval = {
            'expression': expression,
            'notation': notation,
            'result': '',
            'error': True,
            'error_str': "Other error: " + str(e)
        }

    return jsonify(retval)


if __name__ == "__main__":
    app.run(debug=True)
