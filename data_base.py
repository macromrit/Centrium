# test imports
'''
import merkle_tree
import byte_manipulation
import encrypt_decrypt
'''
# """"""""""""""""""""""""""""""""""""""""

import sqlite3

conn = sqlite3.connect('data_stored.db')

# cursor = conn.cursor()

# CREATE_TABLE_QUERY = '''
# CREATE TABLE IF NOT EXISTS INFO_BASE (
#     id INTEGER PRIMARY KEY,
#     file_name TEXT,
#     cypher_key BLOB NOT NULL,
#     chunk_size INT NOT NULL,
#     hash_value TEXT NOT NULL,
#     encrypted_data BLOB NOT NULL,
#     file_extension TEXT
# );
# '''

# cursor.execute(CREATE_TABLE_QUERY)

# # Commit and close the connection
# conn.commit()



# ++++++++++++++++++++++++++++++++++++++++++==+===
'''
# insertion and retrieval test

# step1: read a file and get its raw byte representation, split it chunkwise and compute its root hash
root_hash, ext, chunk_size = byte_manipulation.file_path_2_root_hash("files_uploaded/Nqueens.png", 50)

# step2: generate a key for encryption
key = encrypt_decrypt.generateKey()

# step3: encrypt the data
encrypted_data = encrypt_decrypt.encrypt(byte_manipulation.returnBytesOfFile("files_uploaded/Nqueens.png")[0], key)

# step4: get a name
name = input("Enter a name for your file: ")

# inserting values into db
cursor1 = conn.cursor()

INSERT_QUERY = """
INSERT INTO INFO_BASE (file_name, cypher_key, chunk_size, hash_value, encrypted_data, file_extension) 
VALUES (?, ?, ?, ?, ?, ?)
"""

cursor1.execute(INSERT_QUERY, 
                (name, key, chunk_size, root_hash, encrypted_data, ext))
# commit db
conn.commit()
'''

# read and write it back
# cursor2 = conn.cursor()

SELECT_QUERY = """
SELECT * FROM INFO_BASE WHERE file_name LIKE ?
"""

'''
cursor2.execute(SELECT_QUERY, ("%%",))
data_point = list(cursor2.fetchall())[0]

decrypt_it = encrypt_decrypt.decrypt(data_point[5], data_point[2])

with open(Fr'reconstructed_files/{data_point[1]}.{data_point[6]}', 'wb') as jammer:
    jammer.write(decrypt_it)

'''


from datetime import datetime


def current_date_time() -> str:
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the output
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def find_is_name_unique(file_name, conn) -> bool:
    cursor = conn.cursor()
    
    SELECT_QUERY = """
    SELECT file_name from INFO_BASE
    """

    cursor.execute(SELECT_QUERY)

    data_points = [ele[0] for ele in cursor.fetchall()]

    cursor.close()

    return file_name not in data_points


def insert_into_table(
        file_name: str,
        cypher_key: bytes,
        chunk_size: int,
        root_hash: str,
        encrypted_data: bytes,
        file_extension: str,
        conn
) -> None:
    cursor = conn.cursor()

    INSERT_QUERY = """
    INSERT INTO INFO_BASE 
    (file_name, cypher_key, chunk_size, hash_value, encrypted_data, file_extension, date) 
    VALUES (?, ?, ?, ?, ?, ?,  ?)
    """

    cursor.execute(INSERT_QUERY, (file_name,
                                  cypher_key,
                                  chunk_size,
                                  root_hash,
                                  encrypted_data,
                                  file_extension,
                                  current_date_time()))
    
    cursor.close()

    conn.commit()

def get_all_files(conn, like):
    cursor = conn.cursor()
    
    SELECT_QUERY = """
    SELECT * from INFO_BASE WHERE file_name LIKE ?
    """

    cursor.execute(SELECT_QUERY, (f"%{like}%",))

    data_points = list(cursor.fetchall())

    cursor.close()

    return data_points


if __name__ == "__main__":
    # test: insert
    '''
    name = "AUM"
    cypher_key = encrypt_decrypt.generateKey()
    chunk_size = 100

    data, ext = byte_manipulation.returnBytesOfFile("files_uploaded/Nqueens.png")

    encrpted_data = encrypt_decrypt.encrypt(data, cypher_key)

    chunks = byte_manipulation.split_into_chunks(data, chunk_size)

    hash_root = merkle_tree.construct_merkle_tree(chunks)

    insert_into_table(name, cypher_key, chunk_size, hash_root, encrpted_data, ext)
    '''
    # for i in get_all_files(conn):
    #     print(i[-1])