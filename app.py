from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, validators
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,)
    firstname = db.Column(db.String(45), index=True, nullable=False)
    lastname = db.Column(db.String(45), index=True, nullable=False)
    email = db.Column(db.String(45), index=True, unique=True)
    country = db.Column(db.String(45), index=True, nullable=False)
    city = db.Column(db.String(45), index=True, nullable=False)

    def __init__(self, firstname, lastname, email, country, city):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.country = country
        self.city = city

    def __repr__(self) -> str:
        return "User: \n First Name: {firstname} \n Last Name: {lastname} \n Email: {email} \n Country: {country}\n City: {city}".format(firstname=self.firstname, lastname=self.lastname, email=self.email, country=self.country, city=self.city)


class UserForm(FlaskForm):
    firstname = StringField('Firstname', [validators.DataRequired()])
    lastname = StringField('Lastname', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route('/newuser', methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        new_user = User(firstname=request.form['firstname'], lastname=request.form['lastname'],
                        email=request.form['email'], country=request.form['country'], city=request.form['city'])
        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
    return render_template('form.html', user_form=UserForm())


@app.route('/user/<int:id>')
def get_user_by_id(id):
    user = User.query.get(id)
    return render_template('user.html', user=user)


@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.firstname = request.form.get('firstname')
        user.lastname = request.form.get('lastname')
        user.email = request.form.get('email')
        user.country = request.form.get('country')
        user.city = request.form.get('city')
        try:
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
    return render_template('edit.html', user_form=UserForm(), user=user)


@app.route('/users/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    try:
        db.session.commit()
        return redirect('/')
    except:
        db.session.rollback()


@app.errorhandler(404)
def not_found(error):
    return render_template('404_Not_Found.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500_Internal_Server_Error.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
