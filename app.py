from flask import Flask, request
import pandas as pd
import pickle

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    read_rf = pickle.load(f)


@app.route("/", methods=["GET"])
def hola():
    return "Todo ok"

@app.route("/predict", methods=["GET"])
def predict():
    age = request.args.get("age", None)
    sex = request.args.get("sex", None)
    clase = request.args.get("clase", None)

    if age is None or sex is None or clase is None:
        return "No sueño contigo"
    
    if not (age.isnumeric() and sex.isnumeric() and clase.isnumeric()): 
        return "datos de miercoles"

    survived = "Sobrevivio" if read_rf.predict([[age, sex, clase]])[0] else "Palmo"
    return f"""Para la persona con age {age}, sex {sex} y clase {clase}, 
la prediccion es de {survived}"""


if __name__  == "__main__":
    app.run(debug=True)