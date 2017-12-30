import unittest
from iota import BadApiResponse, StrictIota, __version__
from iota import *
from six import binary_type, moves as compat, text_type

class TestIOTA(unittest.TestCase):

    uri = "http://p103.iotaledger.net:14700"
    # https://seeedy.tangle.works
    sender_seed = 'Y9CXVYQAJ9SLEY9DWRYEIBAUFYSHRYJHWBDMKDTKBNSZGWMEAYZIEP9ETLZUQKZ9RIG9QUJZUVAFQJMMN'
    receiver_seed = 'LI9HGSKOOIMOHDVDJXHDOKOIMLWSQQCOLAXBZDYUYSJZWVJANFMOROLBTMKK9NHHNHSHDPUSEATTI9IZW'
    receiver = 'ESJYJSXVXZZJGWCHDEZQHWWMZNHGJIBXPEENUGOBTNKKFINXSSB9PAWIUITRUCB9VMLLKCASHO99OYYJD'
    receiver_check = 'ESJYJSXVXZZJGWCHDEZQHWWMZNHGJIBXPEENUGOBTNKKFINXSSB9PAWIUITRUCB9VMLLKCASHO99OYYJDMWTVJXSLZ'
    sender = 'UVCRBLOFBJBABWIWXUKBOOCPZIKLQSEHDJBIRECGJJITPIEUUKQWBCOINCUMUPIIMVJPGFOAP9XRXNWXZ'
    sender_check = 'QXOPKXZWDDWAVHBT9R9SKADZFKAICA9CCPRUTJDUCJBRGCWKFDQQEBBDYOYZIHSLHGWMAARJSTGJXXUNXMIARSVBCD'

    def test_nodeinfo(self):
        #print(__version__)
        api = StrictIota(self.uri)
        node_info = api.get_node_info()
        #print(node_info)

    def test_findtransaction(self):
        addresses = [Address(self.sender_check), Address(self.receiver)]
        print(addresses)
        api = Iota(self.uri)
        transactions = api.find_transactions(addresses = addresses)
        print(transactions)
        trytes = api.get_trytes(transactions["hashes"])
        for trytestring in trytes["trytes"]:
                transaction = Transaction.from_tryte_string(trytestring)
                print(transaction.address, ": " , transaction.value, " bundlehash:", transaction.bundle_hash)

    def test_gen_seed(self):
        #source: https://forum.iota.org/t/installed-light-wallet-2-3-no-random-seed-generator-in-tools/1544/5
        from random import SystemRandom
        alphabet = u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        generator = SystemRandom()
        print('Generated Seed: ')
        seed = u''.join(generator.choice(alphabet) for _ in range(81))
        print(seed)
        api = Iota(self.uri, seed)
        api_response = api.get_new_addresses(0, 5)
        print('Generated Addresses: ')
        for addy in api_response['addresses']:
            print('Address: ', binary_type(addy).decode('ascii'))

    def test_s_sent_to_r(self):
        hasSent = False
        addresses = [Address(self.receiver_check)]
        api = Iota(self.uri)
        transactions = api.find_transactions(addresses = addresses)
        for hashe in transactions["hashes"]:
                print(hashe)
                bundles = api.get_bundles(hashe)
                for bundle in bundles["bundles"]:
                    txrec = bundle[0]
                    if txrec.address == self.receiver:
                        hasSent = True
                        print(txrec.address, ": ", txrec.tag)
        assert(hasSent)

    def test_received_value_tag(self):
        value = 20
        tag = 'Xkcd'
        addresses = [Address(self.receiver_check)]
        hasSent = False
        api = Iota(self.uri)
        transactions = api.find_transactions(addresses = addresses)
        for hashe in transactions["hashes"]:
                print(hashe)
                bundles = api.get_bundles(hashe)
                for bundle in bundles["bundles"]:
                    txrec = bundle[0]
                    if txrec.address == self.receiver and txrec.value == value and str(txrec.tag).startswith(tag.upper()):
                        hasSent = True
                        print(txrec.address, ": ", txrec.tag)
        assert(hasSent)

if __name__ == '__main__':
    unittest.main()