# Copyright Mark B. Skouson, 2020

import ffmpeg
import os
os.sys.path.append('/opt')
from project.guests.apps import reshape_video, create_thumbnail, create_minivideo
from project.guests.apps import Configuration


# def test_passtest():
#     assert True

# def test_failtest():
#     assert False

def test_reshape_video():
    infile = '/opt/test/dontgit/frommarksphone.mp4'
    outfile = '/opt/test/dontgit/reshaped_test.mp4'
    c = Configuration()
    reshape_video(infile,outfile,c)
    probe = ffmpeg.probe(outfile)
    w = probe['streams'][0]['width']
    h = probe['streams'][0]['height']
    assert h==c.HEIGHT and w==c.WIDTH

def test_create_thumbnail():
    infile = '/opt/test/dontgit/reshaped_test.mp4'
    # infile = '/opt/test/dontgit/4_3_processed_291-Dxgd-unity_post.mp4'
    outfile = '/opt/test/dontgit/thumbnail_test.jpg'
    c = Configuration()
    create_thumbnail(infile,outfile,c)
    probe = ffmpeg.probe(outfile)
    w = probe['streams'][0]['width']
    h = probe['streams'][0]['height']
    assert h==c.THUMBSIZE and w==c.THUMBSIZE

def test_create_minivideo():
    infile = '/opt/test/dontgit/reshaped_test.mp4'
    # infile = '/opt/test/dontgit/4_3_processed_291-Dxgd-unity_post.mp4'
    outfile = '/opt/test/dontgit/minivideo_test.mp4'
    c = Configuration()
    create_minivideo(infile,outfile,c)
    probe = ffmpeg.probe(outfile)
    w = probe['streams'][0]['width']
    h = probe['streams'][0]['height']
    assert h==c.MINIHEIGHT
