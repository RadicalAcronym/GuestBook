# Copyright Mark B. Skouson, 2020

import ffmpeg
import os
from singlevideo.apps import create_standard_video, create_thumbnail, create_minivideo
from singlevideo.apps import Configuration


videolist = [
    'frommarksphone.mp4',
    'portrait1.mp4',
    '029c8d1f-dc17-4d77-823a-373a2881dd37.mp4',
    '4_3_processed_151-vFkq-guest1.mp4',
    '4_3_processed_291-Dxgd-unity_post.mp4',
    '4_3_processed_295-gVso-guest1.mp4',
    'WIN_20210320_19_17_00_Pro.mp4',
    'output.mp4',
]
answerdict = {
    '029c8d1f-dc17-4d77-823a-373a2881dd37.mp4' : {},
    'portrait1.mp4' : {},
    '4_3_processed_151-vFkq-guest1.mp4' : {},
    '4_3_processed_291-Dxgd-unity_post.mp4' : {},
    '4_3_processed_295-gVso-guest1.mp4' : {},
    'WIN_20210320_19_17_00_Pro.mp4' : {},
    'frommarksphone.mp4' : {},
    'output.mp4' : {},

}
def test_reshape_video():
    for v in videolist:
        infile = f'/opt/GuestBook/GuestBookServer/test/dontgit/{v}'
        outfile = '/opt/GuestBook/GuestBookServer/test/dontgit/reshaped_test.mp4'
        c = Configuration()
        create_standard_video(infile,outfile,c)
        probe = ffmpeg.probe(outfile)
        w = probe['streams'][0]['width']
        h = probe['streams'][0]['height']
        assert h==c.HEIGHT and w==c.WIDTH

def test_create_thumbnail():
    infile = '/opt/GuestBook/GuestBookServer/test/dontgit/reshaped_test.mp4'
    outfile = '/opt/GuestBook/GuestBookServer/test/dontgit/thumbnail_test.jpg'
    c = Configuration()
    create_thumbnail(infile,outfile,c)
    probe = ffmpeg.probe(outfile)
    w = probe['streams'][0]['width']
    h = probe['streams'][0]['height']
    assert h==c.THUMBSIZE and w==c.THUMBSIZE

def test_create_minivideo():
    infile = '/opt/GuestBook/GuestBookServer/test/dontgit/reshaped_test.mp4'
    outfile = '/opt/GuestBook/GuestBookServer/test/dontgit/minivideo_test.mp4'
    c = Configuration()
    create_minivideo(infile,outfile,c)
    probe = ffmpeg.probe(outfile)
    # w = probe['streams'][0]['width']
    h = probe['streams'][0]['height']
    assert h==c.MINIHEIGHT
