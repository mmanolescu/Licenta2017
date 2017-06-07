""" Toncu Vasile, 2017 April """

"""
Read and write raw jpg images from a multipart jpeg stream
In our case the server runs on rpi at http://<rpi-addr>:8080/?action=stream
"""

import requests
import sys
import time

req = requests.get('http://10.1.20.103:8080/?action=stream', stream=True)

def get_next_jpeg():
    # Find the len of the image
    chunks = req.raw.read(1024).split("\r\n\r\n", 1)
    for header in chunks[0].splitlines():
        if header.startswith("Content-Length:"):
            clen = header.split(": ", 1)[1]
            print "Content len is %d" % int(clen)

    remaining = int(clen) - len(chunks[1])

    img = chunks[1] + req.raw.read(remaining)
    print "Image is %d bytes long" % len(img)


    '''
    f = open('img-%s.jpg' % time.time(), 'wb')
    f.write(img)
    f.close()
    '''

    return img


