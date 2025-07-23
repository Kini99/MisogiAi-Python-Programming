sales_data = [
    ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)]),
    ("Q2", [("Apr", 1300), ("May", 1250), ("Jun", 1400)]),
    ("Q3", [("Jul", 1350), ("Aug", 1450), ("Sep", 1300)]),
]

# Total sales per quarter
total_sales_per_quarter = {
    quarter: sum(sales for _, sales in months)
    for quarter, months in sales_data
}
print("Total sales per quarter:", total_sales_per_quarter)

# Month with highest sales
highest_sales_month = max(
    (month for _, months in sales_data for month in months),
    key=lambda x: x[1]
)
print("Month with highest sales:", highest_sales_month)

# Flat list for monthly sales
monthly_sales_flat = [month for _, months in sales_data for month in months]
print("Flat monthly sales list:", monthly_sales_flat)

# Unpacking loops
print("\nQuarterly Sales Report:")
for quarter, months in sales_data:
    print(f"\n{quarter} Sales:")
    for month, sales in months:
        print(f"{month}: {sales}")
