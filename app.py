from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

#ENV = 'prod'
ENV = 'dev'
app.config['SECRET_KEY'] = "my super secret key"

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

# Create a Blog Post Model
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    barcode = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(150))
    minqty = db.Column(db.Integer)
    ohqty = db.Column(db.Integer)

    def __repr__(self):
        return '<barcode %r>' % self.barcode

class ItemForm(FlaskForm):
    barcode = StringField("barcode", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    category = StringField("category")
    minqty = StringField("minqty")
    ohqty = StringField("ohqty")
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addinv')
def addinv():
    return render_template('addinv.html')



#ADD database record
@app.route('/addtodb', methods=['GET', 'POST'])
def addtodb():
    barcode = None
    form = ItemForm()
    if form.validate_on_submit():
        item = Items.query.filter_by(barcode=form.barcode.data).first()
        if item is None:
            item = Items(barcode = form.barcode.data, name=form.name.data, category = form.category.data, minqty = form.minqty.data, ohqty = form.ohqty.data)
            db.session.add(item)
            db.session.commit()
        barcode = form.barcode.data
        form.barcode.data = ''
        form.name.data = ''
        form.category.data = ''
        form.minqty.data = ''
        form.ohqty.data = ''
    our_items = Items.query.order_by(Items.name)
    return render_template("addtodb.html", form = form, barcode=barcode, our_items = our_items)

@app.route('/add_inv', methods=['POST'])
def add_inv():
    barcode = request.form['barcode']
    name = request.form['name']
    category = request.form['category']
    ohqty = request.form['ohqty']
    minqty = request.form['minqty']
    # extract the image URL from the form data
    #image_url = ...

    # create a new Item object and add it to the database
    item = Items(barcode=barcode, name=name, category=category, ohqty=ohqty, minqty=minqty)
    db.session.add(item)
    db.session.commit()

    return 'Item added to database'

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