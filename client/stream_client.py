""" Toncu Vasile, 2017 April """

"""
Read and write raw jpg images from a multipart jpeg stream
In our case the server runs on rpi at http://<rpi-addr>:8080/?action=stream
"""

import requests
import sys
import time

ADDR = '192.168.100.17'

req = requests.get('http://'+ADDR+':8080/?action=stream', stream=True)
# req = requests.get('http://10.1.10.107:8080', stream=True)

def get_next_jpeg():
    # Find the len of the image
    chunks = req.raw.read(1024).split("\r\n\r\n", 1)
    for header in chunks[0].splitlines():
        if header.startswith("Content-Length:"):
            clen = header.split(": ", 1)[1]
            #print "Content len is %d" % int(clen)

    remaining = int(clen) - len(chunks[1])

    img = chunks[1] + req.raw.read(remaining)
    #print "Image is %d bytes long" % len(img)


    '''
    f = open('img-%s.jpg' % time.time(), 'wb')
    f.write(img)
    f.close()
    '''

    return img

url = "http://"+ ADDR +"8080/shot.jpg"

def get_next_shoot():
    r = requests.get(url)
    print len(r.content)
    return r.content



