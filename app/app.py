# Copyright (c) [2024] [Sebastian Kliem]
import pprint

from flask import Flask, render_template, request, jsonify, make_response
from utils.Functions import Calculate_Steam

app = Flask(__name__, static_url_path='/steamcalculator/static')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """

    if request.path.startswith('/steamcalculator/static/'):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route('/calculation', methods=["POST"])
def calculation():
    if request.method == "POST":
        entry_content = request.get_json()
        # pprint.pprint(entry_content)
        celsius = True
        if entry_content["max_flow_in"] == "Fahrenheit":
            celsius = False
        # print(celsius)
        calculator = Calculate_Steam.Calculate_Steam(temperature=int(entry_content["temperature"]),
                                                     humitidy=int(entry_content["humidity"]),
                                                     max_flow=int(entry_content["max_flow_in"]),
                                                     celsius=celsius,
                                                     high_temperature=entry_content["high_temperature"],
                                                     calculation_method_correction=entry_content["calculation_mode_setting"]
                                                     )

        result = calculator.get_amount_of_water()

        return jsonify(used_water_per_minute=result[0], used_water_per_hour=result[1])


if __name__ == "__main__":
    app.run()
