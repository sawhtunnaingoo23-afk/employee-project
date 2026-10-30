from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    age = request.form.get('age', '').strip()
    uni = request.form.get('uni', '').strip()

    if not name or not age:
        return "Please enter both name and age.", 400

    if not age.isdigit() or int(age) <= 0:
        return "Please enter a valid age.", 400

    return render_template('result.html', name=name, age=int(age), uni=uni)


if __name__ == '__main__':
    app.run(debug=True)