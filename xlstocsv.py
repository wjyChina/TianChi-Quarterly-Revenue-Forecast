import pandas as pd
data=pd.read_excel('Balance Sheet.xls',index_col=0)
data.to_csv("Balance Sheet.csv",encoding='utf-8')