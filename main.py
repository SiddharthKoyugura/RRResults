from flask import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from results import *
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "ILoveMyFamilyMoreThanAnything"

class StudentForm(FlaskForm):
    htno = StringField(label="Enter your Roll Number:", validators=[Length(min=10, max=10), DataRequired()])
    # code = SelectField(label="Semester:", choices=[("1-1", "1-1"), ("1-2", "1-2"), ("2-1", "2-1"), ("2-2", "2-2"), ("3-1", "3-1"), ("3-2", "3-2"), ("4-1", "4-1"), ("4-2", "4-2")], validators=[DataRequired()])
    submit = SubmitField(label="Get Result")

# Get Year for footer
x = datetime.now()
year = x.year

@app.route("/", methods=["GET", "POST"])
def home():
    sform = StudentForm()
    if sform.validate_on_submit():
        return redirect(url_for('results', roll=sform.htno.data))
    return render_template("home.html", form=sform, year=year)

@app.route("/results")
def results():
    roll = request.args["roll"]
    marks_data = get_result(roll)
    cgpa = 0
    i = 0
    for sem_code in ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2"]: 
        try:
            cgpa += marks_data[sem_code][-1]["sgpa"]
            i += 1
        except:
            pass
    if marks_data:
        return render_template("result.html", marks_data=marks_data, personal_data=personal_data, cgpa=round(cgpa / i,2))
    flash("INVALID CREDENTIALS / JNTUH SERVERS ARE DOWN")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)