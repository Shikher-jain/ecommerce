# backend.py
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enables CORS for frontend

# Load dataset (replace this file with your actual data)
df = pd.read_csv("ecommerce_data.csv")

# Basic cleaning
df = df.dropna()
df['total_sales'] = df['Quantity'] * df['Price']

@app.route('/api/sales', methods=['GET'])
def get_sales_data():
    grouped = df.groupby('Product Name').agg({
        'Quantity': 'sum',
        'Price': 'mean',
        'total_sales': 'sum'
    }).reset_index()

    data = []
    for _, row in grouped.iterrows():
        data.append({
            "product_name": row['Product Name'],
            "quantity": int(row['Quantity']),
            "price": float(row['Price']),
            "total_sales": float(row['total_sales'])
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
