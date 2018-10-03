from iota import BadApiResponse, StrictIota, __version__
from iota import *

class Payment(object):
    def __init__(self, receiver):
        self.uri = "http://p103.iotaledger.net:14700"
        self.receiver = receiver

    def payed(self, tag, value):
        print(self.receiver, tag, value)
        addresses = [Address(self.receiver)]
        api = Iota(self.uri)
        transactions = api.find_transactions(addresses = addresses)
        for hashe in transactions["hashes"]:
                bundles = api.get_bundles(hashe)
                for bundle in bundles["bundles"]:
                    txrec = bundle[0]
                    if self.receiver.startswith(str(txrec.address)) and int(txrec.value) >= int(value) and str(txrec.tag).startswith(tag.upper()):
                        return True
        return False
