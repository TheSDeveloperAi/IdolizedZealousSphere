import pandas as pd
# pandas_training.py
import numpy as np

import pandas as pd

# --- Section 1: Introduction to Pandas ---
# What is Pandas?
# Why use Pandas (DataFrames and Series)?
# Installation (Done already: pip install pandas)

# --- Section 2: Core Data Structures ---

# 2.1 Series: 1-dimensional labeled array
print("\n--- 2.1 Pandas Series ---")
# Creating a Series
s = pd.Series([1, 3, 5, np.nan, 6, 8]) # Need to import numpy as np for np.nan
print("Example Series:\n", s)

# Creating a Series with a custom index
s2 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print("\nSeries with custom index:\n", s2)

# Accessing elements
print("\nAccessing element 'b':", s2['b'])
print("Accessing element by position (0):", s2[0])

# Basic operations on Series
print("\nBasic operations:")
print("s + 2:\n", s + 2)


# 2.2 DataFrame: 2-dimensional labeled data structure with columns of potentially different types
print("\n--- 2.2 Pandas DataFrame ---")
# Creating a DataFrame from a dictionary
data = {
    'Column1': [1, 2, 3, 4],
    'Column2': ['A', 'B', 'C', 'D'],
    'Column3': [True, False, True, False]
}
df = pd.DataFrame(data)
print("Example DataFrame:\n", df)

# Creating a DataFrame with a custom index and specified columns
df2 = pd.DataFrame(data, index=['row1', 'row2', 'row3', 'row4'], columns=['Column2', 'Column1'])
print("\nDataFrame with custom index and column order:\n", df2)

# Understanding Index and Columns
print("\nDataFrame Index:", df.index)
print("DataFrame Columns:", df.columns)


# --- Section 3: Loading and Saving Data ---
print("\n--- 3. Loading and Saving Data ---")
# (Assume you have a sample.csv file)
# df_from_csv = pd.read_csv('sample.csv')
# print("\nDataFrame loaded from CSV:\n", df_from_csv.head())

# Saving a DataFrame to CSV
# df.to_csv('output.csv', index=False) # index=False to not write the DataFrame index as a column
# print("\nDataFrame saved to output.csv")


# --- Section 4: Exploring DataFrames ---
print("\n--- 4. Exploring DataFrames ---")
# (Using the example DataFrame 'df')
print("First 2 rows:\n", df.head(2))
print("\nLast 1 row:\n", df.tail(1))
print("\nDataFrame Info:\n")
df.info()
print("\nDescriptive Statistics:\n", df.describe())
print("\nShape of the DataFrame:", df.shape)
print("\nColumn names:", df.columns)
print("\nIndex values:", df.index)


# --- Section 5: Selecting Data ---
print("\n--- 5. Selecting Data ---")
# Selecting a single column
print("Select Column1:\n", df['Column1'])
print("\nSelect Column2 (another way):\n", df.Column2) # Access as attribute (if column name is a valid identifier)

# Selecting multiple columns
print("\nSelect Column1 and Column3:\n", df[['Column1', 'Column3']])

# Selecting rows by label using .loc[]
print("\nSelect row with index 0 using .loc[]:\n", df.loc[0]) # If using default numerical index
# If using custom index: print("\nSelect row 'row2' using .loc[]:\n", df2.loc['row2'])

# Selecting rows by integer position using .iloc[]
print("\nSelect row at integer position 1 using .iloc[]:\n", df.iloc[1])

# Selecting a specific value using .loc[]
# print("\nSelect value at row 'row3' and column 'Column1':", df2.loc['row3', 'Column1'])

# Selecting a specific value using .iloc[]
print("\nSelect value at integer position [2, 0]:", df.iloc[2, 0])

# Slicing rows using .loc[] (inclusive of end label)
# print("\nSlice rows from 'row1' to 'row3' using .loc[]:\n", df2.loc['row1':'row3'])

# Slicing rows using .iloc[] (exclusive of end integer position)
print("\nSlice rows from integer position 0 to 2 using .iloc[]:\n", df.iloc[0:2])

