# Import necessary libraries
import pandas as pd
import numpy as np

# Load all CSV files
orders = pd.read_csv('olist_orders_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv')
order_items = pd.read_csv('olist_order_items_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')
payments = pd.read_csv('olist_order_payments_dataset.csv')
reviews = pd.read_csv('olist_order_reviews_dataset.csv')

# Display the first few rows of each dataset to understand the structure
print("Orders Dataset:")
print(orders.head())
print("\nCustomers Dataset:")
print(customers.head())
print("\nOrder Items Dataset:")
print(order_items.head())
print("\nProducts Dataset:")
print(products.head())
print("\nPayments Dataset:")
print(payments.head())
print("\nReviews Dataset:")
print(reviews.head())

# Step 1: Clean the Orders Dataset
# Convert date columns to datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# Handle missing values in the Orders dataset
orders = orders.dropna(subset=['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date'])

# Step 2: Clean the Customers Dataset
# Check for duplicates and missing values
print("\nMissing values in Customers Dataset:")
print(customers.isnull().sum())
customers = customers.drop_duplicates()

# Step 3: Clean the Order Items Dataset
# Calculate total price for each item (price * quantity)
order_items['total_price'] = order_items['price'] * order_items['order_item_id']

# Step 4: Clean the Products Dataset
# Handle missing values in the Products dataset
print("\nMissing values in Products Dataset:")
print(products.isnull().sum())
products = products.dropna(subset=['product_category_name'])

# Step 5: Clean the Payments Dataset
# Check for missing values
print("\nMissing values in Payments Dataset:")
print(payments.isnull().sum())

# Step 6: Clean the Reviews Dataset
# Convert review dates to datetime
reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'])

# Handle missing values in the Reviews dataset
reviews = reviews.dropna(subset=['review_comment_message'])

# Step 7: Merge Datasets
# Merge Orders and Customers
merged_data = pd.merge(orders, customers, on='customer_id', how='inner')

# Merge with Order Items
merged_data = pd.merge(merged_data, order_items, on='order_id', how='inner')

# Merge with Products
merged_data = pd.merge(merged_data, products, on='product_id', how='inner')

# Merge with Payments
merged_data = pd.merge(merged_data, payments, on='order_id', how='inner')

# Merge with Reviews
merged_data = pd.merge(merged_data, reviews, on='order_id', how='inner')

# Step 8: Final Data Cleaning
# Drop unnecessary columns (if any)
merged_data = merged_data.drop(columns=['customer_zip_code_prefix', 'product_weight_g', 'product_length_cm', 
                                       'product_height_cm', 'product_width_cm', 'review_comment_title'])

# Handle missing values in the final merged dataset
print("\nMissing values in Merged Dataset:")
print(merged_data.isnull().sum())
merged_data = merged_data.dropna()

# Step 9: Save the Cleaned Data
merged_data.to_csv('cleaned_ecommerce_data.csv', index=False)

print("\nData cleaning and merging completed! Cleaned data saved as 'cleaned_ecommerce_data.csv'.")
print('cleaned_ecommerce_data.csv'.head())