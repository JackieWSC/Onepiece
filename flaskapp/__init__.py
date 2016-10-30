from flask import Flask, render_template
import mockotfc

otfc = mockotfc.OTFC()


app = Flask(__name__)

@app.route('/git/')
def git():
    return render_template("git.html")


@app.route('/tdtools/')
def tdtools():
    return render_template("tdtools.html", otfc = otfc)


@app.route('/exchange/')
def git():
    return render_template("exchange.html")

if __name__ == "__main__":
    app.run()
