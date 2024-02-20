from flask import Flask, jsonify, request
import pandas as pd
from pytrends.request import TrendReq
import statsmodels.api as sm

app = Flask(__name__)

valid_timeframes = [
    "now 1-d",
    "now 1-H",
    "now 4-H",
    "now 1-d",
    "now 7-d",
    "today 1-m",
    "today 3-m",
    "today 12-m",
    "today 5-y"
]
data = pd.read_csv('flaskserver/db.csv')
@app.route('/sva', methods=['GET'])
def interest_over_time():
    pytrends = TrendReq(hl='en-US', tz=360)
    product_name = data['name'][0]
    kw_list = [product_name]
    geo = "IN"
    
    sva_data = {}

    for timeframe in valid_timeframes:
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo)
        interest_over_time_df = pytrends.interest_over_time().reset_index()
        interest_over_time_df['date'] = interest_over_time_df['date'].astype(str)
        sva_data[timeframe] = interest_over_time_df.rename(columns={product_name: 'score'})[['date', 'score']].to_dict(orient='records')

    result = {'sva': sva_data}

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
