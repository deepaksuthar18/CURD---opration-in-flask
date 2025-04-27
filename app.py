from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


# Create database tables
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/add", methods=["POST"])
def add_user():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]

    new_user = User(firstname=firstname, lastname=lastname, email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/update/<int:id>", methods=["POST"])
def update_user(id):
    user = User.query.get_or_404(id)
    user.firstname = request.form["firstname"]
    user.lastname = request.form["lastname"]
    user.email = request.form["email"]

    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