# Combining row and column selection
# print("\nSelect Column1 for rows 'row1' and 'row4':\n", df2.loc[['row1', 'row4'], 'Column1'])


# --- Section 6: Filtering Data ---
print("\n--- 6. Filtering Data ---")
# Filtering based on a condition
print("Rows where Column1 > 2:\n", df[df['Column1'] > 2])

# Filtering with multiple conditions (use & for AND, | for OR)
# print("\nRows where Column1 > 1 and Column2 is 'C':\n", df[(df['Column1'] > 1) & (df['Column2'] == 'C')])


# --- Section 7: Handling Missing Data ---
# print("\n--- 7. Handling Missing Data ---")
# (Using the example Series 's' with np.nan)
# print("Check for missing values:\n", s.isnull())
# print("\nCheck for non-missing values:\n", s.notnull())

# Dropping missing values
# print("\nSeries after dropping missing values:\n", s.dropna())

# Filling missing values
# print("\nSeries after filling missing values with 0:\n", s.fillna(0))


# --- Section 8: Data Cleaning and Preparation ---
# print("\n--- 8. Data Cleaning and Preparation ---")
# Renaming columns
# df_renamed = df.rename(columns={'Column1': 'NewColumn1', 'Column2': 'NewColumn2'})
# print("DataFrame with renamed columns:\n", df_renamed)

# Changing data types
# df['Column1'] = df['Column1'].astype(float)
# print("\nData type of Column1 after casting:", df['Column1'].dtype)

# Removing duplicates (if any)
# df_no_duplicates = df.drop_duplicates()
# print("\nDataFrame after removing duplicates:\n", df_no_duplicates)


# --- Section 9: Basic Operations and Aggregations ---
print("\n--- 9. Basic Operations and Aggregations ---")
# Calculating the sum of a column
print("Sum of Column1:", df['Column1'].sum())

# Calculating the mean of a column
print("Mean of Column1:", df['Column1'].mean())

# Applying a function to a column
# df['Column1_squared'] = df['Column1'].apply(lambda x: x**2)
# print("\nDataFrame with squared Column1:\n", df)

# Grouping data (example: if you had a 'Category' column and 'Sales' column)
# grouped_data = df.groupby('Category')['Sales'].sum()
# print("\nGrouped data (Sum of Sales by Category):\n", grouped_data)


# --- Section 10: Display and Formatting ---
print("\n--- 10. Display and Formatting ---")
# Controlling display options (e.g., maximum rows to display)
# pd.set_option('display.max_rows', 10)

# Using to_string() for terminal output formatting
# (Using the example DataFrame 'df' again)
print("DataFrame printed using to_string(index=False):\n", df.to_string(index=False))

# Using col_space and justify
print("\nDataFrame with col_space and justify:\n", df.to_string(index=False, col_space={'Column1': 10, 'Column2': 15}, justify={'Column1': 'right'}))


# --- Section 11: Putting it Together (Your Project Focus) ---
print("\n--- 11. Project Focus: Order Summary DataFrame ---")
# How to create a DataFrame from your customer_product_list
# How to calculate item totals, tax, etc. for each row
# How to format the output using to_string() parameters like col_space

# (Example: Simulate creating order_data similar to your project)
# simulated_order_data = [
#     {'Code': 'P101', 'Product name': 'Acrilico (fosco, black, 500ml)', 'Qty': 2, 'Total': '8.00', 'Tax': '0.80', 'total price + fees': '8.80'},
#     {'Code': 'P102', 'Product name': 'Acrilico (semibrilho, white, 1000ml)', 'Qty': 1, 'Total': '6.75', 'Tax': '1.01', 'total price + fees': '7.76'},
# ]
# df_order_summary = pd.DataFrame(simulated_order_data)
# print("\nSimulated Order Summary DataFrame:\n", df_order_summary.to_string(index=False))

# Practice formatting the simulated DataFrame to match your desired output


# --- End of Training Template ---