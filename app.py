from flask import Flask, render_template, request
from src.set_logger import set_logger
from src.load_model import load_model

app = Flask(__name__, template_folder=r'webapp/template', static_folder='webapp/static')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        age = request.form.get("age")
        region = request.form.get("region")
        bmi = request.form.get("bmi")
        output = "Age: {}, Region: {}, BMI: {}".format(age, region, bmi)

        return render_template(r"index.html", output=output)
    return render_template(r"index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template(r"error_404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
