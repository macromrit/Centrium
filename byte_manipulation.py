from typing import Tuple, List
from merkle_tree import construct_merkle_tree

def returnBytesOfFile(file_path) -> Tuple:
    """
    This function's used to convert a given file to its raw binary(bytes format)
    then this returns a tuple of 2 elements
        -> raw binary data in Bytes format
        -> file's extension:
               this would be useful while reconstructing the byte code and 
               get the file back alive
    """
    try:
        with open(file_path, "rb") as jammer:
            byte_version = jammer.read()
    except (FileNotFoundError, PermissionError):
        raise Exception("File specified is not existent or read permission's not given for the file  !!!")
    
    return byte_version, file_path.strip().split(".")[-1]

def writeBytesOfFile(new_name: str, raw_byte_repr: bytes, file_extension: str) -> None:
    """
    the byte representation must be constructed to a file
    and file_extension is used to specify of which format the file is
    """
    with open(f'reconstructed_files/{new_name}.{file_extension}', "wb") as hammer:
        hammer.write(raw_byte_repr)

def split_into_chunks(byte_code: bytes, chunk_size: int = 50) -> List[bytes]:
    """
    the bytecode fed is splitted of chunk-sizes specified
    then put into a list which is returned
    chunk size by default is 11 bytes... it could be changed
    """
    res = list()

    for chunk in range(0, len(byte_code), chunk_size):
        # slicing chunks and putting in array which would end-up being 
        # the leaves of merkle tree
        res.append(byte_code[chunk: chunk+chunk_size]) 
    
    return res

def file_path_2_root_hash(file_path, chunk_size: int = 50):
    byte, ext = returnBytesOfFile(file_path)
    chunkiez = split_into_chunks(byte, chunk_size)
    root_hash = construct_merkle_tree(chunkiez)
    return root_hash, ext, chunk_size

def bytes_2_roothash(byte_data, chunk_size):
    chunkiez = split_into_chunks(byte_data, chunk_size)
    root_hash = construct_merkle_tree(chunkiez)
    return root_hash

if __name__ == "__main__":

    byte, ext = returnBytesOfFile("files_uploaded/Nqueens.png")
    byte2, ext = returnBytesOfFile("files_uploaded/sample.txt")
    # writeBytesOfFile("newfile", byte, ext)
    # print(len(byte[:100] + byte[:100]))
    chunkiez = split_into_chunks(byte)
    chunkiez2 = split_into_chunks(byte2)
    
    
    hash1 = construct_merkle_tree(chunkiez)
    
    hash2 = construct_merkle_tree(chunkiez2)

    print(hash1)
    print(len(hash2))
    print(hash2)
    # print(byte2)