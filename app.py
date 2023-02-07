from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        age = request.form.get("age")
        region = request.form.get("region")
        bmi = request.form.get("bmi")
        output = "Age: {}, Region: {}, BMI: {}".format(age, region, bmi)
        return render_template(r"webapp/template/index.html/index.html", output=output)
    return render_template(r"webapp/template/index.html/index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template(r"webapp/template/index.html/404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
