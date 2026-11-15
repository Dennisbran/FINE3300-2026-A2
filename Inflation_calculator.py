import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Import data analysis and visualization libraries

# -------------------------
# Read and prepare CPI data for use in inflation calculator.
# -------------------------

cpi = pd.read_csv("CPI_Data.csv", skiprows=9, header=None)
cpi = cpi.iloc[:, :2]
cpi.columns = ["Date", "CPI"]
# Keep only the date and CPI columns and name them.
cpi["Date"] = pd.to_datetime(cpi["Date"])
cpi["CPI"] = pd.to_numeric(cpi["CPI"])
# Convert the dates and values to proper types.
cpi = cpi[cpi["Date"].dt.day == 1].reset_index(drop=True)
# Remove the two stray end-of-month rows so there is exactly one row per month.
cpi["Inflation"] = cpi["CPI"].pct_change(12) * 100
# Use pct_change to calculate the inflation from 12 months ago and multiply it by 100 to get it into percentage form for input into CPI graph.
# Date, CPI, and Inflation are all put into one dataframe for use in CPI graph and inflation calculator.

#-------------------------
# Take the CPI data and create a graph to visualize the data.
#-------------------------

print("Generating CPI graph...")

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(cpi["Date"], cpi["CPI"], color="blue", linewidth=2, label="CPI Level")
ax1.axhline(y=100, color="gray", linestyle=":", linewidth=1.5, label="Base Level (100)")
# This horizontal line is included as a reference line representing the CPI base, which is 2002 at 100.
ax1.set_xlabel("Year", fontsize=12)
ax1.set_ylabel("CPI Level (2002 = 100)", color="blue", fontsize=12)
ax1.tick_params(axis="y", labelcolor="blue")
# Make this first line blue to contrast the percentage change line that will be added.

ax2 = ax1.twinx()
ax2.plot(cpi["Date"], cpi["Inflation"], color="red", linewidth=1.5, alpha=0.8, label="Annual % Change")
ax2.set_ylabel("Annual Percentage Change (%)", color="red", fontsize=12)
ax2.tick_params(axis="y", labelcolor="red")
# Create a second y-axis because CPI levels and percentage changes use different scales.
# Make the second line a different color and alpha to distinguish it from the first line.

plt.title("Canada Consumer Price Index \nMonthly CPI Level and Annual Percentage Change", fontsize=14, pad=15)
# Create title and use \n to create a line break in the title for better readability.

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
# Legend creation.

ax1.xaxis.set_major_locator(mdates.YearLocator(10))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.tight_layout()
# Format graph further to increase readability and make it more visually appealing.

plt.savefig("cpi_graph.png", dpi=300, bbox_inches="tight")
# Set dpi to 300 and bbox_inches to tight to ensure high resolution and ensure no unnecessary outside space.
print("Graph saved as: cpi_graph.png")
# Print this to tell the user the name of the saved graph file.
print("Close the graph window to continue")
# Print this so the user doesn't think the program froze when the graph pops up.
plt.show()

# -------------------------
# User input
# -------------------------

print()
print("=" * 60)
print("       BANK OF CANADA STYLE INFLATION CALCULATOR")
print()

price = float(input("Enter price ($): "))
# Use float() to convert input into a number for use in calculations.
start_date = input("Enter first date (YYYY-MM): ")
end_date = input("Enter second date (YYYY-MM): ")
# User is prompted to input data in the format YYYY-MM to ensure it can be converted into a datetime object for use in calculations.

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
# Convert the date inputs into datetime objects for use in calculations.

# -------------------------
# Find CPI values
# -------------------------

start_row = cpi[(cpi["Date"].dt.year == start_date.year) & (cpi["Date"].dt.month == start_date.month)]
end_row = cpi[(cpi["Date"].dt.year == end_date.year) & (cpi["Date"].dt.month == end_date.month)]
# Take the user inputs and use them to find the corresponding rows in the CPI dataframe
# so that we can retrieve the corresponding CPI values for use in the calculations.

if start_row.empty or end_row.empty:
    raise SystemExit("\nOne or both of the dates are not in the CPI data. Please run the program again and enter dates between January, 1914 and September, 2026.")
# Included to perform validation on inputs, ensuring they are within the data set.

cpi_start = float(start_row.iloc[0]["CPI"])
cpi_end = float(end_row.iloc[0]["CPI"])
# Use iloc and ["CPI"] to select the corresponding CPI value from the CPI column.
# Use float() to ensure the values are usable in calculations.

# -------------------------
# Calculations
# -------------------------

new_price = price * (cpi_end / cpi_start)

difference = new_price - price
percentage_change = (difference / price) * 100

years = abs((end_date - start_date).days / 365.25)
# Use abs to ensure the output is non-negative.

if years > 0:
    annual_rate = (((cpi_end / cpi_start) ** (1 / years)) - 1) * 100
else:
    annual_rate = 0
# If/else statement is included to ensure that division by zero will not happen and cause an error.

# -------------------------
# Output
# -------------------------

start_text = start_date.strftime("%Y-%m")
end_text = end_date.strftime("%Y-%m")
# Use strftime to format the dates into a YYYY-MM format for output to the user.

print()
print("RESULTS")
print("-" * 60)
print(f"Original price in {start_text}: ${price:,.2f} CAD")
print(f"Equivalent price in {end_text}: ${new_price:,.2f} CAD")
print(f"Percentage change: {round(percentage_change, 2)}%")
print(f"Number of years: {round(years, 2)}")
print(f"Average annual rate of change: {round(annual_rate, 2)}%")
print(f"CPI in {start_text}: {round(cpi_start, 1)}")
print(f"CPI in {end_text}: {round(cpi_end, 1)}")
# Use round() to limit displayed numbers to a readable number of decimal places,
# but use :,.2f to ensure dollars round to the nearest penny and include a thousands separator.
# Use f-string to insert variables directly into the output text.