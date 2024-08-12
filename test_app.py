import pytest
import os
import csv
from datetime import datetime
from unittest.mock import patch, MagicMock
from app import (load_data, save_data, login_user, analyze_monthly_sales, analyze_price, analyze_weekly_sales, analyze_total_sales_amount, analyze_all_branches_monthly_sales,
                 RegisterBranchCommand, RecordSaleCommand, BranchMonthlySalesAnalysisCommand, ProductPriceAnalysisCommand, NetworkWeeklySalesAnalysisCommand,
                 TotalSalesAnalysisCommand, AllBranchesMonthlySalesAnalysisCommand)

# Constants for test files
TEST_USER_FILE = "test_users.csv"
TEST_BRANCHES_FILE = "test_branches.csv"
TEST_PRODUCTS_FILE = "test_products.csv"
TEST_SALES_FILE = "test_sales.csv"

# Helper function to clear test files
def clear_test_files():
    for file in [TEST_USER_FILE, TEST_BRANCHES_FILE, TEST_PRODUCTS_FILE, TEST_SALES_FILE]:
        if os.path.exists(file):
            os.remove(file)

# Helper function to initialize test files
def initialize_test_files():
    headers_users = ['Username', 'Password']
    data_users = [['testuser', 'testpass']]
    save_data(TEST_USER_FILE, data_users, headers=headers_users)

    headers_branches = ['Branch ID', 'Branch Name', 'Location']
    data_branches = [['1', 'Branch A', 'Location A']]
    save_data(TEST_BRANCHES_FILE, data_branches, headers=headers_branches)

    headers_products = ['Product ID', 'Product Name']
    data_products = [['1', 'Product A']]
    save_data(TEST_PRODUCTS_FILE, data_products, headers=headers_products)

    headers_sales = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
    data_sales = [['1', '1', '100', datetime.now().strftime('%Y-%m-%d')]]
    save_data(TEST_SALES_FILE, data_sales, headers=headers_sales)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    clear_test_files()
    initialize_test_files()
    yield
    clear_test_files()

def test_load_data():
    data = load_data(TEST_USER_FILE)
    assert len(data) == 1
    assert data[0] == ['testuser', 'testpass']

def test_save_data():
    new_data = [['2', 'Branch B', 'Location B']]
    save_data(TEST_BRANCHES_FILE, new_data)
    data = load_data(TEST_BRANCHES_FILE)
    assert len(data) == 2
    assert data[1] == ['2', 'Branch B', 'Location B']

def test_login_success():
    with patch('builtins.input', side_effect=['testuser', 'testpass']):
        assert login_user() == True

def test_login_failure():
    with patch('builtins.input', side_effect=['invaliduser', 'invalidpass']):
        assert login_user() == False

def test_analyze_monthly_sales():
    try:
        analyze_monthly_sales('1')
    except Exception as e:
        pytest.fail(f"analyze_monthly_sales raised an exception: {e}")

def test_analyze_price():
    try:
        analyze_price('1')
    except Exception as e:
        pytest.fail(f"analyze_price raised an exception: {e}")

def test_analyze_weekly_sales():
    try:
        analyze_weekly_sales()
    except Exception as e:
        pytest.fail(f"analyze_weekly_sales raised an exception: {e}")

def test_analyze_total_sales_amount():
    try:
        analyze_total_sales_amount()
    except Exception as e:
        pytest.fail(f"analyze_total_sales_amount raised an exception: {e}")

def test_analyze_all_branches_monthly_sales():
    try:
        analyze_all_branches_monthly_sales()
    except Exception as e:
        pytest.fail(f"analyze_all_branches_monthly_sales raised an exception: {e}")

@patch('app.input', side_effect=['2', 'Branch B', 'Location B'])
def test_register_branch_command(mock_input):
    command = RegisterBranchCommand()
    with patch('sys.stdout', new=MagicMock()):
        command.execute()
    # Ensure the new branch was added
    data = load_data(TEST_BRANCHES_FILE)
    assert len(data) == 2
    assert data[1] == ['2', 'Branch B', 'Location B']

@patch('app.input', side_effect=['1', '1', '200'])
def test_record_sale_command(mock_input):
    command = RecordSaleCommand()
    with patch('sys.stdout', new=MagicMock()):
        command.execute()
    # Ensure the new sale was added
    data = load_data(TEST_SALES_FILE)
    assert len(data) == 2
    assert data[1][:3] == ['1', '1', '200']

def test_branch_monthly_sales_analysis_command():
    command = BranchMonthlySalesAnalysisCommand('1')
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"BranchMonthlySalesAnalysisCommand raised an exception: {e}")

def test_product_price_analysis_command():
    command = ProductPriceAnalysisCommand('1')
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"ProductPriceAnalysisCommand raised an exception: {e}")

def test_network_weekly_sales_analysis_command():
    command = NetworkWeeklySalesAnalysisCommand()
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"NetworkWeeklySalesAnalysisCommand raised an exception: {e}")

def test_total_sales_analysis_command():
    command = TotalSalesAnalysisCommand()
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"TotalSalesAnalysisCommand raised an exception: {e}")

def test_all_branches_monthly_sales_analysis_command():
    command = AllBranchesMonthlySalesAnalysisCommand()
    try:
        command.execute()
    except Exception as e:
        pytest.fail(f"AllBranchesMonthlySalesAnalysisCommand raised an exception: {e}")
