import psycopg2
import pandas as pd

con = psycopg2.connect(database="postgres", user="postgres", password="rucon2020", host="127.0.0.1", port="5432")
print("Database opened successfully")

cur = con.cursor()

userDataset = "cam-pennfudan-31Dec20"

#query = "SELECT * FROM meta_db WHERE datasetID LIKE '" + userDataset + "'";
query = "SELECT * FROM meta_db";


cur.execute(query)
data = cur.fetchall()

#cols = list(map(lambda x: x[0], cur.description))
#df = DataFrame(data, columns=cols)
col_names = []
for elt in cur.description:
    col_names.append(elt[0])

df = pd.DataFrame(data, columns=col_names)
print (df["datasetid"][0])
print (df.head())

#print df.iloc[0]['datasetid']
#for row in df.head().itertuples():
#    print row.datasetid

con.close()
