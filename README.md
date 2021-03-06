# ToptalCalculator

![GitHub](https://img.shields.io/github/license/josetomastocino/toptal-calculator?style=flat-square) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/josetomastocino/toptal-calculator/CI?style=flat-square) ![GitHub top language](https://img.shields.io/github/languages/top/josetomastocino/toptal-calculator?style=flat-square)

ToptalCalculator is an advanced calculator built in Python by [José Tomás Tocino](https://josetomatocino.com)
for the Toptal Technical Screening process. It's able to process both **arithmetic expressions**
and **linear equations**, and has a simple companion **web interface** built with Flask to try the project.

![Capture](assets/capture.png)

## Capabilities

As previously stated, this calculator can process arithmetic expressions and solve linear equations, so long as they're
properly formatted. In particular:

* The calculator can solve **linear equations** with a single variable.
* The calculator can do calculations in both **infix and postfix (RPN) notation**.
* The calculator supports **parentheses** in infix notation.
* The calculator supports **addition, subtraction, multiplication, division, logarithms (log and ln), trigonometric
  functions (sin, cos, tan, ctan)**.
* The calculator works with the known constants of **Archimedes’ constant** (Pi) and **Euler’s number** (e).

## Implementation

The calculator is implemented in Python 3.8 with no external dependencies or libraries. The core resides in
the `calculator` package. It contains an `evaluator` module with an
`evaluate` function, which receives a string with the expression or equation and does all the processing.

In particular, the steps involved in the evaluation process are the following:

* First, the `parser` module is used to tokenize the input. Available tokens appear in the `tokens` module.
* Then, if the input is not in Reverse Polish Notation (postfix), the token list is converted to postfix notation.
* Finally, the evaluator detects whether the input represents a simple expression or an equation. The list of tokens in
  postfix notation is properly parsed and evaluated, and the result is returned. If there's an error, a `RuntimeError`
  exception is raised.

### Frontend and server

Optionally, **ToptalCalculator** offers a web-based user interface built with Flask in the back-end, and Vue.js + Bulma
in the front-end.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. First, make sure you have
Python3 properly installing by running:

```
python3 --version
```

Then, make sure you have pip and pipenv installed:

```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pipenv wheel
```

Install the dependencies:

```
pipenv install
```

Make sure the code is working properly by **running the tests**, using:

```
pipenv run pytest
```

It should report something like:

```
.....................................
----------------------------------------------------------------------
Ran 37 tests in 0.004s

OK
```

### Running the web user interface

Running the web user interface is really simple. Just run

```
python server/server.py
```

And then navigate to http://127.0.0.1:5000/ to check the user interface.

## Authors

* **José Tomás Tocino** - [Personal website](https://josetomastocino.com)

## License

This project is licensed under the Unlicense, meaning it's free and released into the public domain - see
the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Toptal for giving me this opportunity to show my skills!
