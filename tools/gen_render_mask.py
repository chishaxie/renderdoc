#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from PIL import Image
from PIL import ImageChops

scan_dir = 'G:\\renderdoc_gta'

regex_p = re.compile(r'^p_([0-9]+)\.png$')

point_table = ([0] + ([255] * 255))

def gen(scan_dir):
    imgs = []
    for fn in os.listdir(scan_dir):
        m = regex_p.search(fn)
        if m:
            index = int(m.group(1))
            imgs.append((fn, index))
    imgs.sort(key=lambda x: x[1])
    # print imgs
    
    assert len(imgs) % 2 == 1

    im_mask = None

    im_white = None
    im_black = None

    im_last = None
    for i, img in enumerate(imgs):
        im = Image.open(os.path.join(scan_dir, img[0]))
        if im_last is None:
            im_last = im
            im_mask = Image.new('1', im.size)
            im_white = Image.new('1', im.size, color=255)
            im_black = Image.new('1', im.size, color=0)
            continue
        diff = ImageChops.difference(im, im_last)
        diff = diff.convert('L')
        diff = diff.point(point_table)
        # diff.show()
        if i % 2 == 1:
            # print img[0], 'w'
            im_mask.paste(im_white, mask=diff)
        else:
            # print img[0], 'b'
            im_mask.paste(im_black, mask=diff)
        im_last = im
    im_mask.show()

gen(scan_dir)
