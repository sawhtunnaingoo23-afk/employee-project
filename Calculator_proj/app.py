
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])

    addition = num1 + num2
    subtraction = num1 - num2
    multiplication = num1 * num2

    if num2 != 0:
        division = num1 / num2
    else:
        division = "Cannot divide by zero"

    return render_template(
        'result.html',
        num1=num1,
        num2=num2,
        addition=addition,
        subtraction=subtraction,
        multiplication=multiplication,
        division=division
    )

if __name__ == '__main__':
    app.run(debug=True)
