# Copyright Mark B. Skouson, 2020

import os
import json
import requests

def test_guest_post_vid_uid():
    """
    The full video receiving and processing process is outlined in 
    serverapp.guests.views.post_vid_uid
    
    Test the server to make sure it can handle guest tries to submit videos
    and process them.  

    If the environment variable CLOUD_TASKS is set to True (actually not False)
    this test will exercise the capability using cloud tasks.
    Otherwise it will process the video on Server and and wait until the 
    processing is done to return a response.
    """
    ###################
    # Check for a wrong url
    HOSTNAME = 'localhost'
    # TODO be able to dynamically determine HOSTNAME depending on where running the test
    HOSTNAME = 'host.docker.internal'  # must use this if trying to go to localhost from a docker on mac
    HOSTPORT = str(8000)
    sendurl = 'http://' + HOSTNAME + ':' + HOSTPORT + '/guests/4/3/qlHxCHcgJ/post_vid/'
    with requests.Session() as s:
        with open('/opt/GuestBook/GuestbookServer/test/dontgit/testclip.mov', 'rb') as img:
            r = s.post(sendurl, data='guest1'.encode('utf-8'), verify=False)
    assert b'Bad event url' in r._content
    ################
    # Test a get request 
    #   Simulate Guest initial 
    # Set up the url that would come from the qr code
    # This is for the test case set up through factoryrdlab@gmail.com
    # http://localhost:8000/guests/4/3/qlHxCHcgJo/post_vid/
    sendurl = 'http://' + HOSTNAME + ':' + HOSTPORT + '/guests/4/3/qlHxCHcgJo/post_vid/'
    with requests.Session() as s:
        r = s.get(sendurl)
    assert b'Factory Research and Development' in r._content

    ################
    # Test test 
    # Set up the url that would come from the qr code
    # This is for the test case set up through event host=factoryrdlab@gmail.com
    # http://localhost:8000/guests/4/3/qlHxCHcgJo/post_vid/
    sendurl = 'http://' + HOSTNAME + ':' + HOSTPORT + '/guests/4/3/qlHxCHcgJo/post_vid/'
    with requests.Session() as s:
        with open('/opt/GuestBook/GuestbookServer/test/dontgit/testclip.mov', 'rb') as img:
            r = s.post(sendurl, data='guest1'.encode('utf-8'), verify=False)
            content = json.loads(r.content)

            secureurl = content['url']
            assert 'https://storage.googleapis.com/gb-a/4/3/orig' in secureurl

            successurl = 'http://' + HOSTNAME + ':' + HOSTPORT + '/guests/4/3/qlHxCHcgJo/'+str(content['vid'])+'/'
            # print(successurl)
            with open('/opt/GuestBook/GuestbookServer/test/dontgit/testclip.mov', 'rb') as img:
                payload = {
                    'success_action_redirect':
                        ('success_action_redirect',
                         successurl,
                         'text/plain'),
                    'file':
                        ('in2a.mov',
                            img,
                            'multipart/form-data',
                            {'Expires': '0'}
                        )
                }
                r = s.post(secureurl, files=payload)#, verify=False)
                print(r.status_code)
                print(r.__dict__)

            assert r.status_code == 200
