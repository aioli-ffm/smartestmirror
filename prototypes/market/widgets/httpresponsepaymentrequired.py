from django.http import HttpResponse
from . import walker


class HttpResponsePaymentRequired(HttpResponse):
    def __init__(self, widget_id):
        super(HttpResponsePaymentRequired, self).__init__()
        self.status_code = 402
        # TODO -> config file
        address = 'ESJYJSXVXZZJGWCHDEZQHWWMZNHGJIBXPEENUGOBTNKKFINXSSB9PAWIUITRUCB9VMLLKCASHO99OYYJDMWTVJXSLZ'
        widget = walker.widget("widgets/widgets/" + widget_id + ".json")
        resp = '<p>You have to pay ' + \
            str(widget['value']) + '.<br/>Send them to address \'' + \
            address + '\' with tag \'' + widget_id + '\'</p>'
        self.write(resp)
