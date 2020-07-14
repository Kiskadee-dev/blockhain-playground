import hashlib
import json


class Block:
    def __init__(self):
        self.prev_hash = "GENESIS"
        self.zeros = 3
        self.data = []
        self.salt = 0

    def get_hash(self) -> str:
        computed_hash = hashlib.sha256(str(
            str(self.prev_hash) + str(self.data) + str(self.salt)).encode("utf-8"))
        return computed_hash.hexdigest()

    def serialize(self) -> dict:
        s = {
            "prev_hash": self.prev_hash,
            "zeros": self.zeros,
            "data": self.data,
            "salt": self.salt
        }
        return s


class BlockChain:
    def __init__(self):
        self.chain = []
        self.unclaimed_work = []
        self.claimed_work = []
        self.latest_hash = "GENESIS"

    def load(self) -> bool:
        with open("saved_chain.json", "r") as file:
            chain = json.load(file)
            for block in chain:
                b = Block()
                b.prev_hash = block['prev_hash']
                b.zeros = block['zeros']
                b.data = block['data']
                b.salt = block['salt']
                self.chain.append(b)
            file.close()
        if self.validate_chain(self.chain):
            print(f"Chain loaded: {len(self.chain)} blocks")
            return True
        else:
            print("Invalid chain")
            self.chain.clear()
            return False

    def save(self):
        with open("saved_chain.json", "w") as file:
            blocks = []
            for block in self.chain:
                blocks.append(block.serialize())
            json.dump(blocks, file)
            file.close()

    def create_work(self, data):
        b = Block()
        b.data = data
        b.prev_hash = ""
        self.unclaimed_work.append(b)
        print(f"Added block to the unclaimed pool")

    def get_work(self) -> Block:
        if len(self.unclaimed_work) > 0:
            work = self.unclaimed_work.pop()
            work.prev_hash = self.latest_hash
            self.claimed_work.append(work)
            return work

    def create_and_add_block(self, data) -> Block:
        b = Block()
        b.data = data
        if len(self.chain) > 1:
            b.prev_hash = self.chain[len(self.chain) - 1].get_hash()
        else:
            b.prev_hash = "GENESIS"
        self.mine(b)
        return Block

    def create_zeros(self, size: int) -> str:
        z = ""
        for i in range(size):
            z += '0'
        return z

    def mine(self, block: Block) -> Block:
        counter = 0
        while not block.get_hash().endswith(self.create_zeros(block.zeros)):
            counter += 1
            block.salt += 1
            if counter % 1000000 == 0:
                print(f"Computed hash {counter}: {block.get_hash()}")
        self.chain.append(block)
        print(f"Successfully mined a block: {block.get_hash()}")
        return block

    def validate_chain(self, chain: list) -> bool:
        for block in chain:
            if not self.validate_block(block):
                return False
        return True

    def validate_block(self, block: Block) -> bool:
        if block.prev_hash != "GENESIS" and len(self.chain) > 1:
            # Percorre a corrente para encontrar o bloco referente anterior
            for i in range(len(self.chain)):
                if self.chain[i].prev_hash == block.prev_hash:
                    # Se a hash do bloco anterior for diferente, esta corrente é inválida
                    if self.chain[i - 1].get_hash() != block.prev_hash:
                        return False
        elif not block.get_hash().endswith(self.create_zeros(block.zeros)):
            return False

        return True
