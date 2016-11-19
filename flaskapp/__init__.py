import requests
from flask import Flask, render_template, request
import mockotfc
import jpy2hkd
import datetime
from forex_python.converter import CurrencyRates

otfc = mockotfc.OTFC()

app = Flask(__name__)

@app.route('/git/')
def git():
    return render_template("git.html")

@app.route('/tdtools/')
def tdtools():
    return render_template("tdtools.html", otfc = otfc)

@app.route('/jpy2hkd/', methods=['GET', 'POST'])
def jpdTohkd():
    # get currency rate for JPY
    # currentJPY = 0.07122
    c = CurrencyRates()
    currentJPY = c.get_rate('JPY','HKD')
    datetimeStr = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


    g1 = jpy2hkd.Group("100", 100, 1000, 50, 100, currentJPY)
    g2 = jpy2hkd.Group("1000", 1000, 5000, 100, 1000, currentJPY)
    # g2 = jpy2hkd.Group("2000", 2000, 3000, 100, 1000, currentJPY)
    # g2 = jpy2hkd.Group("3000", 3000, 4000, 100, 1000, currentJPY)
    # g2 = jpy2hkd.Group("4000", 4000, 5000, 100, 1000, currentJPY)
    g3 = jpy2hkd.Group("5000", 5000, 10000, 100, 1000, currentJPY)

    main = jpy2hkd.jpy2hkd()
    main.AddGroup("100",g1)
    main.AddGroup("1000",g2)
    main.AddGroup("5000",g3)

    jpy = 100
    hkd = round(currentJPY * jpy,1)
    errors = []

    if request.method == "POST":
        try:
            jpy_in = request.form.get('jpy_in')
            hkd_in = request.form.get('hkd_in')

            if jpy_in is not None:
                jpy = float(jpy_in)
                if jpy != 0:
                    hkd = jpy*currentJPY
                    hkd = round(hkd,1)

            if hkd_in is not None:
                hkd = float(hkd_in)
                if hkd != 0:
                    jpy = hkd/currentJPY
                    jpy = round(jpy,1)
        except:
            errors.append("Unable to get URL.")

    disCurrnetJPY = round((currentJPY*100),2)
    return render_template(
        "jpy2hkd.html", 
        main = main, 
        jpy = jpy, hkd = hkd, 
        currentJPY = disCurrnetJPY, 
        datetimeStr = datetimeStr)

if __name__ == "__main__":
    app.run()
