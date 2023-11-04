"""
Created on 08-09-2012

@author: Maciej Wasilak
"""

import sys
from ipaddress import ip_address

from twisted.internet import reactor
from twisted.python import log

import txthings.coap as coap
import txthings.resource as resource


class Agent:
    """
    Example class which performs single GET request to coap.me
    port 5683 (official IANA assigned CoAP port), URI "test".
    Request is sent 1 second after initialization.

    Remote IP address is hardcoded - no DNS lookup is preformed.

    Method requestResource constructs the request message to
    remote endpoint. Then it sends the message using protocol.request().
    A deferred 'd' is returned from this operation.

    Deferred 'd' is fired internally by protocol, when complete response is received.

    Method printResponse is added as a callback to the deferred 'd'. This
    method's main purpose is to act upon received response (here it's simple print).
    """

    def __init__(self, protocol, host):
        self.protocol = protocol
        self.host = host
        reactor.callLater(1, self.requestResource)

    def requestResource(self):
        request = coap.Message(code=coap.GET)
        # Send request to "coap://coap.me:5683/time"
        request.opt.uri_path = (b'time',)
        request.opt.observe = 0

        # ---------------------------- added by johirul ---------------------------- #
        if sys.version_info.major == 2:
            # -- python 2
            request.remote = (ip_address(unicode(self.host)), coap.COAP_PORT)      
        else:
            # -- python 3
            request.remote = (ip_address(self.host), coap.COAP_PORT)
        # ----------------------------x----------------x---------------------------- #
        
        d = protocol.request(request, observeCallback=self.printLaterResponse)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)

    def printResponse(self, response):
        
        # ---------------------------- added by johirul ---------------------------- #
        if sys.version_info.major == 2:
            # -- python 2
            payload = response.payload
        else:
            # -- python 3
            payload = response.payload.decode()
        # ----------------------------x----------------x---------------------------- #

        print('First result: ' + payload)
        # reactor.stop()

    def printLaterResponse(self, response):
        
        # ---------------------------- added by johirul ---------------------------- #
        if sys.version_info.major == 2:
            # -- python 2
            payload = response.payload
        else:
            # -- python 3
            payload = response.payload.decode()
        # ----------------------------x----------------x---------------------------- #

        print('Observe result: ' + payload)

    def noResponse(self, failure):
        print('Failed to fetch resource:')
        print(failure)
        # reactor.stop()


log.startLogging(sys.stdout)

endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
client = Agent(protocol, host='127.0.0.1')

reactor.listenUDP(61616, protocol)  # , interface="::")
reactor.run()
