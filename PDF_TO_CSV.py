import fitz  
import pandas as pd

input_file1="EB_Redemption_Details"
input_file2="EB_Purchase_Details"
pdf1 = fitz.open(input_file1+".pdf")
pdf2 = fitz.open(input_file2+".pdf")
page_dataframe1=[]
page_dataframe2=[]
for i in pdf1:
  tabs1= i.find_tables()
  tab1=tabs1[0]
  pg_df1= tab1.to_pandas()  
  page_dataframe1.append(pg_df1)


for i in pdf2:
  tabs2= i.find_tables()
  tab2=tabs2[0]
  pg_df2= tab2.to_pandas()  
  page_dataframe2.append(pg_df2)

df1=pd.concat(page_dataframe1)
df2=pd.concat(page_dataframe2)
df1.to_csv(f"{input_file1}.csv", index=False)
df2.to_csv(f"{input_file2}.csv", index=False)