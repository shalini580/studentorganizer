import pandas as pd

# Read the CSV file
price_df = pd.read_csv('natural_gas_prices.csv')

print(price_df.head())  # Just to verify the data loaded correctly
value = price_storage_contract(
    price_data=price_df,
    injection_dates=['2023-06-30','2023-07-31'],
    withdrawal_dates=['2023-10-31','2023-12-31'],
    injection_rate=500000, 
    withdrawal_rate=500000,
    max_volume=1_000_000,
    storage_cost_per_month=100_000,
    injection_cost_per_mmbtu=0.01,
    withdrawal_cost_per_mmbtu=0.01,
    transport_cost_per_event=50_000
)
print(f"Estimated contract value: ${value:,.2f}")
