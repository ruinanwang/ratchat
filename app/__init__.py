
import config
from flask import Flask, render_template
from sms import sms

SECRET_KEY = config.secret_key
app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(sms)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', data=[1,2,3,4])

if __name__ == '__main__':
    app.run(debug=True)
