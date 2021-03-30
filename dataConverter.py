import sqlite3
import pandas as pd

conn = sqlite3.connect('./my_fts_data_update.db')
c = conn.cursor()

c.execute('''CREATE VIRTUAL TABLE dict USING FTS5(word, POS, definition, images, videos, audios, notes, english, france, russia, chinese, japan, korea, spain)''')

users = pd.read_csv('/Users/ducdo/Downloads/full_dic.tsv', sep='\t')

# write the data to a sqlite table
users.to_sql('dict', conn, if_exists='append', index = False)

# Check if virtual table can update
# print('run')
# c.execute("UPDATE dict SET POS = 'updated' WHERE definition = '1. Con chữ thứ nhất của bảng chữ cái tiếng Việt: chữ a thường (a); viết A hoa (A) ; từ A đến Z (từ đầu đến cuối, đủ mọi thứ).'")

# conn.commit()