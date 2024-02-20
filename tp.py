import pandas as pd
from pytrends.request import TrendReq
import statsmodels.api as sm

# Read the CSV file containing product data
data = pd.read_csv("db.csv")

# Get user input for timeframe
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

print("Select a timeframe:")
for i, timeframe in enumerate(valid_timeframes, start=1):
    print(f"{i}. {timeframe}")

while True:
    try:
        choice = int(input("Enter the number corresponding to the desired timeframe: "))
        if 1 <= choice <= len(valid_timeframes):
            timeframe = valid_timeframes[choice - 1]
            break
        else:
            print("Invalid choice. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Get the product name
product_name = data['name'][0]
kw_list = [product_name]
geo = "IN"

# Fetch interest over time data
pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo)
interest_over_time_df = pytrends.interest_over_time()

# Perform seasonal decomposition
decomposition = sm.tsa.seasonal_decompose(interest_over_time_df[product_name], model='additive')

# Output text analysis
print("Seasonal Decomposition Analysis:")
print("-------------------------------")

# Analyzing Trend Component
trend_mean = decomposition.trend.mean()
trend_std = decomposition.trend.std()
print("Trend Component:")
print(f"Mean: {trend_mean}")
print(f"Standard Deviation: {trend_std}")
if trend_mean > 0:
    print("The trend component indicates an overall increasing trend in interest over time.")
elif trend_mean < 0:
    print("The trend component indicates an overall decreasing trend in interest over time.")
else:
    print("The trend component indicates a stable trend in interest over time.")

# Analyzing Seasonal Component
seasonal_mean = decomposition.seasonal.mean()
seasonal_std = decomposition.seasonal.std()
print("\nSeasonal Component:")
print(f"Mean: {seasonal_mean}")
print(f"Standard Deviation: {seasonal_std}")
if seasonal_mean > 0:
    print("The seasonal component suggests a seasonal increase in interest during certain periods.")
elif seasonal_mean < 0:
    print("The seasonal component suggests a seasonal decrease in interest during certain periods.")
else:
    print("The seasonal component suggests no significant seasonal pattern in interest.")

# Analyzing Residual Component
residual_mean = decomposition.resid.mean()
residual_std = decomposition.resid.std()
print("\nResidual Component:")
print(f"Mean: {residual_mean}")
print(f"Standard Deviation: {residual_std}")
print("The residual component represents unexplained variability in the data after removing trend and seasonal components.")
