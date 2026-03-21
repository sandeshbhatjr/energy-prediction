from flask import Flask, jsonify
from flask_cors import CORS
from pydantic import BaseModel, field_validator

import datetime as dt
import pandas as pd

from empredictor.data_cleanup import da_price
from empredictor.exceptions import RequestFailure
from empredictor.bidding_zone_info import Germany

import secret

# ---------- Pydantic models ----------

class DateParam(BaseModel):
    date_str: str

    @field_validator("date_str")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        if len(v) != 8 or not v.isdigit():
            raise ValueError("Date must be in yyyymmdd format")
        year, month, day = int(v[:4]), int(v[4:6]), int(v[6:8])
        dt.datetime(year, month, day)  # raises ValueError if invalid
        return v

    @property
    def year(self) -> int:
        return int(self.date_str[:4])

    @property
    def month(self) -> int:
        return int(self.date_str[4:6])

    @property
    def day(self) -> int:
        return int(self.date_str[6:8])

    def to_timestamps(self) -> tuple[pd.Timestamp, pd.Timestamp]:
        start = pd.Timestamp(
            dt.datetime(self.year, self.month, self.day, 0, 0), tz="Europe/Berlin"
        )
        end = pd.Timestamp(
            dt.datetime(self.year, self.month, self.day, 23, 0), tz="Europe/Berlin"
        )
        return start, end


class SummaryParam(BaseModel):
    period: str
    condition: str = "all"

    @field_validator("period")
    @classmethod
    def validate_period(cls, v: str) -> str:
        if v not in ("daily",):
            raise ValueError("Only 'daily' period is supported")
        return v

    @field_validator("condition")
    @classmethod
    def validate_condition(cls, v: str) -> str:
        if v not in ("all", "weekends"):
            raise ValueError("Condition must be 'all' or 'weekends'")
        return v


class ModelInfo(BaseModel):
    descr: str
    acc: str


# ---------- Application setup ----------

API_KEY = secret.API_KEY
da_price_germany = da_price(API_KEY, Germany)

app = Flask(__name__)
CORS(app)


# ---------- Error handlers ----------

@app.errorhandler(RequestFailure)
def handle_request_failure(error: RequestFailure):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(422)
def handle_validation_error(error):
    return jsonify({"err": str(error)}), 422


# ---------- Routes ----------

@app.route("/")
def root():
    return jsonify(
        {
            "desc": "energy-predictor backend API",
            "v": 1,
            "endpoints": {
                "/v1/daprices/<yyyymmdd>": "Day Ahead Prices in Germany",
                "/v1/model/list": "List of all trained models",
                "/v1/model/predict/<modelName>/<yyyymmdd>": "Model predictions",
                "/v1/summary/<period>/<condition>": "Background Summary",
            },
        }
    )


@app.route("/v1/daprices/<date_chosen>")
def get_daprice(date_chosen: str):
    try:
        date_param = DateParam(date_str=date_chosen)
    except ValueError as e:
        return jsonify({"err": str(e)}), 400

    start, end = date_param.to_timestamps()
    price = da_price_germany.get(start, end)

    if price is not None:
        price.set_index(price.index.hour, inplace=True)
        return jsonify(price.to_dict())
    else:
        return jsonify({"err": "No data for this date available."}), 404


MODELS: dict[str, ModelInfo] = {
    "Naive": ModelInfo(
        descr="This is used to setup a baseline performance; it is not for actual modelling.",
        acc="33.67%",
    ),
    "AR(k=720)": ModelInfo(
        descr="Univariate approach 1 with a seasonality of 720 hours.",
        acc="13.67%",
    ),
    "VAR(k=720)": ModelInfo(
        descr="Mulitvariate approach with a seasonality of 14 days.",
        acc="6.67%",
    ),
}


@app.route("/v1/model/list")
def list_models():
    return jsonify({name: model.model_dump() for name, model in MODELS.items()})


@app.route("/v1/model/predict/<model_name>/<date_chosen>")
def predict(model_name: str, date_chosen: str):
    try:
        DateParam(date_str=date_chosen)
    except ValueError as e:
        return jsonify({"err": str(e)}), 400

    if model_name not in MODELS:
        return jsonify({"err": f"Model '{model_name}' not found"}), 404

    return jsonify({"err": "Prediction endpoint not yet implemented"}), 501


@app.route("/v1/summary/<period>/<condition>")
def summarise(period: str, condition: str):
    try:
        params = SummaryParam(period=period, condition=condition)
    except ValueError as e:
        return jsonify({"err": str(e)}), 400

    df = da_price_germany.ddf.dataframe

    if params.condition == "all":
        grouped_df = df.groupby(df.index.hour)
    elif params.condition == "weekends":
        grouped_df = df[
            (df.index.weekday == 0) | (df.index.weekday == 1)
        ].groupby(df.index.hour)

    def lq(x):
        return x.mean() - x.std()

    def uq(x):
        return x.mean() + x.std()

    summary_df = grouped_df.agg({"Day Ahead Price": ["mean", "min", "max", lq, uq]})
    return jsonify(summary_df["Day Ahead Price"].to_dict())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
