from flask import Flask, render_template
import mockotfc

otfc = mockotfc.OTFC()


app = Flask(__name__)

@app.route('/main/')
def main():
    return render_template("index.html")


@app.route('/tdtools/')
def tdtools():
    return render_template("tdtools.html", otfc = otfc)


if __name__ == "__main__":
    app.run()
