# Copyright Mark B. Skouson, 2020

import ffmpeg
import os
from guests.apps import create_standard_video, create_thumbnail, create_minivideo
from guests.apps import Configuration


# def test_passtest():
#     assert True

# def test_failtest():
#     assert False

def test_reshape_video():
    infile = '/opt/GuestBook/GuestBookServer/test/dontgit/testclip.mov'
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
    w = probe['streams'][0]['width']
    h = probe['streams'][0]['height']
    assert h==c.MINIHEIGHT
