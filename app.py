from flask import Flask, request
import pandas as pd
import pickle
from sqlalchemy import create_engine

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    read_rf = pickle.load(f)

churro = "postgresql://usuario:JFgm8AoSMDyg5QCntFL5XVCtceQ9loUG@dpg-d4fjib0dl3ps73d0nbe0-a.oregon-postgres.render.com/mypostgres_x1sa"
engine = create_engine(churro)

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

    df = pd.DataFrame({
    "sex":[sex],
    "age":[age],
    "clase": [clase],
    "prediction": [survived]
    })
    df.to_sql("predictions", con=engine, if_exists="append", index=None)

    return f"""Para la persona con age {age}, sex {sex} y clase {clase}, 
la prediccion es de {survived}"""


if __name__  == "__main__":
    app.run(debug=True)