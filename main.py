import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

df = pd.read_excel("Annual_Money_and_Banking.xlsx", skiprows=6)
#dropping the first 2 junk columns
df = df.drop(df.columns[[0,1]], axis=1).dropna(how="all")
# Renaming the first remaining column to Items
df = df.rename(columns={df.columns[0]: "Items"})
#setting items as Index
df = df.set_index("Items")
#Filtering only India columns
india_df = df.filter(regex=r"India")
#india_df.to_excel("cleaned_india_data.xlsx", index=True)
start_year = 2025
num_cols = india_df.shape[1] - 1
year_labels = [f"{col.split('.')[0]} {start_year - i}" for i, col in enumerate(india_df.columns)]
india_df.columns = year_labels
#Visualizzation code for currency in circulation 
currency = india_df.loc["Currency in Circulation"].copy() / 1000000  # Lakh crores
m3 = india_df.loc["Broad Money"].copy() / 1000000  # Lakh crores

# Convert index labels like "India 2025" -> years and sort ascending for consistent plotting
def to_year_series(s):
    years = pd.Index([int(lbl.split()[-1]) for lbl in s.index], name="Year")
    return pd.Series(s.values, index=years).sort_index()

currency = to_year_series(currency)
m3 = to_year_series(m3)

# Plot both lines on the same graph
plt.figure(figsize=(10, 6))
plt.plot(currency.index, currency.values, marker='o', linestyle='-', color='teal', label="Currency in Circulation")
plt.plot(m3.index, m3.values, marker='s', linestyle='-', color='orange', label="Broad Money (M3)")

# Mirror (right-side) view
#plt.gca().invert_xaxis()

# Axis formatting
plt.title("India – Currency in Circulation vs Broad Money (M3)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Value in ₹ Lakh crores", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)

# Avoid scientific notation like 1e7
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(style='plain', axis='y')

# Legend and instruction
plt.legend(loc="upper left")
plt.figtext(
    0.5, 0.01,
    "Instruction: The legend identifies each line. Currency in Circulation is physical cash; M3 includes currency + deposits\n" \
    " Data Source: RBI Annual Report 2001-25, Yahoo Finance (USD/INR)",
    
    ha="center", fontsize=9, color="dimgray"
)

# Leave space for figtext
plt.tight_layout(rect=(0, 0.05, 1, 1))

#We'll measure : 1) Pre-2014(before the govt change)
#2) Plost-2014 (after the change)
#3) Urjit patel's tenure (sept2016 - december 2018)
#4) After Patel (2019 onwards)
#For each window well calculate the linear slope -> lakh crores per year change,
#cagr-> %growth per year 
def slope_per_year(years, values):
    m, _ = np.polyfit(years, values, 1)
    return m

def cagr(start_val, end_val, start_year, end_year):
    n = end_year - start_year
    if n <= 0 or start_val <= 0:
        return np.nan
    return (end_val / start_val) ** (1 / n) - 1

# Helper to slice by year range
def slice_range(series, start, end):
    return series[(series.index >= start) & (series.index <= end)]
# -------------------Windows of interest -------------------    
windows = {
    "Pre-2014": (2000, 2014),
    "Post-2014": (2015, 2025),
    "Urjit Patel": (2016, 2018),
    "After Patel": (2019, 2025)
}

def annotate_window(series, start, end, color):
    sub = slice_range(series, start, end)
    if len(sub) >= 2:
        slope = slope_per_year(sub.index.values, sub.values)
        growth = cagr(sub.iloc[0], sub.iloc[-1], sub.index[0], sub.index[-1])
        # Print to terminal
        print(f"{start}-{end} – {color}: slope={slope:.2f} ₹ Lakh crores/year, CAGR={growth*100:.2f}%")
        # Annotate on plot
        mid_year = sub.index[len(sub)//2]
        mid_val = sub.values[len(sub)//2]
        plt.text(mid_year, mid_val,
                 f"{slope:.2f} ₹ Lakh cr/yr\n{growth*100:.2f}%",
                 fontsize=8, color=color, ha='center', va='bottom',
                 bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1))

for name, (start, end) in windows.items():
    annotate_window(currency, start, end, 'teal')
    annotate_window(m3, start, end, 'orange')
#--------------------Net Foreign Exchange Assets Change --------------------
rbi_fx = india_df.loc["Net Foreign Exchange Assets of the Central Bank"].copy() / 1_000_000
bank_fx = india_df.loc["Net Foreign Assets of Commercial Banks"].copy() / 1_000_000
total_fx_assets = rbi_fx + bank_fx

fx_change = to_year_series(total_fx_assets).diff()
plt.bar(fx_change.index, fx_change.values, color='purple', alpha=0.2, label='Net FX Asset Change')
plt.legend(loc="upper left", fontsize=10)
for year, val in fx_change.items():
    plt.text(year, val, f"{val:.1f}", ha='center', va='bottom', fontsize=7, color='purple', alpha=0.7)

#---------------------USD/INR exchange rate ---------------------------

try:
    usdinr_data = pd.read_csv("usdinr_data.csv", index_col=0, parse_dates=True)
    print("Loaded USD/INR data from local file.")
except FileNotFoundError:
    usdinr_data = yf.download("USDINR=X", start="2000-01-01", end="2025-12-31")
    usdinr_data.to_csv("usdinr_data.csv")
    print("Fetched USD/INR data from Yahoo Finance and saved locally.")


# --- Load manually edited USD/INR file ---
usdinr_df = pd.read_csv("usdinr_data.csv", parse_dates=["Date"], dayfirst=True)

# Extract year from Date
usdinr_df["Year"] = usdinr_df["Date"].dt.year

# Group by Year and take the average Close price
usdinr_annual = usdinr_df.groupby("Year")["Close"].mean()

ax1 = plt.gca()
ax2 = ax1.twinx()
ax2.plot(usdinr_annual.index, usdinr_annual.values,
         color='black', linestyle='--', marker='o', label="USD/INR Exchange Rate")
#ax2.set_ylabel("USD/INR Exchange Rate", fontsize=6)
# Define highlight periods as (start_year, end_year, color, alpha)
highlight_periods = [
    (2016, 2018, 'orange', 0.1),  # Patel era
    (2021, 2025, 'red', 0.1)      # Post-pandemic liquidity surge
]

# Loop through and shade
for start, end, color, alpha in highlight_periods:
    ax1.axvspan(start, end, color=color, alpha=alpha)
# --- Prepare aligned DataFrame for correlation ---


plt.show()
