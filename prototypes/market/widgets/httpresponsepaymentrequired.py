from django.http import HttpResponse
from . import walker

class HttpResponsePaymentRequired(HttpResponse):
    def __init__(self, widget_id):
        super(HttpResponsePaymentRequired, self).__init__()
        self.status_code = 402
        widget = walker.widget("widgets/widgets/"+widget_id+".json")
        resp = '<p>You have to pay ' + str(widget['value']) + '.<br/>Send them to \'leet124\'</p>'
        self.write(resp)
