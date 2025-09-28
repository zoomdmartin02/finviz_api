# process_models.py

from models import ALL_MODELS
from datetime import datetime
import os
import glob
import pandas as pd

# Set the current date string
current_date_str = datetime.now().strftime("%Y%m%d")

def get_metric_info(metric_name):
    # Loop through all models, groups, and metrics
    for model in ALL_MODELS:
        for group in model.metric_groups:
            for metric in group.metrics:
                if metric.metric_name == metric_name:
                    return metric.metric_name, metric.threshold
    # If not found
    return "Unknown Metric", "No Threshold"

def process_model(model, current_date_str):
    # Load main stocks
    all_stocks_path = f"{model.data_path}{current_date_str}_all_stocks.csv"
    all_stocks_df = pd.read_csv(all_stocks_path)

    # Gather feature files
    pattern = f"{model.data_path}{current_date_str}_*.csv"
    files = glob.glob(pattern)
    all_files = [f for f in files if os.path.basename(f) != f"{current_date_str}_all_stocks.csv"]

    # Load feature data
    features_df_list = []
    for file in all_files:
        try:
            df = pd.read_csv(file)
            filename_only = os.path.basename(file)
            feature_name = filename_only.replace('.csv', '').replace(f"{current_date_str}_", "")
            metric_name, threshold = get_metric_info(feature_name)
            df['FeatureDescription'] = f"{metric_name} ({threshold})"
            features_df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    combined_df = pd.concat(features_df_list, ignore_index=True)

    # Make lookup dicts
    metric_info_map = {}
    for group in model.metric_groups:
        for metric in group.metrics:
            metric_info_map[metric.metric_name] = {'group': group.name, 'weight': metric.weight}


    # Create ticker to features map
    ticker_feature_map = {}
    for ticker in all_stocks_df['Ticker']:
        feature_list = list(combined_df[combined_df['Ticker'] == ticker]['FeatureDescription'])
        ticker_feature_map[ticker] = feature_list


    # 7. Map Ticker attributes
    mapping_df = all_stocks_df[['Ticker', 'Company', 'Index', 'Sector', 'Industry', 'Country', 'Exchange', 
                                'Market Cap', 'P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 'Dividend Yield', 
                                'Dividend TTM', 'Dividend Ex Date', 'Dividend Growth 1 Year', 'Dividend Growth 3 Years',
                                'Dividend Growth 5 Years', 'Payout Ratio', 'EPS (ttm)', 'EPS Growth Past 3 Years', 
                                'EPS Growth Past 5 Years', 'EPS Growth Next 5 Years', 'Sales Year Over Year TTM', 'Sales Growth Past 3 Years', 
                                'Sales Growth Past 5 Years', 'Sales Growth Quarter Over Quarter', 'EPS Surprise',
                                'Insider Transactions', 'Institutional Ownership', 'Current Ratio', 'Quick Ratio',
                                'Total Debt/Equity', 'Gross Margin', 'Operating Margin', 'Profit Margin', 'Volatility (Week)',
                                'Volatility (Month)', '20-Day Simple Moving Average', '50-Day Simple Moving Average',
                                '200-Day Simple Moving Average', '50-Day High', '50-Day Low', '52-Week High',
                                '52-Week Low', 'Relative Strength Index (14)','Analyst Recom', 'Average Volume',
                                'Relative Volume', 'Price', 'Change', 'Volume', 'Prev Close', 'High', 'Low', '52-Week Range',
                                'All-Time High', 'All-Time Low', 'Performance (Quarter)','Performance (Half Year)',
                                'Performance (Year)']].set_index('Ticker')
    ticker_to_company = mapping_df['Company'].to_dict()
    ticker_to_index = mapping_df['Index'].to_dict()
    ticker_to_sector = mapping_df['Sector'].to_dict()
    ticker_to_industry = mapping_df['Industry'].to_dict()
    ticker_to_country = mapping_df['Country'].to_dict()
    ticker_to_exchange = mapping_df['Exchange'].to_dict()
    ticker_to_market_cap = mapping_df['Market Cap'].to_dict()
    ticker_to_p_e = mapping_df['P/E'].to_dict()
    ticker_to_forward_p_e = mapping_df['Forward P/E'].to_dict()
    ticker_to_peg = mapping_df['PEG'].to_dict()
    ticker_to_p_s = mapping_df['P/S'].to_dict()
    ticker_to_p_b = mapping_df['P/B'].to_dict()
    ticker_to_dividend_yield = mapping_df['Dividend Yield'].to_dict()
    ticker_to_dividend_ttm = mapping_df['Dividend TTM'].to_dict()
    ticker_to_dividend_ex_date = mapping_df['Dividend Ex Date'].to_dict()
    ticker_to_dividend_growth_1y = mapping_df['Dividend Growth 1 Year'].to_dict()
    ticker_to_dividend_growth_3y = mapping_df['Dividend Growth 3 Years'].to_dict()
    ticker_to_dividend_growth_5y = mapping_df['Dividend Growth 5 Years'].to_dict()
    ticker_to_payout_ratio = mapping_df['Payout Ratio'].to_dict()
    ticker_to_eps_ttm = mapping_df['EPS (ttm)'].to_dict()
    ticker_to_eps_growth_3y = mapping_df['EPS Growth Past 3 Years'].to_dict()
    ticker_to_eps_growth_5y = mapping_df['EPS Growth Past 5 Years'].to_dict()
    ticker_to_eps_growth_next_5y = mapping_df['EPS Growth Next 5 Years'].to_dict()
    ticker_to_sales_year_over_year_ttm = mapping_df['Sales Year Over Year TTM'].to_dict()
    ticker_to_sales_growth_3y = mapping_df['Sales Growth Past 3 Years'].to_dict()
    ticker_to_sales_growth_5y = mapping_df['Sales Growth Past 5 Years'].to_dict()
    ticker_to_sales_growth_qoq = mapping_df['Sales Growth Quarter Over Quarter'].to_dict()
    ticker_to_eps_surprise = mapping_df['EPS Surprise'].to_dict()
    ticker_to_insider_transactions = mapping_df['Insider Transactions'].to_dict()
    ticker_to_institutional_ownership = mapping_df['Institutional Ownership'].to_dict()
    ticker_to_current_ratio = mapping_df['Current Ratio'].to_dict()
    ticker_to_quick_ratio = mapping_df['Quick Ratio'].to_dict()
    ticker_to_total_debt_equity = mapping_df['Total Debt/Equity'].to_dict()
    ticker_to_gross_margin = mapping_df['Gross Margin'].to_dict()
    ticker_to_operating_margin = mapping_df['Operating Margin'].to_dict()
    ticker_to_profit_margin = mapping_df['Profit Margin'].to_dict()
    ticker_to_volatility_week = mapping_df['Volatility (Week)'].to_dict()
    ticker_to_volatility_month = mapping_df['Volatility (Month)'].to_dict()
    ticker_to_sma_20 = mapping_df['20-Day Simple Moving Average'].to_dict()
    ticker_to_sma_50 = mapping_df['50-Day Simple Moving Average'].to_dict()
    ticker_to_sma_200 = mapping_df['200-Day Simple Moving Average'].to_dict ()
    ticker_to_50_day_high = mapping_df['50-Day High'].to_dict()
    ticker_to_50_day_low = mapping_df['50-Day Low'].to_dict()
    ticker_to_52_week_high = mapping_df['52-Week High'].to_dict()
    ticker_to_52_week_low = mapping_df['52-Week Low'].to_dict()
    ticker_to_rsi_14 = mapping_df['Relative Strength Index (14)'].to_dict()
    ticker_to_analyst_recom = mapping_df['Analyst Recom'].to_dict()
    ticker_to_average_volume = mapping_df['Average Volume'].to_dict()
    ticker_to_relative_volume = mapping_df['Relative Volume'].to_dict()
    ticker_to_price = mapping_df['Price'].to_dict()
    ticker_to_change = mapping_df['Change'].to_dict()
    ticker_to_volume = mapping_df['Volume'].to_dict()
    ticker_to_prev_close = mapping_df['Prev Close'].to_dict()
    ticker_to_high = mapping_df['High'].to_dict()
    ticker_to_low = mapping_df['Low'].to_dict()
    ticker_to_52_week_range = mapping_df['52-Week Range'].to_dict()
    ticker_to_all_time_high = mapping_df['All-Time High'].to_dict()
    ticker_to_all_time_low = mapping_df['All-Time Low'].to_dict()
    ticker_to_performance_quarter = mapping_df['Performance (Quarter)'].to_dict()
    ticker_to_performance_half_year = mapping_df['Performance (Half Year)'].to_dict()
    ticker_to_performance_year = mapping_df['Performance (Year)'].to_dict()



    results = []

    # 8. Loop through each ticker and compute score
    for ticker in all_stocks_df['Ticker']:
        feature_list = ticker_feature_map.get(ticker, [])
        count = len(feature_list)

        # Build set of metric names in lowercase for case-insensitive matching
        all_metric_names = set()
        for group in model.metric_groups:
            for metric in group.metrics:
                all_metric_names.add(metric.metric_name.lower())

        # Initialize matched metrics dictionary
        matched_metrics_in_group = {metric_name: False for metric_name in all_metric_names}

        # Normalize feature descriptions to lowercase
        normalized_features = [feature.lower() for feature in feature_list]

        # Match features to metrics by substring (case-insensitive)
        for feature in normalized_features:
            for metric_name in all_metric_names:
                if metric_name in feature:
                    matched_metrics_in_group[metric_name] = True
                    break  # stop after first match

        # Now, use 'matched_metrics_in_group' for scoring
        multiplier = 1.0
        for metric_name, matched in matched_metrics_in_group.items():
            if matched:
                # Find the original metric object (case-sensitive)
                # so we can get the correct weight
                metric_obj = next(
                    m for g in model.metric_groups for m in g.metrics
                    if m.metric_name.lower() == metric_name
                )
                weight = float(metric_obj.weight)
                multiplier *= (1 + weight)

        # Convert score to percentage
        score = round((multiplier - 1) * 100, 2)
        

        # Add the Ticker URL:
        ticker_url = f"https://elite.finviz.com/quote.ashx?t={ticker}&ty=c&p=d&b=1"

        # Build the record
        # 10. Build result record
        results.append({
            'Ticker': ticker,
            'Ticker_URL': ticker_url,
            'Count': count,
            'Score': score,
            'Company': ticker_to_company.get(ticker, 'Unknown'),
            'Index': ticker_to_index.get(ticker, 'Unknown'),
            'Sector': ticker_to_sector.get(ticker, 'Unknown'),
            'Industry': ticker_to_industry.get(ticker, 'Unknown'),
            'Country': ticker_to_country.get(ticker, 'Unknown'),
            'Exchange': ticker_to_exchange.get(ticker, 'Unknown'),
            'Market Cap': ticker_to_market_cap.get(ticker, 'Unknown'),
            'P/E': ticker_to_p_e.get(ticker, 'Unknown'),
            'Forward P/E': ticker_to_forward_p_e.get(ticker, 'Unknown'),
            'PEG': ticker_to_peg.get(ticker, 'Unknown'),
            'P/S': ticker_to_p_s.get(ticker, 'Unknown'),
            'P/B': ticker_to_p_b.get(ticker, 'Unknown'),
            'Dividend Yield': ticker_to_dividend_yield.get(ticker, 'Unknown'),
            'Dividend TTM': ticker_to_dividend_ttm.get(ticker, 'Unknown'),
            'Dividend Ex Date': ticker_to_dividend_ex_date.get(ticker, 'Unknown'),
            'Dividend Growth 1 Year': ticker_to_dividend_growth_1y.get(ticker, 'Unknown'),
            'Dividend Growth 3 Years': ticker_to_dividend_growth_3y.get(ticker, 'Unknown'),
            'Dividend Growth 5 Years': ticker_to_dividend_growth_5y.get(ticker, 'Unknown'),
            'Payout Ratio': ticker_to_payout_ratio.get(ticker, 'Unknown'),
            'EPS (ttm)': ticker_to_eps_ttm.get(ticker, 'Unknown'),
            'EPS Growth Past 3 Years': ticker_to_eps_growth_3y.get(ticker, 'Unknown'),
            'EPS Growth Past 5 Years': ticker_to_eps_growth_5y.get(ticker, 'Unknown'),
            'EPS Growth Next 5 Years': ticker_to_eps_growth_next_5y.get(ticker, 'Unknown'),
            'Sales Year Over Year TTM': ticker_to_sales_year_over_year_ttm.get(ticker, 'Unknown'),
            'Sales Growth Past 3 Years': ticker_to_sales_growth_3y.get(ticker, 'Unknown'),
            'Sales Growth Past 5 Years': ticker_to_sales_growth_5y.get(ticker, 'Unknown'),
            'Sales Growth Quarter Over Quarter': ticker_to_sales_growth_qoq.get(ticker, 'Unknown'),
            'EPS Surprise': ticker_to_eps_surprise.get(ticker, 'Unknown'),
            'Insider Transactions': ticker_to_insider_transactions.get(ticker, 'Unknown'),
            'Institutional Ownership': ticker_to_institutional_ownership.get(ticker, 'Unknown'),
            'Current Ratio': ticker_to_current_ratio.get(ticker, 'Unknown'),
            'Quick Ratio': ticker_to_quick_ratio.get(ticker, 'Unknown'),
            'Total Debt/Equity': ticker_to_total_debt_equity.get(ticker, 'Unknown'),
            'Gross Margin': ticker_to_gross_margin.get(ticker, 'Unknown'),
            'Operating Margin': ticker_to_operating_margin.get(ticker, 'Unknown'),
            'Profit Margin': ticker_to_profit_margin.get(ticker, 'Unknown'),
            'Volatility (Week)': ticker_to_volatility_week.get(ticker, 'Unknown'),
            'Volatility (Month)': ticker_to_volatility_month.get(ticker, 'Unknown'),
            '20-Day Simple Moving Average': ticker_to_sma_20.get(ticker, 'Unknown'),
            '50-Day Simple Moving Average': ticker_to_sma_50.get(ticker, 'Unknown'),
            '200-Day Simple Moving Average': ticker_to_sma_200.get(ticker, 'Unknown'),
            '50-Day High': ticker_to_50_day_high.get(ticker, 'Unknown'),
            '50-Day Low': ticker_to_50_day_low.get(ticker, 'Unknown'),
            '52-Week High': ticker_to_52_week_high.get(ticker, 'Unknown'),
            '52-Week Low': ticker_to_52_week_low.get(ticker, 'Unknown'),
            'Analyst Recom': ticker_to_analyst_recom.get(ticker, 'Unknown'),
            'Average Volume': ticker_to_average_volume.get(ticker, 'Unknown'),
            'Relative Volume': ticker_to_relative_volume.get(ticker, 'Unknown'),
            'Price': ticker_to_price.get(ticker, 'Unknown'),
            'Change': ticker_to_change.get(ticker, 'Unknown'),
            'Volume': ticker_to_volume.get(ticker, 'Unknown'),
            'Prev Close': ticker_to_prev_close.get(ticker, 'Unknown'),
            'High': ticker_to_high.get(ticker, 'Unknown'),
            'Low': ticker_to_low.get(ticker, 'Unknown'),
            '52-Week Range': ticker_to_52_week_range.get(ticker, 'Unknown'),
            'All-Time High': ticker_to_all_time_high.get(ticker, 'Unknown'),
            'All-Time Low': ticker_to_all_time_low.get(ticker, 'Unknown'),
            'Performance (Quarter)': ticker_to_performance_quarter.get(ticker, 'Unknown'),
            'Performance (Half Year)': ticker_to_performance_half_year.get(ticker, 'Unknown'),
            'Performance (Year)': ticker_to_performance_year.get(ticker, 'Unknown'),
            'Relative Strength Index (14)': ticker_to_rsi_14.get(ticker, 'Unknown'),
            'RelatedFeatures': feature_list
        })

    # After the loop, create DataFrame and save results
    results_df = pd.DataFrame(results)

    # Sort and reset index as needed
    if model.name == "Value Model":
        results_df = results_df.sort_values(by=['Score', 'Count', 'Relative Strength Index (14)', 'P/E', 'Forward P/E', 'PEG'], 
                                            ascending=[False, False, True, True, True, True]).reset_index(drop=True)
    elif model.name == "Growth Model":
        results_df = results_df.sort_values(by=['Score', 'Count', 'Relative Strength Index (14)', 'EPS (ttm)', 'Sales Year Over Year TTM'], 
                                            ascending=[False, False, True, False, False]).reset_index(drop=True)
    elif model.name == "Dividend Model":
        results_df = results_df.sort_values(by=['Score', 'Count', 'Relative Strength Index (14)', 'Dividend Yield'], 
                                            ascending=[False, False, True, False]).reset_index(drop=True)
    elif model.name == "Momentum Model":
        results_df = results_df.sort_values(by=['Score', 'Count', 'Relative Strength Index (14)', 'Performance (Quarter)', 'Performance (Half Year)', 'Performance (Year)'], 
                                            ascending=[False, False, True, False, False, False]).reset_index(drop=True)

    # Add the Run_Date column
    results_df['Run_Date'] = current_date_str

    results_df['Clickable_URL'] = results_df.apply(
    lambda row: f'=HYPERLINK("{row["Ticker_URL"]}", "{row["Ticker"]}")', axis=1)  # For Excel's HYPERLINK formula

    col_order = ['Clickable_URL', 'Count','Score', 'Relative Strength Index (14)', 'Company', 'Index', 'Sector', 'Industry', 'Country', 'Exchange', 
                 'Market Cap', 'Price', 'Change', 'Volume', 'P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 
                 'Dividend Yield', 'Dividend TTM', 'Dividend Ex Date', 'Dividend Growth 1 Year', 
                 'Dividend Growth 3 Years', 'Dividend Growth 5 Years', 'Payout Ratio', 'EPS (ttm)', 
                 'EPS Growth Past 3 Years', 'EPS Growth Past 5 Years', 'EPS Growth Next 5 Years',
                 'Sales Year Over Year TTM', 'Sales Growth Past 3 Years', 'Sales Growth Past 5 Years', 
                 'Sales Growth Quarter Over Quarter', 'EPS Surprise','Insider Transactions',
                 'Institutional Ownership','Current Ratio','Quick Ratio','Total Debt/Equity',
                 'Gross Margin','Operating Margin','Profit Margin','Volatility (Week)',
                 'Volatility (Month)','20-Day Simple Moving Average','50-Day Simple Moving Average',
                 '200-Day Simple Moving Average','50-Day High','50-Day Low','52-Week High',
                 '52-Week Low','Analyst Recom','Average Volume',
                 'Relative Volume','Prev Close','High','Low','52-Week Range','All-Time High',
                 'All-Time Low','Run_Date','Performance (Quarter)','Performance (Half Year)', 
                 'Performance (Year)','RelatedFeatures']
    
    results_df = results_df[col_order]

    # Save the results for this model
    output_filename = f"{model.data_path}{model.name}_{current_date_str}_results.xlsx"
    results_df.to_excel(output_filename, index=False, engine='openpyxl')
    print(f"Results saved to {output_filename}")

    # --- Cleanup: delete non-result files ---
def cleanup_input_files():
    data_files = glob.glob(f"{model.data_path}*")
    for file in data_files:
        basename = os.path.basename(file)
        if "_results" not in basename:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")


# Loop over all models and process each
for model in ALL_MODELS:
    process_model(model, current_date_str)

del_files = input("Do you want to delete the input data files? Y or N")

if del_files.strip().upper() == 'Y':
    cleanup_input_files()
else:
    print("Input data files retained.")
