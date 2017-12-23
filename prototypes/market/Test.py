import unittest
from iota import BadApiResponse, StrictIota, __version__
from iota import *

class TestIOTA(unittest.TestCase):

    uri = "http://p103.iotaledger.net:14700"
    receiver = 'ACESICDEEKYSTSBBKCXHGGBTFR9FGOMOWDAQJEI9ECTBBMKRFLMGAJXOQGSOOMODKPJKANVSEGIEYNNNA'
    receiver_check = 'ACESICDEEKYSTSBBKCXHGGBTFR9FGOMOWDAQJEI9ECTBBMKRFLMGAJXOQGSOOMODKPJKANVSEGIEYNNNAILGUG9RUX'
    sender = 'QXOPKXZWDDWAVHBT9R9SKADZFKAICA9CCPRUTJDUCJBRGCWKFDQQEBBDYOYZIHSLHGWMAARJSTGJXXUNX'

    def test_nodeinfo(self):
        print(__version__)
        api = StrictIota(self.uri)
        node_info = api.get_node_info()
        print(node_info)

    def test_findtransaction(self):
        addresses = [Address(self.sender), Address(self.receiver)]
        print(addresses)
        api = Iota(self.uri)
        transactions = api.find_transactions(addresses = addresses)
        print(transactions)
        trytes = api.get_trytes(transactions["hashes"])
        for trytestring in trytes["trytes"]:
                transaction = Transaction.from_tryte_string(trytestring)
                print(transaction.address, ": " , transaction.value, " bundlehash:", transaction.bundle_hash)

if __name__ == '__main__':
    unittest.main()