'''
Created on 08-09-2012
@author: Maciej Wasilak

Updated on 28-11-2020
@co-author: Johirul Islam
'''

import sys, time

from ipaddress import ip_address

from twisted.internet import reactor
from twisted.python import log

import txthings.coap as coap
import txthings.resource as resource

from config import CoAP_HOST, CoAP_PORT

from resources import DHTClient

def main():
    log.startLogging(sys.stdout)
    
    
    # Resource tree creation
    # coap://<host>:<port>
    '''root = resource.CoAPResource()'''
    
    # sensors root URL
    # coap://<host>:<port>/sensors
    '''sensors = resource.CoAPResource()
    root.putChild('sensors', sensors)'''
    
    # sensors dynamic URL
    # coap://<host>:<port>/sensors/dht
    '''dht = resource.CoAPResource()
    sensors.putChild('dht', dht)'''


    endpoint = resource.Endpoint(None)
    protocol = coap.Coap(endpoint)
    
    
    """
    # ---------------------------------------------------------------------- #        
    # read temperature 
    temperature = read(MODEL, PIN, 'temperature')
    temperature = round(temperature, 1)		
    print "temperature # ", temperature	
            
    # URI for "coap://<host>:<port>/sensors/dht/temperature"
    #uri      = (b'sensors/dht/temperature')
    uri      = (b'sensors', b'dht', b'temperature', )
    
    # Send request to "coap://<host>:<port>/sensors/dht/temperature"
    DHTClient(protocol, CoAP_HOST, CoAP_PORT, uri, str(temperature))
    
            
    # read humidity 
    humidity = read(MODEL, PIN, 'humidity')
    humidity = round(humidity, 1)	
    print "humidity    # ", humidity
            
    # URI for "coap://<host>:<port>/sensors/dht/temperature"
    uri      = (b'sensors', b'dht', b'humidity', )
    
    # Send request to "coap://<host>:<port>/sensors/dht/<temperature/humidity>"
    DHTClient(protocol, CoAP_HOST, CoAP_PORT, uri, str(humidity))
    # /--------------------------------------------------------------------- #
    """
    
    
    # above functionality made for temperature & humidity reading 
    # moved to resources module in DHTClient class
    DHTClient(protocol, CoAP_HOST, CoAP_PORT)
    
            
    reactor.listenUDP(61616, protocol)  # , interface="::")
    reactor.run()
    
        
if __name__ == '__main__':
    
    main()
    
