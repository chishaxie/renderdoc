#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

import gen_render_mask


def main():
    img_prefix = '20180123_'

    rdc_dir = 'Z:\\RenderMask\\save'
    debug_cmd = 'Z:\\RenderMask\\Debug\\renderdoccmd.exe'
    release_cmd = 'Z:\\RenderMask\\Release\\renderdoccmd.exe'
    ini_file_path = 'Z:\\RenderMask\\test.ini'
    train_data_dir = 'Z:\\RenderMask\\train_data'

    # origin_img_dir = os.path.join(train_data_dir, 'img')
    # mask_dir = os.path.join(train_data_dir, 'mask')
    # if not os.path.exists(origin_img_dir):
    #     os.makedirs(origin_img_dir)
    # if not os.path.exists(mask_dir):
    #     os.makedirs(mask_dir)
    img_index = 0
    for rdc_file_name in os.listdir(rdc_dir):
        if not rdc_file_name.endswith('rdc'):
            continue
        if not rdc_file_name.startswith('GTA'):
            continue

        rdc_file_path = os.path.join(rdc_dir, rdc_file_name)
        tmp_af_out_dir = os.path.join(rdc_dir, 'tmp_'+rdc_file_name)
        try:
            if not os.path.exists(tmp_af_out_dir):
                os.makedirs(tmp_af_out_dir)
            # origin_img_out_dir = os.path.join(origin_img_dir, str(img_index))
            # if not os.path.exists(origin_img_out_dir):
            #     os.makedirs(origin_img_out_dir)
            origin_img_file_path = os.path.join(train_data_dir, 'out.png')

            os.system('start /wait %s replay '
                      '%s --af-out %s' % (debug_cmd, rdc_file_path, train_data_dir))
            
            os.system('start /wait %s replay '
                      '%s --af-out %s --ini %s' % (release_cmd, rdc_file_path, tmp_af_out_dir, ini_file_path))

            print '************************************************************************\n' * 8
            print 'rdc file:', rdc_file_path

            if os.path.exists(origin_img_file_path):
                new_img_file_path = os.path.join(train_data_dir, '%s%s.png' % (img_prefix, img_index))
                print 'move file from %s to %s ......' % (origin_img_file_path, new_img_file_path)
                os.rename(origin_img_file_path, new_img_file_path)
            else:
                print 'move failed'
                break

            print 'gen mask'
            mask = gen_render_mask.gen(tmp_af_out_dir)
            mask_file_path = os.path.join(train_data_dir, '%s%s_mask.png' % (img_prefix, img_index))
            print mask_file_path
            mask.save(mask_file_path)
            if not os.path.exists(mask_file_path):
                print 'mask save failed'
                break
        except Exception as e:
            raise
            print '---------gggggggggg-------------'
            print e.message
            print '================================'
            continue
        finally:
            img_index += 1
            print 'finish'
            print '*********************************************************\n' * 4


if __name__ == '__main__':
    main()
