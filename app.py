import os
import csv
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# File names used in the application
USER_DATA_FILE = "users.csv"
BRANCH_DATA_FILE = "branches.csv"
PRODUCT_DATA_FILE = "products.csv"
SALES_DATA_FILE = "sales.csv"

########## Factory Pattern ##########

# Abstract class for data loaders
class AbstractDataLoader:
    def load_data(self):
        raise NotImplementedError

# Implementation for loading CSV files
class CSVDataLoader(AbstractDataLoader):
    def __init__(self, file_name):
        self.file_name = file_name
    
    def load_data(self):
        data = []
        if os.path.exists(self.file_name):
            with open(self.file_name, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    data.append(row)
        return data

# Factory class to create data loaders
class DataLoaderCreator:
    @staticmethod
    def create_loader(file_name):
        if file_name.endswith('users.csv'):
            return CSVDataLoader(file_name)
        elif file_name.endswith('branches.csv'):
            return CSVDataLoader(file_name)
        elif file_name.endswith('products.csv'):
            return CSVDataLoader(file_name)
        elif file_name.endswith('sales.csv'):
            return CSVDataLoader(file_name)
        else:
            raise ValueError("Unsupported file type")

########## Command Pattern ##########

# Abstract command base class
class AbstractCommand:
    def execute(self):
        raise NotImplementedError

# Command for adding a new branch
class RegisterBranchCommand(AbstractCommand):
    def execute(self):
        print("\n<<<< Register a New Branch >>>>")
        branches_data = load_data(BRANCH_DATA_FILE)
        
        branch_id = input("Enter Branch ID: ")
        branch_name = input("Enter Branch Name: ")
        branch_location = input("Enter Location: ")

        new_branch_entry = [branch_id, branch_name, branch_location]
        branches_data.append(new_branch_entry)

        os.remove(BRANCH_DATA_FILE)

        headers = ['Branch ID', 'Branch Name', 'Location']
        save_data(BRANCH_DATA_FILE, branches_data, headers=headers)
        print(f"Branch {branch_name} has been successfully added.")

# Command for adding a new sale
class RecordSaleCommand(AbstractCommand):
    def execute(self):
        print("\n<<<< Record a New Sale >>>>")
        sales_data = load_data(SALES_DATA_FILE)
        
        branch_id = input("Enter Branch ID: ")
        product_id = input("Enter Product ID: ")
        amount_sold = input("Enter Amount Sold: ")

        new_sale_entry = [branch_id, product_id, amount_sold, datetime.now().strftime('%Y-%m-%d')]
        sales_data.append(new_sale_entry)

        os.remove(SALES_DATA_FILE)

        headers = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
        save_data(SALES_DATA_FILE, sales_data, headers=headers)
        print("The sale has been successfully recorded.")

# Command for monthly sales analysis of a branch
class BranchMonthlySalesAnalysisCommand(AbstractCommand):
    def __init__(self, branch_id):
        self.branch_id = branch_id
    
    def execute(self):
        analyze_monthly_sales(self.branch_id)

# Command for price analysis of a product
class ProductPriceAnalysisCommand(AbstractCommand):
    def __init__(self, product_id):
        self.product_id = product_id
    
    def execute(self):
        analyze_price(self.product_id)

# Command for weekly sales analysis of the network
class NetworkWeeklySalesAnalysisCommand(AbstractCommand):
    def execute(self):
        analyze_weekly_sales()

# Command for total sales amount analysis
class TotalSalesAnalysisCommand(AbstractCommand):
    def execute(self):
        analyze_total_sales_amount()

# Command for monthly sales analysis across all branches
class AllBranchesMonthlySalesAnalysisCommand(AbstractCommand):
    def execute(self):
        analyze_all_branches_monthly_sales()

########## Utility Functions ##########

# Load data from a specified CSV file
def load_data(file_name):
    loader = DataLoaderCreator.create_loader(file_name)
    return loader.load_data()

# Save data to a specified CSV file
def save_data(file_name, data, headers=None):
    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists and headers:
            writer.writerow(headers)
        writer.writerows(data)

# Handle user login process
def login_user():
    print("<<<< User Login >>>>")
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

# Perform monthly sales analysis for a specific branch
def analyze_monthly_sales(branch_id):
    print(f"\n<<<< Monthly Sales Analysis for Branch {branch_id} >>>>")
    sales_data = load_data(SALES_DATA_FILE)
    branch_sales = [int(sale[2]) for sale in sales_data if sale[0] == branch_id]

    if not branch_sales:
        print(f"No sales information is present for Branch ID{branch_id}.")
        return

    plt.figure(figsize=(8, 5))
    plt.hist(branch_sales, bins=10, edgecolor='black')
    plt.title(f'Monthly Sales Analysis for Branch {branch_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Perform price analysis for a specific product
def analyze_price(product_id):
    print(f"\n<<<< Product Price Analysis for Product {product_id} >>>>")
    sales_data = load_data(SALES_DATA_FILE)
    product_sales = [int(sale[2]) for sale in sales_data if sale[1] == product_id]

    if not product_sales:
        print(f"No sales information is present for Product ID {product_id}.")
        return

    average_price = np.mean(product_sales)
    max_price = np.max(product_sales)
    min_price = np.min(product_sales)
    median_price = np.median(product_sales)

    print(f"Average Price: {average_price} LKR")
    print(f"Maximum Price: {max_price} LKR")
    print(f"Minimum Price: {min_price} LKR")
    print(f"Median Price: {median_price} LKR")

    # Plot boxplot for sales price distribution
    plt.figure(figsize=(8, 5))
    plt.boxplot(product_sales, vert=False)
    plt.title(f'Sales Price Distribution for Product {product_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.grid(True)
    plt.show()

# Perform weekly sales analysis for the network
def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Date format '{date_str}' is not recognized")

def analyze_weekly_sales():
    print("\n<<<< Weekly Sales Analysis for the Supermarket Network >>>>")
    sales_data = load_data(SALES_DATA_FILE)

    # Example: Analyze sales for the current week
    current_date = datetime.today()
    week_start = current_date - timedelta(days=current_date.weekday())
    week_end = week_start + timedelta(days=6)

    weekly_sales = [int(sale[2]) for sale in sales_data
                    if week_start <= parse_date(sale[3]) <= week_end]

    total_sales = sum(weekly_sales)
    average_sales = np.mean(weekly_sales) if weekly_sales else 0

    print(f"Weekly Sales Total: {total_sales} LKR")
    print(f"Average Sales per Day: {average_sales} LKR")

# Analyze the total amount of sales
def analyze_total_sales_amount():
    print("\n<<<< Total Sales Revenue Analysis >>>>")
    sales_data = load_data(SALES_DATA_FILE)
    total_sales = sum([int(sale[2]) for sale in sales_data])

    print(f"Overall Sales Revenue: {total_sales} LKR")

# Perform monthly sales analysis for all branches
def analyze_all_branches_monthly_sales():
    print("\n<<<< Monthly Sales Analysis for All Branches >>>>")
    sales_data = load_data(SALES_DATA_FILE)
    branch_data = load_data(BRANCH_DATA_FILE)
    
    monthly_sales_summary = {branch[0]: 0 for branch in branch_data}
    
    for sale in sales_data:
        branch_id = sale[0]
        monthly_sales_summary[branch_id] += int(sale[2])
    
    branch_ids, sales_amounts = zip(*monthly_sales_summary.items())
    
    plt.figure(figsize=(10, 6))
    plt.bar(branch_ids, sales_amounts)
    plt.title('Monthly Sales Summary for All Branches')
    plt.xlabel('Branch ID')
    plt.ylabel('Total Sales (LKR)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

########## Main Program ##########
# Main function to execute the program
def main():
    # Ensure required CSV files exist and are initialized with headers
    headers_users = ['Username', 'Password']
    if not os.path.exists(USER_DATA_FILE):
        save_data(USER_DATA_FILE, [], headers=headers_users)

    headers_branches = ['Branch ID', 'Branch Name', 'Location']
    if not os.path.exists(BRANCH_DATA_FILE):
        save_data(BRANCH_DATA_FILE, [], headers=headers_branches)

    headers_products = ['Product ID', 'Product Name']
    if not os.path.exists(PRODUCT_DATA_FILE):
        save_data(PRODUCT_DATA_FILE, [], headers=headers_products)

    headers_sales = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
    if not os.path.exists(SALES_DATA_FILE):
        save_data(SALES_DATA_FILE, [], headers=headers_sales)

    # User login loop
    while True:
        if login_user():
            print("Login successful!")
            break
        else:
            print("Invalid username or password. Please try again.")

    # Command mapping
    command_map = {
        '1': RegisterBranchCommand,
        '2': RecordSaleCommand,
        '3': BranchMonthlySalesAnalysisCommand,
        '4': ProductPriceAnalysisCommand,
        '5': NetworkWeeklySalesAnalysisCommand,
        '6': TotalSalesAnalysisCommand,
        '7': AllBranchesMonthlySalesAnalysisCommand,
        '8': lambda: print("Logged out.")
    }

    # Main menu loop
    while True:
        print("\n<<<< Main Menu >>>>")
        print("1. Register a New Branch")
        print("2. Record a New Sale")
        print("3. Monthly Sales Analysis for a Specific Branch")
        print("4. Product Price Analysis")
        print("5. Weekly Sales Analysis for the Network")
        print("6. Total Sales Amount Analysis")
        print("7. Monthly Sales Analysis for All Branches")
        print("8. Log Out")

        user_choice = input("Enter your option (1-8): ")

        if user_choice in command_map:
            if user_choice == '8':
                command_map[user_choice]()  # Handle logout directly
                break
            else:
                if user_choice in ['3', '4']:
                    param = input(f"Enter {'Branch ID' if user_choice == '3' else 'Product ID'}: ")
                    command = command_map[user_choice](param)
                else:
                    command = command_map[user_choice]()
                command.execute()
        else:
            print("Invalid option. Please choose a number from 1 to 8")

# Run the main program
main()           