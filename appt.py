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
    timeframe_choice = request.args.get('timeframe_choice', type=int)

    if not 1 <= timeframe_choice <= len(valid_timeframes):
        return jsonify({'error': 'Invalid timeframe choice. Please enter a valid number.'}), 400

    timeframe = valid_timeframes[timeframe_choice - 1]

    pytrends = TrendReq(hl='en-US', tz=360)

    product_name = data['name'][0]
    kw_list = [product_name]
    geo = "IN"

    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo)
    interest_over_time_df = pytrends.interest_over_time().reset_index()

    interest_over_time_df['date'] = interest_over_time_df['date'].astype(str)

    result = {
    'sva': interest_over_time_df.rename(columns={product_name: 'score'})[['date', 'score']].to_dict(orient='records')
}


    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
