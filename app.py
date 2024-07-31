
import pandas as pd
from flask import Flask, jsonify
from memory_db import DataFrameDb
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def set_up()->DataFrameDb:
    df = pd.read_csv(r"C:\Users\jonat\Downloads\Root Beer Ratings - Sheet1.csv")
    in_mem = DataFrameDb()
    in_mem.import_data(df)
    return in_mem

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/root_beer/name_in/<name>")
def name_in(name):
    """
    file: root_beer_specs.yml
    """
    df_db = set_up()
    return str(df_db.name_present(name))

if __name__ == "__main__":
    app.run(debug=True)


# In memory 