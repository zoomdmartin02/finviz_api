from dataclasses import dataclass
from typing import List, Optional

API_Token = "&auth=0be90b58-6916-4652-98d4-d050032195f4"
FINVIZ_BASE = "https://elite.finviz.com/export.ashx?v=111&f="

#Columns to include (no leading '&' or '?')
INCLUDED_FILTERS = ', '.join(str(i) for i in range(151))


@dataclass
class Metric:
    metric_name: str            # human label used in filenames and display
    filter: str
    threshold: float
    weight: str

    
@dataclass
class MetricGroup:
    name: str
    metrics: List[Metric]
    group_weight: float


@dataclass
class FinancialModel:
    name: str
    metric_groups: List[MetricGroup]
    data_path: str

def build_finviz_url(v: str, f_value: str, c_codes: Optional[str] = None, ft: str = "4", token: str = API_Token) -> str:
    """
    Build Finviz export URL without importing urlencode.
    (Assembles query string manually with proper commas and & separators.)
    """
    # ensure token has no leading & or auth= prefix
    token_val = token.strip()
    # base query
    url = f"{FINVIZ_BASE}?v={v}&f={f_value}"
    if c_codes:
        url += f"&c={c_codes}"
    url += f"&ft={ft}&auth={token_val}"
    return url

#Use v=151 (supports custom column c=) for all metrics that need INCLUDED_FILTERS
V_FOR_CUSTOM = "151"

#-----------------------
# Value Model
#-----------------------
Value_Model = FinancialModel(
    name="Value Model",
    data_path=".\\Value_Investing\\",
    metric_groups=[
        MetricGroup(
            name="Valuation",
            group_weight=1.0,
            metrics=[
                Metric("P_E Ratio", "fa_pe_0to15", "< 15", 0.25),
                Metric("Forward P_E", "fa_fpe_0to13", "< 13", 0.20),
                Metric("PEG Ratio", "fa_peg_0to1.5", "< 1.5", 0.15),
                Metric("Price_Book", "fa_pb_0to1.5", "< 1.5", 0.10),
                Metric("Price_Free Cash Flow", "fa_pfcf_u15", "< 15", 0.10),
                Metric("EV_Revenue", "fa_evsales_u2", "< 2", 0.10),
            ]
        ),
        MetricGroup(
            name="Profitability",
            group_weight=0.7,
            metrics=[
                Metric("Return on Equity (ROE)", "fa_roe_o15", "> 15%", 0.12),
                Metric("Gross Margin", "fa_grossmargin_o40", "> 40%", 0.08),
                Metric("Operating Margin", "fa_opermargin_o15", "> 15%", 0.08),
                Metric("Net Profit Margin", "fa_netmargin_o10", "> 10%", 0.07),
            ]
        ),
        MetricGroup(
            name="Balance Sheet",
            group_weight=0.6,
            metrics=[
                Metric("Current Ratio", "fa_curratio_o1.5", "> 1.5", 0.10),
                Metric("Debt_Equity", "fa_debteq_u0.5", "< 0.5", 0.10),
            ]
        )
    ]
)


#-----------------------
# Growth Model
#-----------------------
Growth_Model = FinancialModel(
    name="Growth Model",
    data_path=".\\Growth_Investing\\",
    metric_groups=[
        MetricGroup(
            name="Growth Rates",
            group_weight=1.0,
            metrics=[
                Metric("Revenue Growth (YOY)", "fa_salesyoyttm_o15", "> 15%", 0.30),
                Metric("EPS Growth (YOY)", "fa_epsyoy_o20", "> 20%", 0.30),
                Metric("5Y Revenue CAGR", "fa_sales5years_o20", "> 20%", 0.15),
                Metric("5Y EPS CAGR", "fa_eps5years_o25", "> 25%", 0.15),
            ]
        ),
        MetricGroup(
            name="Margins & ROIC",
            group_weight=0.7,
            metrics=[
                Metric("Return on Invested Capital (ROIC)", "fa_roi_12to100", "> 12%", 0.06),
                Metric("Gross Margin Expansion", "fa_grossmargin_pos", "Increasing", 0.05),
                Metric("Operating Margin Expansion", "fa_opermargin_pos", "Increasing", 0.04),
                Metric("Net Income Margin", "fa_netmargin_o15", "> 15%", 0.05),
            ]
        ),
        MetricGroup(
            name="Scale & Liquidity",
            group_weight=0.4,
            metrics=[
                Metric("Market Cap", "cap_midover", "Mid or Large (> $2B)", 0.03),
                Metric("Average Volume", "sh_avgvol_o1000", "Over 1M", 0.03),
            ]
        )
    ]
)


#-----------------------
#Dividend Model
#-----------------------
Dividend_Model = FinancialModel(
    name="Dividend Model",
    data_path=".\\Dividend_Investing\\",
    metric_groups=[
        MetricGroup(
            name="Yield & Payout Ratios",
            group_weight=1.0,
            metrics=[
                Metric("Dividend Yield", "fa_div_o3", "> 3%", 0.30),
                Metric("Payout Ratio", None, "< 60%", 0.15),  # no direct finviz export filter
                Metric("Forward Yield", None, "Above S&P Median", 0.10),
                Metric("FCF Payout Ratio", None, "< 70%", 0.10),
            ]
        ),
        MetricGroup(
            name="Dividend Growth & History",
            group_weight=0.7,
            metrics=[
                Metric("Dividend Growth 5Y CAGR", "fa_divgrowth_5yo5", "> 5%", 0.15),
                Metric("Dividend Aristocrat/King", None, "Yes", 0.10),
                Metric("Dividend CAGR 10Y", None, "> 5%", 0.05),
            ]
        ),
        MetricGroup(
            name="Safety & Coverage",
            group_weight=0.6,
            metrics=[
                Metric("Debt_Equity", "fa_debteq_u0.7", "< 0.7", 0.05),
                Metric("Interest Coverage", None, "> 4", 0.05),
                Metric("Dividend Coverage by FCF", None, "> 1.5x", 0.05),
            ]
        )
    ]
)


#-----------------------
#Momentum Model
#-----------------------
Momentum_Model = FinancialModel(
    name="Momentum Model",
    data_path=".\\Momentum_Investing\\",
    metric_groups=[
        MetricGroup(
            name="Price Momentum",
            group_weight=1.0,
            metrics=[
                Metric("Performance 3M", "ta_perf_3mup", "3M up", 0.30),
                Metric("Performance 6M", "ta_perf_6mup", "6M up", 0.20),
                Metric("Performance 1Y", "ta_perf_12mup", "1Y up", 0.20),
                Metric("RSI (14) High", "ta_rsi_o60", "RSI > 60", 0.10),
            ]
        ),
        MetricGroup(
            name="Volume & Liquidity",
            group_weight=0.6,
            metrics=[
                Metric("Relative Volume", "sh_relvol_o1.5", "> 1.5", 0.10),
                Metric("Average Volume", "sh_avgvol_o1000", "Over 1M", 0.05),
            ]
        ),
        MetricGroup(
            name="Trend Structure",
            group_weight=0.4,
            metrics=[
                Metric("Price Above 50 SMA", "ta_sma50_pa", "Price > 50 SMA", 0.05),
                Metric("50 SMA above 200 SMA", "ta_sma50_pa&ta_sma200_pa", "Golden cross", 0.05),
            ]
        )
    ]
)


#-----------------------
# Aggregate list
#-----------------------
ALL_MODELS = [Value_Model, Growth_Model, Dividend_Model, Momentum_Model]