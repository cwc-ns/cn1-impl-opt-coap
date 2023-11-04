'''
Created on 08-09-2012
@author: Maciej Wasilak

Updated on 30-10-2021
@co-author: Johirul Islam
'''

import sys, time

from ipaddress import ip_address

from twisted.python import log
from twisted.internet import reactor

import txthings.coap as coap

'''
from adafruit_dht import read

from config import SLEEP, MODEL, PIN, CoAP_HOST, CoAP_PORT
'''

import random
from config import SLEEP

__author__ = 'Johirul Islam'


class DHTClient:
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

    # As DHTClient(protocol, CoAP_HOST, CoAP_PORT, uri, str(humidity)) is commented in main()
    
    """
    def __init__(self, protocol, host, port, uri, payload):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.uri = uri
        self.payload = payload
        reactor.callLater(1, self.requestResource)
    """

    def __init__(self, protocol, host, port):
        self.protocol = protocol
        self.host = host
        self.port = port
        
        self.next = "temperature"
        self.sleepRequired = False
        
        # send temperature / humidity
        reactor.callLater(0, self.requestResource)
        

    def requestResource(self):
        
        if self.next == "temperature":
            
            # read temperature 
            #temperature = read(MODEL, PIN, 'temperature')
            #temperature = round(temperature, 1)
            # ------------------------------------ #
            # since we do not have an actual hardware, therefore we can generate a random value for this            
            # now, pick a value with 1 decimal point in between 25.00 and 35.00 which can be treated as 
            # temperature data that is reading from a DHT22 sensor
            temperature = round(random.uniform(25.00, 35.00), 1)
            print("sending ... temperature # ", temperature)
            
            # URI for "coap://<host>:<port>/sensors/dht/temperature"
            #uri      = (b'sensors/dht/temperature')
            uri      = (b'sensors', b'dht', b'temperature', )
            self.uri = uri
            self.payload = str(temperature)
            
            self.next = "humidity"
            self.sleepRequired = False
            
        elif self.next == "humidity":
            
            # read humidity 
            #humidity = read(MODEL, PIN, 'humidity')
            #humidity = round(humidity, 1)
            # ------------------------------------ #
            # since we do not have an actual hardware, therefore we can generate a random value for this
            # now, pick a value with 1 decimal point in between 35.00 and 45.00 which can be treated as 
            # humidity data that is reading from a DHT22 sensor
            humidity = round(random.uniform(35.00, 45.00), 1)	
            print("sending ... humidity    # ", humidity)
            
            # URI for "coap://<host>:<port>/sensors/dht/humidity"
            uri      = (b'sensors', b'dht', b'humidity', )
    
            # Send request to "coap://<host>:<port>/sensors/dht/<temperature/humidity>"
            #DHTClient(protocol, CoAP_HOST, CoAP_PORT, uri, str(humidity))
            self.uri = uri
            self.payload = str(humidity)  
            
            self.next = "temperature"
            self.sleepRequired = True
        
        print("-------------------- CoAP  Request -------------------")
        print("host    :", self.host)
        print("port    :", self.port)
        print("URI     :", self.uri)
        print("payload :", self.payload)
        print("------------------------ ends ------------------------")
        
        request = coap.Message(code=coap.POST, payload=self.payload)        
        request.opt.uri_path = self.uri        
        request.opt.observe = 0
        
        # bypass following error --> 
        # ipaddress.AddressValueError: '192.168.1.128' does not appear 
        # to be an IPv4 or IPv6 address. Did you pass in a bytes (str in Python 2) instead of a unicode object?
        #request.remote = (ip_address(self.host), self.port)
        
        if sys.version_info.major == 2:
            # -- python 2
            request.remote = (ip_address(unicode(self.host)), self.port)
        else:
            # -- python 3
            request.remote = (ip_address(self.host), self.port)
        
        d = self.protocol.request(request, observeCallback=self.printLaterResponse)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)

    def printResponse(self, response):
        log.msg('response found. reading...')
        host, port = response.remote
        
        print("------------------- CoAP Response --------------------")
        print("host     : ", host)
        print("port     : ", port)
        
        if sys.version_info.major == 2:
            # -- python 2
            payload = response.payload
        else:
            # -- python 3
            payload = response.payload.decode()
            
        print("payload  : ", str(payload))
        print("------------------------ ends ------------------------")
        # reactor.stop()        
        
        if self.sleepRequired:
            time.sleep(SLEEP)
        
        # send temperature / humidity
        reactor.callLater(0, self.requestResource)
        

    def printLaterResponse(self, response):
        print('Observe result: ' + str(response.payload))
        

    def noResponse(self, failure):
        print('Failed to fetch resource:')
        print(failure)
        # reactor.stop()
    
    """    
    def sendRequest(self):
        # ---------------------------------------------------------------------- #        
        # read temperature 
        temperature = read(MODEL, PIN, 'temperature')
        temperature = round(temperature, 1)		
        print "temperature # ", temperature	
            
        # URI for "coap://<host>:<port>/sensors/dht/temperature"
        #uri      = (b'sensors/dht/temperature')
        uri      = (b'sensors', b'dht', b'temperature', )
    
        # Send request to "coap://<host>:<port>/sensors/dht/temperature"
        #DHTClient(protocol, CoAP_HOST, CoAP_PORT, uri, str(temperature))
        self.uri = uri
        self.payload = str(temperature)
        self.requestResource()
    
            
        # read humidity 
        humidity = read(MODEL, PIN, 'humidity')
        humidity = round(humidity, 1)	
        print "humidity    # ", humidity
            
        # URI for "coap://<host>:<port>/sensors/dht/temperature"
        uri      = (b'sensors', b'dht', b'humidity', )
    
        # Send request to "coap://<host>:<port>/sensors/dht/<temperature/humidity>"
        #DHTClient(protocol, CoAP_HOST, CoAP_PORT, uri, str(humidity))
        self.uri = uri
        self.payload = str(humidity)        
        self.requestResource()
        # /--------------------------------------------------------------------- #
    """


