import streamlit as st
from data_base import insert_into_table, find_is_name_unique
import encrypt_decrypt
from byte_manipulation import bytes_2_roothash
import sqlite3
import re

st.set_page_config(
    page_title="Centrium",
    page_icon="🏛️"
)

def is_valid_file_name(file_name):
    '''
    this function checks whether a file name fed in
    satisfied the namings constraints of a variable 
    as the file shouldn't if stored locally shouldn't 
    create any issues with path.
    '''

    # Regular expression for a valid variable name
    pattern = re.compile(r'^[a-zA-Z_]\w*$')
    
    # Check if the string matches the pattern
    return bool(pattern.match(file_name))


# ++++++++++++
conn = sqlite3.connect('data_stored.db')
# ++++++++++++

# App's name +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
st.write("<br>", unsafe_allow_html=True)

st.header("Centrium 🏛️")
st.markdown("###### Share files globally 🧑🏻‍💻, without letting people know your identity 👽")
st.write("<br>",unsafe_allow_html=True)


# file submission form
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


with st.form("my_form", clear_on_submit=True):
    st.write("<br>", unsafe_allow_html=True)

    st.markdown("#### Upload a File")
    
    st.write("<ln>", unsafe_allow_html=True)
    
    # accepting file name - must be unique
    file_name = st.text_input(
            "Enter some text 👇",
            placeholder="file name shouldn't exist in central DB, file extension's not necessary",
        )
    
    st.write("<br>", unsafe_allow_html=True)

    chunk_size = st.slider('Decide the size of each chunk (in bytes) fed to the Merkle Tree 👇', 20, 300, step=20)

    st.write("<br>", unsafe_allow_html=True)

    # accepting file
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)
    if uploaded_file: # if a file has been uploaded, else its None
        bytes_data = uploaded_file.read()
        file_extension = uploaded_file.name.split(".")[-1]
        st.write(file_extension)

    st.write("<br>", unsafe_allow_html=True)

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

    st.write("<br>", unsafe_allow_html=True)

    if submitted:
        if uploaded_file and find_is_name_unique(file_name, conn) and is_valid_file_name(file_name):
            # raw byte data of the file
            data = bytes_data
            # generate a key
            cypher_key = encrypt_decrypt.generateKey()
            # encrypted data
            encrypted_data = encrypt_decrypt.encrypt(data, cypher_key)
            # file extension
            ext = file_extension
            # root-hash
            root_hash =  bytes_2_roothash(data, chunk_size)

            # inserting the data received to db and commiting the action
            insert_into_table(file_name, cypher_key, chunk_size, root_hash, encrypted_data, ext, conn)

            # if its a successful, display it
            st.success("File has been successfully uploaded to the central repo.", icon="🥳")

            st.balloons()
        
        else:
            # if file not uploaded, display the error behind it
            if not uploaded_file:
                st.error("File not uploaded. Make sure you do that 😬", icon="🚨")
            
            if not is_valid_file_name(file_name):
                st.error("File name has used an invalid naming convention. Stick to variable's naming convention 😟", icon="🚨")

            if not find_is_name_unique(file_name, conn):
                st.error(F"File name '{file_name}' already taken. Get an alternative 💔", icon="🚨")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# closing the connection
conn.close()