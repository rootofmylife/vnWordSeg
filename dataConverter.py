import sqlite3
import pandas as pd

conn = sqlite3.connect('./my_data.db')
c = conn.cursor()

c.execute('''CREATE TABLE dict (word text, POS text, definition text)''')

users = pd.read_csv('/Users/ducdo/Downloads/full_dic.tsv', sep='\t')

# write the data to a sqlite table
users.to_sql('dict', conn, if_exists='append', index = False)