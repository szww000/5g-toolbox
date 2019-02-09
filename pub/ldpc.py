#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ldpc.py
@Time    :   2019/02/09 22:09:38
@Author  :   10110574 
@Version :   v0.0
@Contact :   meng.bo1@zte.com.cn
@License :   (C)Copyright 2018-2019
@Desc    :   None
'''

import numpy as np


class Ldpc(object):
    
    def __init__(**kwargs):
        pass

    def code_block_segment(self, b, bg_ind):
        kcb = np.array([8448,3840])
        kcb = kcb[bg_ind-1]
        if b <= kcb:
            cb_crc_len = 0
            cb_num = 1
            b1 = b
        else:
            cb_crc_len = 24
            cb_num = np.ceil(b/(kcb-cb_crc_len))
            b1 = b + cb_num * cb_crc_len
        k1 = np.int32(b1/cb_num)
        return cb_crc_len, cb_num, k1
