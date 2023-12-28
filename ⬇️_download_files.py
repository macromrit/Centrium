import streamlit as st
from data_base import get_all_files
import sqlite3
from encrypt_decrypt import decrypt
from merkle_tree import construct_merkle_tree
from byte_manipulation import bytes_2_roothash

# making a connection to db
# +++++++++++++++++++++++++++++
conn = sqlite3.connect('data_stored.db')
# +++++++++++++++++++++++++++++


st.set_page_config(
    page_title="Centrium",
    page_icon="🏛️"
)

st.header("Centrium 🏛️")
st.markdown("###### Share files globally 🧑🏻‍💻, without letting people know your identity 👽")

st.write("<br>",unsafe_allow_html=True)

file_name_search = st.text_input(
            "Search for files👇",
            placeholder="Enter the file's name that you are searching for",
        )

st.write("<br>", unsafe_allow_html=True)

to_display_files = get_all_files(conn, file_name_search)

if to_display_files:
    for id, file_name, cipher_key, chunk_size, hash_value, encrypted_data, file_extension, date in to_display_files:

        with st.expander("file-id:    {}".format(id), expanded=True):
            st.write("<br>", unsafe_allow_html=True)
            st.markdown("###### 😚 file-name:    {}".format(file_name+"."+file_extension))
            st.markdown("###### 🤪 file-extension:    {}".format(file_extension))
            
            # data being decrypted
            decrypted_data = decrypt(encrypted_data, cipher_key)

                    
            st.markdown("###### 🧐 file-size(bytes):    {} bytes".format(len(decrypted_data)))
            if date:
                st.markdown("###### 😇 upload-date(yyyy-mm-dd):    {}".format(date.split()[0]))
                st.markdown("###### 😎 upload-time(military):    {}".format(date.split()[-1]))

            decrypt_root_hash = bytes_2_roothash(decrypted_data, chunk_size)
            
            st.write("<br>", unsafe_allow_html=True)

            if decrypt_root_hash == hash_value:
                st.download_button(label="download {}".format(file_name+"."+file_extension), data=decrypted_data, file_name=(file_name+"."+file_extension))
                st.success("root hashes of previous and current merkle tree matched, file isn't corrupted", icon="🥳")
            else:
                # root hashes didn't match, file's corrupted
                st.download_button(label="download {}".format(file_name+"."+file_extension), data=decrypted_data, file_name=(file_name+"."+file_extension), disabled=True)
                st.error("""Root hashes of the previous merkle tree and current merkle tree
    didn't match 😬, file's corrupted!!!""", icon="🚨")
            
            st.write("<br>", unsafe_allow_html=True)
else:
    st.markdown("#### No files were found 😅")

