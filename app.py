import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test_function():
    return 'Это тестовая страница ответ сгенерирован в %s' % \
        datetime.datetime.now().utcnow()

@app.route('/hello/world')
def hello():
    return 'HELLO WORLD!'
