
import pandas as pd
from flask import Flask, jsonify
from memory_db import DataFrameDb
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

def set_up()->DataFrameDb:
    df = pd.read_csv("data/root_beer.csv")
    in_mem = DataFrameDb()
    in_mem.import_data(df)
    return in_mem

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/root_beer/name_in/<name>")
@swag_from("root_beer/name_in.yml")
def name_in(name):
    df_db = set_up()
    return str(df_db.name_present(name))

@app.route("/root_beer/names")
@swag_from("root_beer/names.yml")
def all_names():
    df_db = set_up()
    names = list(df_db.data["Name"])
    print(names)
    return jsonify({"hello": names})

if __name__ == "__main__":
    app.run(debug=True)


# In memory 