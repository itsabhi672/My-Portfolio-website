from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Abhimanyu_00@db.lwhckdlsqfdbttecgnnu.supabase.co:5432/postgres"
db.init_app(app)


class ContactData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    message  = db.Column(db.String(2000), nullable=False)

#Contact Form
class MyForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email =  StringField('Your Email', validators=[DataRequired(), Email("Please enter a correct email address.")])
    subject =  StringField('Subject')
    message =  TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField("Send Message")

#Creating the Database Table
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    my_form = MyForm()
    if my_form.validate_on_submit():
        if request.method == "POST":
            data = ContactData(
                name=my_form.name.data,
                email=my_form.email.data,
                subject=my_form.subject.data,
                message=my_form.message.data
            )
            db.session.add(data)
            db.session.commit()
            flash("Thanks for your response.")
            return redirect(url_for("contact"))
    return render_template("contact.html", form=my_form)





if __name__ == "__main__":
    app.run(debug=True)