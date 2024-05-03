import pandas as pd
def feature_eng(df):
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df =df[df['UnitPrice']>0]
    df['Order_status']=df.InvoiceNo.apply(find_cancelled_transaction)
    df['Returned_order_qty']= df.Quantity.apply(returns)
    df.Quantity=df.Quantity.apply(dropneg)
    df.InvoiceDate = pd.to_datetime(df['InvoiceDate'])
    df['year'] = pd.to_datetime(df['InvoiceDate']).dt.year
    df['month'] = pd.to_datetime(df['InvoiceDate']).dt.month_name()
    max_date = pd.to_datetime('2011-12-09 12:50:00')
    customer_data = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()
    customer_data['InvoiceDate'] = pd.to_datetime(customer_data['InvoiceDate'])
    customer_data['Days_since_Most_rececnt_purchase'] = (max_date - customer_data['InvoiceDate']).dt.days
    customer_data['Total_transactions'] = df.groupby('CustomerID')['InvoiceNo'].count().reset_index(drop=True)
    customer_data['total_products_purchased'] = df.groupby('CustomerID')['Quantity'].sum().reset_index(drop=True)
    customer_data['Total_spend'] = df.groupby('CustomerID').apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum()).reset_index(drop=True)
    customer_data['Average_spend']=customer_data['Total_spend']/customer_data['Total_transactions']
    customer_data['Unique_products_purchased']= df.groupby('CustomerID')['StockCode'].nunique().reset_index(drop=True)
    ##
    # Sort the DataFrame by 'CustomerID' and 'InvoiceDate'
    df_sorted = df.sort_values(by=['CustomerID', 'InvoiceDate'])
    df_sorted['Days_between_transactions'] = df_sorted.groupby('CustomerID')['InvoiceDate'].diff().dt.days.dropna()
    #df_sorted.dropna(inplace= True,axis=0)
    average_days_between_transactions = df_sorted.groupby('CustomerID')['Days_between_transactions'].mean().reset_index(drop=True)

    # Assign the result to the 'Average_days_between_transactions' column in the customer_data DataFrame
    customer_data['Average_days_between_transactions'] = average_days_between_transactions
    customer_data.dropna(inplace=True)
    filtered_df = df[df['Order_status'] == 'cancelled']
    customer_data['Return_quantity']=filtered_df.groupby("CustomerID")['Returned_order_qty'].sum().reset_index(drop=True)
    customer_data.drop('Return_quantity',axis=1,inplace=True)
    Total_returned_orders=filtered_df.groupby("CustomerID")['InvoiceNo'].nunique().reset_index()
    Total_returned_orders.rename(columns={'InvoiceNo': 'Total_cancelled_transactions'}, inplace=True)
    customer_data=customer_data.merge(Total_returned_orders,on='CustomerID',how='left')
    customer_data['Total_cancelled_transactions'].fillna(0,inplace=True)
    customer_data['cancellation_rate']= customer_data['Total_cancelled_transactions']/customer_data['Total_transactions']
    return customer_data

def find_cancelled_transaction(x):
    x = str(x)  # Convert x to a string
    if x.startswith('C'):
        return 'cancelled'
    else:
        return 'Successful'
def returns(x):
    if x<0:
        return x*-1
    else:
        return 0    
def dropneg(x):
    if x <0:
        return 0
    else :
        return x
