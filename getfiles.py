import os
import blockchain
import json
import base64

b = blockchain.BlockChain()
b.load()
quit()
dirs = os.listdir()

for d in dirs:
    if os.path.isfile(d):
        file = open(d, "rb").read()

        format = d.split('.')
        print(f"Processing {d}, format: {format[1]}")

        b.create_work(json.dumps({"filename": d,
                                  "format": format,
                                  "data": str(base64.b16encode(file))
                                  }
                                 )
                      )

while len(b.unclaimed_work) > 0:
    b.mine(b.get_work())

print(f"Chain is valid? {b.validate_chain(b.chain)}")
b.save()
