from flask import Flask, request, jsonify
from flask_cors import CORS

from calculator.evaluator import evaluate

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def index():
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
