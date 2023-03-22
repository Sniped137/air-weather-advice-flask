from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__, template_folder='../templates',static_folder='../static')

@app.route('/index')
def index():
    return render_template('test.html')

@app.route('/data')
def get_data():
    data = {
        'div1': 'Content for div 1',
        'div2': 'Content for div 2',
        'div3': 'Content for div 3'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)