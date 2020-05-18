import json
import electrum_pb2


# Using google protobuf results in all `bytes` fields being 3/4 their Base64 encoded JSON size
# Additionally, message sizes are smaller

request = electrum_pb2.GetMerkleProof(
    tx_hash=bytes.fromhex(
        "e41e875d21861a7f43168010b123895cb74116d5dfe009ac743265cb7495546a"
    )
)


# Response params
block_height = 450538
pos = 710
merkle = [
    "713d6c7e6ce7bbea708d61162231eaa8ecb31c4c5dd84f81c20409a90069cb24",
    "03dbaec78d4a52fbaf3c7aa5d3fccd9d8654f323940716ddf5ee2e4bda458fde",
    "e670224b23f156c27993ac3071940c0ff865b812e21e0a162fe7a005d6e57851",
    "369a1619a67c3108a8850118602e3669455c70cdcdb89248b64cc6325575b885",
    "4756688678644dcb27d62931f04013254a62aeee5dec139d1aac9f7b1f318112",
    "7b97e73abc043836fd890555bfce54757d387943a6860e5450525e8e9ab46be5",
    "61505055e8b639b7c64fd58bce6fc5c2378b92e025a02583303f69930091b1c3",
    "27a654ff1895385ac14a574a0415d3bbba9ec23a8774f22ec20d53dd0b5386ff",
    "5312ed87933075e60a9511857d23d460a085f3b6e9e5e565ad2443d223cfccdc",
    "94f60b14a9f106440a197054936e6fb92abbd69d6059b38fdf79b33fc864fca0",
    "2d64851151550e8c4d337f335ee28874401d55b358a66f1bafab2c3e9f48773d",
]

# JSON response
json_response = json.dumps({"merkle": merkle, "block_height": block_height, "pos": pos})
print(f"Size of json response message: {len(json_response)}")


# Protobuf response
merkle_proto = [bytes.fromhex(txid) for txid in merkle]
merkle_response = electrum_pb2.MerkleProof(
    height=int(block_height), merkle=merkle_proto, position=int(pos)
)
print(f"Size of protobuf response message: {merkle_response.ByteSize()}")
