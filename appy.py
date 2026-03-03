from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Granja: 5x5 tiles (0=vacío, 1=plantado)
farm_size = 5
farm = [[{"crop": None, "growth": 0} for _ in range(farm_size)] for _ in range(farm_size)]
day = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_state")
def get_state():
    return jsonify({"farm": farm, "day": day})

@app.route("/plant", methods=["POST"])
def plant():
    data = request.json
    x, y = data["x"], data["y"]
    crop = data["crop"]
    if farm[y][x]["crop"] is None:
        farm[y][x]["crop"] = crop
        farm[y][x]["growth"] = 0
    return jsonify(success=True, farm=farm)

@app.route("/next_day", methods=["POST"])
def next_day():
    global day
    day += 1
    for row in farm:
        for tile in row:
            if tile["crop"]:
                tile["growth"] += 1
    return jsonify(success=True, day=day, farm=farm)

if __name__ == "__main__":
    app.run(debug=True)
