from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'
#ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ert33MNB@localhost/lexus'
else:
    app.debug = True
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zirttrbffmhloz:339ab0e6aea18db86a4fa458b520179730e285ce522efa7f88715f6a2cbc6066@ec2-3-208-74-199.compute-1.amazonaws.com:5432/datjvvm56fr58q'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jackson_inventory_user:AjssKyOevzJkzP0GrjZu7OQ9SUkoSneX@dpg-chb67f2k728tp9c87hsg-a.oregon-postgres.render.com/jackson_inventory'
    #postgres://jackson_inventory_user:AjssKyOevzJkzP0GrjZu7OQ9SUkoSneX@dpg-chb67f2k728tp9c87hsg-a.oregon-postgres.render.com/jackson_inventory

app.config['SQLALCHECMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:  #customer does not exist
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='you have already submitted feedback')

if __name__ == '__main__':
    app.run()