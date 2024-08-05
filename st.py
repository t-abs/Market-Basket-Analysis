import streamlit as st
import pandas as pd
from itertools import combinations

def load_data(file_path):
    df = pd.read_csv(file_path)
    transactions = df.apply(lambda row: row.dropna().tolist(), axis=1).tolist()
    return transactions

def get_itemsets(transactions, length):
    itemsets = set()
    for transaction in transactions:
        for item in combinations(sorted(transaction), length):
            itemsets.add(item)
    return itemsets

def get_support(itemsets, transactions):
    itemset_counts = {itemset: 0 for itemset in itemsets}
    for transaction in transactions:
        transaction_set = set(transaction)
        for itemset in itemsets:
            if set(itemset).issubset(transaction_set):
                itemset_counts[itemset] += 1
    total_transactions = len(transactions)
    return {itemset: count / total_transactions for itemset, count in itemset_counts.items()}

def apriori(transactions, min_support):
    itemsets = get_itemsets(transactions, 1)
    frequent_itemsets = {}
    k = 1
    
    while itemsets:
        itemset_support = get_support(itemsets, transactions)
        itemsets = set(itemset for itemset, support in itemset_support.items() if support >= min_support)
        
        if not itemsets:
            break
        
        frequent_itemsets[k] = itemsets
        k += 1
        itemsets = get_itemsets(transactions, k)
    
    return frequent_itemsets

# Streamlit app
st.title('Market Basket Analysis with Custom Apriori Algorithm')

# Define the path to the CSV file
file_path = 'market.csv'

# Load and preprocess data
transactions = load_data(file_path)

# Display a preview of the data
st.write("Data Preview:")
st.write(pd.DataFrame(transactions).head())

# Apply Apriori algorithm
min_support = st.slider('Minimum Support', 0.0, 0.1, 0.0045, step=0.0001)
frequent_itemsets = apriori(transactions, min_support)

# Display results
if not frequent_itemsets:
    st.write('No itemsets found.')
else:
    st.write('Frequent Itemsets:')
    for length, itemsets in frequent_itemsets.items():
        st.write(f"**Itemsets of length {length}:**")
        for itemset in itemsets:
            support = get_support({itemset}, transactions)[itemset]
            st.write(f"**Itemset:** {itemset}")
            st.write(f"**Support:** {support:.4f}")
            st.write("-----------------------------------------------------")
