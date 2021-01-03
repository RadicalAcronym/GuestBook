# Copyright Mark B. Skouson, 2019
from unittest import TestCase
import requests
import os
import json


class TestReceiveVideoDirect(TestCase):
    def test_receiv_video_direct(self):
        HOSTNAME = 'localhost'
        HOSTPORT = str(8000)
        sendurl = 'http://' + HOSTNAME + ':' + HOSTPORT + '/guests/4/3/qlHxCHcgJo/post_vid/'
        with requests.Session() as s:
            r = s.post(sendurl, data='guest1'.encode('utf-8'), verify=False)
            content = json.loads(r.content)
            secureurl = content['url']
            print(secureurl)
            successurl = 'http://' + HOSTNAME + ':' + HOSTPORT + '/guests/4/3/qlHxCHcgJo/'+str(content['vid'])+'/'
            # print(successurl)
            with open('testclip.mov', 'rb') as img:
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

            self.assertTrue('200', r.status_code)


    # def test_imageclassification(self):
    #     HOSTNAME = 'localhost'
    #     HOSTPORT = str(8000)
    #     sendurl = 'http://' + HOSTNAME + ':' + HOSTPORT + '/robots/catch_classify/'
    #
    #     with requests.Session() as s:
    #         with open('sample.jpg', 'rb') as img:
    #             payload = {'image':
    #                        ('sample.jpg',
    #                         img,
    #                         'multipart/form-data',
    #                         {'Expires': '0'}
    #                         )
    #                        }
    #             r = s.post(sendurl, files=payload, verify=False)
    #         if r.status_code == 200:
    #             resp = json.loads(r.content)
    #         print('HEADERS:\n', r.headers)
    #         print('r.content', resp)
    #     expected_response = [['n04584207', 'wig', 0.11642187833786011],
    #                          ['n04254680', 'soccer_ball', 0.04691394418478012],
    #                          ['n03877472', 'pajama', 0.032831691205501556],
    #                          ['n04532106', 'vestment', 0.022965330630540848],
    #                          ['n03141823', 'crutch', 0.02023189887404442],
    #                          ['n04442312', 'toaster', 0.019975844770669937],
    #                          ['n03018349', 'china_cabinet', 0.019496949389576912],
    #                          ['n03720891', 'maraca', 0.017556708306074142],
    #                          ['n03476991', 'hair_spray', 0.017064088955521584],
    #                          ['n03443371', 'goblet', 0.016647690907120705]]
    #     self.assertEqual(expected_response, resp)
