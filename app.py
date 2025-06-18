from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    results = []

    balances = {}
    for player in data:
        name = player['name']
        buy_in = int(player['buy_in']) if player['buy_in'] else 0
        cash_out = int(player['cash_out']) if player['cash_out'] else 0
        balances[name] = cash_out - buy_in

    owes = []
    payers = {k: v for k, v in balances.items() if v < 0}
    receivers = {k: v for k, v in balances.items() if v > 0}

    for payer, debt in payers.items():
        debt = abs(debt)
        for receiver in list(receivers):
            if receivers[receiver] == 0:
                continue
            payment = min(debt, receivers[receiver])
            owes.append(f"{payer} צריך להעביר {payment} ש\"ח ל-{receiver}")
            receivers[receiver] -= payment
            debt -= payment
            if debt == 0:
                break

    return jsonify(owes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)