from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bsplhkxszxlwnc:14c4eb0e92485145bea8d2b278eb04622b1caef88ae23261920c77107d56d396@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d5ueis6uarurgd?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email_ = email
        self.height_ = height

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email_name']
        height = request.form['height_name']
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template('success.html')
    return render_template(
        'index.html', 
        text='Seems like we\'ve got something from that email address already!'
    )

if __name__ == '__main__':
    app.debug = True
    app.run()