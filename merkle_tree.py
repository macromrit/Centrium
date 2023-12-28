# Python code for implemementing Merkle Tree 
from typing import List
import hashlib
"""

	def hash(val: str):
		sha256_hash = hashlib.sha256()
		sha256_hash.update(val)
		hash_hex = sha256_hash.hexdigest()
        print(hash_hex)
		
        

			# 	# Create a SHA-256 hash object
        # sha256_hash = hashlib.sha256()
        # # Update the hash object with your binary data
        # sha256_hash.update(val)

        # # Get the hexadecimal representation of the hash
        # hash_hex = sha256_hash.hexdigest()
		
        # return hash_hex
"""

# class Node:

# 	def __init__(self, left, right, value: str, content, is_copied=False) -> None:
# 		self.left: Node = left
# 		self.right: Node = right
# 		self.value = value
# 		self.content = content
# 		self.is_copied = is_copied	

# 	def __str__(self):
# 		return (str(self.value))

# 	def copy(self):
# 		"""
# 		class copy function
# 		"""
# 		return Node(self.left, self.right, self.value, self.content, True)
	
class Node:
	def __init__(self, left, right, value, content, is_copied=False):
		self.left = left
		self.right = right
		self.value = value # hash values at each node
		self.content = str(content) # content at each node
		self.is_copied = is_copied
	
	# @staticmethod
	# def hash(val):
	# 	sha256_hash = hashlib.sha256()
	# 	sha256_hash.update(val)
	# 	hash_hex = sha256_hash.hexdigest()

	# 	return hash_hex
	
	@staticmethod
	def hash(val: str) -> str: 
		return hashlib.sha256(str(val).encode('utf-8')).hexdigest()

	def __str__(self):
		return (str(self.value))

	def copy(self):
		"""
		class copy function
		"""
		return Node(self.left, self.right, self.value, self.content, True)


class MerkleTree:
	def __init__(self, values: List[str]) -> None:
		self.__buildTree(values)

	def __buildTree(self, values: List[str]) -> None:

		leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
		if len(leaves) % 2 == 1:
			leaves.append(leaves[-1].copy()) # duplicate last elem if odd number of elements
		self.root: Node = self.__buildTreeRec(leaves)

	def __buildTreeRec(self, nodes: List[Node]) -> Node:
		if len(nodes) % 2 == 1:
			nodes.append(nodes[-1].copy()) # duplicate last elem if odd number of elements
		half: int = len(nodes) // 2

		if len(nodes) == 2:
			return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)

		left: Node = self.__buildTreeRec(nodes[:half])
		right: Node = self.__buildTreeRec(nodes[half:])
		value: str = Node.hash(left.value + right.value)
		content: str = f'{left.content}+{right.content}'
		return Node(left, right, value, content)

	def printTree(self) -> None:
		self.__printTreeRec(self.root)
		
	def __printTreeRec(self, node: Node) -> None:
		if node != None:
			if node.left != None:
				print("Left: "+str(node.left))
				print("Right: "+str(node.right))
			else:
				print("Input")
				
			if node.is_copied:
				print('(Padding)')
			print("Value: "+str(node.value))
			print("Content: "+str(node.content))
			print("")
			self.__printTreeRec(node.left)
			self.__printTreeRec(node.right)

	def getRootHash(self) -> str:
	    return self.root.value



def construct_merkle_tree(elems: list) -> str:
	'''
	bytecodes which were splitted into chunks
	are sent thru the merkle tree as a sequence
	which are treated as leaves then the root hash is constructed
	'''

	#as there are odd number of inputs, the last input is repeated
	# print("Inputs: ")
	# print(*elems, sep=" | ")
	# print("")
	mtree = MerkleTree(elems)
	# print("Root Hash: "+mtree.getRootHash()+"\n")
	# mtree.printTree()
	return mtree.getRootHash()


if __name__ == "__main__":
    construct_merkle_tree("Geeks for Geeks is gr8".split())
