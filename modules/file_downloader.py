# download_files.py

from models import ALL_MODELS, INCLUDED_FILTERS, API_Token
from datetime import datetime
import requests
import os
import time

# Set the current date string
current_date_str = datetime.now().strftime("%Y%m%d")

def execute_request(api_value):
    response = requests.get(api_value)
    response.raise_for_status()
    return response.content

def build_finviz_url(v: str, f_value: str, c_codes: str = None, ft: str = "4", token: str = API_Token):
    url = f"https://elite.finviz.com/export.ashx?v={v}&f={f_value}"
    if c_codes:
        url += f"&c={c_codes}"
    url += f"&ft={ft}&auth={token}"
    return url

def download_files(models, pull_tickers=False, ticker_filename="all_stocks.csv"):
    # convert to list if needed
    if not isinstance(models, list):
        models = [models]
    
    # Download main stock list
    all_stocks_url = f"https://elite.finviz.com/export.ashx?v=151&f=geo_usa,ind_stocksonly&c={INCLUDED_FILTERS}&ft=4&auth=0be90b58-6916-4652-98d4-d050032195f4"
    
    if pull_tickers:
        for m in models:
            filename = f"{m.data_path}{current_date_str}_{ticker_filename}"
            try:
                content = execute_request(all_stocks_url)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "wb") as f:
                    f.write(content)
                print(f"Downloaded main stock list to {filename}")
                time.sleep(62)  # wait to avoid rate limiting
            except Exception as e:
                print(f"Error fetching/saving main stocks file: {e}")
    
    # Download metrics for each model
    time.sleep(62)  # wait before starting metric downloads
    for m in models:
        for group in m.metric_groups:
            for metric in group.metrics:
                url = build_finviz_url(v="151", f_value=metric.filter, c_codes=INCLUDED_FILTERS)
                filename = f"{m.data_path}{current_date_str}_{metric.metric_name}.csv"
                try:
                    content = execute_request(url)
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "wb") as f:
                        f.write(content)
                    print(f"Successfully downloaded {filename}")
                    time.sleep(62)
                except Exception as e:
                    print(f"Error fetching/writing {filename}: {e}")

    print("Download complete.")

def main():
    # Example: call download_files with models
    # You might need to import models or set models here
    from models import ALL_MODELS
    download_files(ALL_MODELS, pull_tickers=True)

# This makes the script executable via
if __name__ == "__main__":
    main()
