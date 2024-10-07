import datetime
from flask import Flask

app = Flask(__name__)

page_counter = 0
@app.route('/endpoint/counter')
def func():
    global page_counter
    page_counter += 1
    return f'Страница была посещена {page_counter} раз'