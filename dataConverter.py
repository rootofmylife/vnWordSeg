import sqlite3
import pandas as pd

conn = sqlite3.connect('./my_fts_data.db')
c = conn.cursor()

c.execute('''CREATE VIRTUAL TABLE dict USING FTS5(word, POS, definition)''')

users = pd.read_csv('/Users/ducdo/Downloads/full_dic.tsv', sep='\t')

# write the data to a sqlite table
users.to_sql('dict', conn, if_exists='append', index = False)