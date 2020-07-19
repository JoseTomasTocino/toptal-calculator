from flask import Flask, request, jsonify
from flask_cors import CORS

from calculator.evaluator import evaluate

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def index():
    expression = request.args.get('expression', '')

    try:
        retval = {
            'expression': expression,
            'result': evaluate(expression),
            'error': False
        }

    except RuntimeError as e:
        retval = {
            'expression': expression,
            'result': '',
            'error': True,
            'error_str': str(e)
        }

    return jsonify(retval)


if __name__ == "__main__":
    app.run(debug=True)
