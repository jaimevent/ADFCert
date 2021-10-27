"""

Sources:
https://www.section.io/engineering-education/how-to-create-a-blockchain-in-python/
https://github.com/SomayyehGholami/Implementing-Smart-Blockchain

"""

from time import time
import json
import hashlib

class Blockchain:
    def __init__(self):
       self.current_information = []
       self.chain = []

       # Create the genesis block
       self.new_block(previous_hash='1')

    def new_block(self, previous_hash):
        """
        Create a new Block in the Smart Blockchain
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'information': self.current_information,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_information = []

        self.chain.append(block)
        return block

    def new_information(self, information):
        """
        Creates a new information
        :param information: Your information
        :return: The index of the Block that will hold this information
        """
        if not self.find_information(information):
            self.current_information.append({'information': information })

            return self.last_block['index'] + 1
        else:
            return -1

    def find_information(self, information):
        for block in self.chain:
            for infoBlock in block["information"]:
                if infoBlock["information"] == information:
                    return True
        return False


    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
