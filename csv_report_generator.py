import csv
import os

def generate_sales_summary(input_file, output_file):
    """
    Reads sales or transaction data from a CSV, calculates
    total revenue and averages, and exports a clean summary report.
    """
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    total_revenue = 0.0
    item_count = 0
    category_summary = {}

    try:
        with open(input_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = row.get('Item', 'Unknown')
                price = float(row.get('Price', 0.0))
                quantity = int(row.get('Quantity', 1))
                
                revenue = price * quantity
                total_revenue += revenue
                item_count += quantity
                
                category_summary[item] = category_summary.get(item, 0.0) + revenue

        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric / Item', 'Total Value'])
            writer.writerow(['Total Items Sold', item_count])
            writer.writerow(['Total Revenue ($)', f"{total_revenue:.2f}"])
            writer.writerow([])
            writer.writerow(['--- Item Breakdown ---', '---'])
            for item, rev in category_summary.items():
                writer.writerow([item, f"${rev:.2f}"])

        print(f"Summary successfully generated: {output_file}")

    except ValueError as ve:
        print(f"Data formatting error: {ve}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    # Test script run
    print("CSV Report Generator loaded. Ready to process files.")
