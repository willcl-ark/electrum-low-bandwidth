"""Generate Request and Response messages using a few different encodings and compare
the size.
"""

import json

import cbor
import msgpack

import electrum_pb2

# Request parameters
txid = "e41e875d21861a7f43168010b123895cb74116d5dfe009ac743265cb7495546a"
block_height = 450538


json_request = (
    json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "blockchain.transaction.get_merkle",
            "params": [txid, block_height],
            "id": "0",
        }
    )
    + "\n"
)


protobuf_request = electrum_pb2.GetMerkleProof(tx_hash=bytes.fromhex(txid))

cbor_request = cbor.dumps(("blockchain.transaction.get_merkle", bytes.fromhex(txid)))

msgpack_request = msgpack.packb(
    ("blockchain.transaction.get_merkle", bytes.fromhex(txid))
)


# Response parameters
pos = 710
merkle_path = [
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

json_response = (
    json.dumps(
        {"jsonrpc": "2.0", "result": [merkle_path, block_height, pos], "id": "0",}
    )
    + "\n"
)

merkle_response = electrum_pb2.MerkleProof(
    height=int(block_height),
    merkle=[bytes.fromhex(txid) for txid in merkle_path],
    position=int(pos),
)

cbor_response = cbor.dumps(
    ([bytes.fromhex(txid) for txid in merkle_path], block_height, pos)
)

msgpack_response = msgpack.packb(
    ([bytes.fromhex(txid) for txid in merkle_path], block_height, pos)
)


# Results
w = 27  # width
print(f"{'Size of json request:':{w}}{len(json_request)}")
print(f"{'Size of protobuf request:':{w}}{protobuf_request.ByteSize()}")
print(f"{'Size of CBOR request:':{w}}{len(cbor_request)}")
print(f"{'Size of msgpack request:':{w}}{len(msgpack_request)}")
print(f"\n{'Size of json response:':{w}}{len(json_response)}")
print(f"{'Size of protobuf response:':{w}}{merkle_response.ByteSize()}")
print(f"{'Size of CBOR response:':{w}}{len(cbor_response)}")
print(f"{'Size of msgpack response:':{w}}{len(msgpack_response)}")

#########
# Results
#########

# Size of json request:      165
# Size of protobuf request:  34
# Size of CBOR request:      70
# Size of msgpack request:   70
#
# Size of json response:     805
# Size of protobuf response: 381
# Size of CBOR response:     384
# Size of msgpack response:  384
