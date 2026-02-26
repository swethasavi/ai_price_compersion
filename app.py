from ai_predict import predict_price
from flask import Flask, render_template, request
from data.load_csv import load_market_data


app = Flask(__name__)

import os
market_data = load_market_data(
    os.path.join(os.path.dirname(__file__), "market_data.csv")
)

STORAGE_LOSS_PER_DAY = 0.012  # 1.2% per day
DAYS = 7


@app.route("/")
def index():
    return render_template("index.html", data=market_data)


@app.route("/compare", methods=["POST"])
def compare():
    district = request.form["district"]
    crop = request.form["crop"]
    quantity = float(request.form["quantity"])

    market1 = request.form["market1"]
    market2 = request.form["market2"]

    if market1 == market2:
        return "Error: Please select two different markets for comparison. <a href='/'>Go back</a>", 400

    transport1 = float(request.form["transport1"])
    transport2 = float(request.form["transport2"])

    m1_price = market_data[district][crop][market1]
    m2_price = market_data[district][crop][market2]

    loss_qty = quantity * STORAGE_LOSS_PER_DAY * DAYS
    effective_qty = quantity - loss_qty

    # --- OLD TODAY INCOME (unchanged) ---
    m1_today = (m1_price["today"] * quantity) - transport1
    m2_today = (m2_price["today"] * quantity) - transport2

    # --- NEW: AI predicted future prices ---
    predicted_m1_price = predict_price(district, crop, market1, DAYS)
    predicted_m2_price = predict_price(district, crop, market2, DAYS)

    m1_future = (predicted_m1_price * effective_qty) - transport1
    m2_future = (predicted_m2_price * effective_qty) - transport2

    options = {
        f"Sell today at {market1}": m1_today,
        f"Sell after 7 days at {market1}": m1_future,
        f"Sell today at {market2}": m2_today,
        f"Sell after 7 days at {market2}": m2_future,
    }

    best_option = max(options, key=options.get)

    return render_template(
        "result.html",
        district=district,
        crop=crop,
        quantity=quantity,
        market1=market1,
        market2=market2,
        m1_price=m1_price,
        m2_price=m2_price,
        m1_today=round(m1_today, 2),
        m1_future=round(m1_future, 2),
        m2_today=round(m2_today, 2),
        m2_future=round(m2_future, 2),
        ai_m1=round(predicted_m1_price, 2),
        ai_m2=round(predicted_m2_price, 2),
        best_option=best_option,
        best_value=round(options[best_option], 2)
    )


if __name__ == "__main__":
    app.run(debug=True)
