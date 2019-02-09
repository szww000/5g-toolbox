#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Numerology.py
@Time    :   2019/02/09 22:58:59
@Author  :   finito 
@Version :   v0.0
@Contact :   szww000@126.com
@License :   (C)Copyright 2018-2019
@Desc    :   None
'''

import numpy as np


class Numerology(object):

    def __init__(self, **kwargs):
        self.fft_size = kwargs.get('fft_size', 2048)
        self.mu = kwargs.get('mu', 0)
        self.cyclic_prefix = kwargs.get('cyclic_prefix', 0)
        self.k = self.fft_size * (1 << self.mu) // 2048

    def cal_cp_len(self):
        if 0 == self.cyclic_prefix:
            cp_len = np.array([144 * (2 ** -self.mu) + 16, 144 * (2 ** -self.mu)])
        else:
            cp_len = np.array([512 * (2 ** -self.mu), 512 * (2 ** -self.mu)])
        return cp_len * self.k
    
    def add_cp(self, d_in):
        cp_len = self.cal_cp_len()
        td_shape = d_in.shape
        if 0 == self.mu:
            sym_other = np.setdiff1d(range(14), [0, 7])
            ant_data_sym0_7 = \
                np.concatenate((d_in[:, (td_shape[1] - cp_len[0]):, [0, 7]],
                                d_in[:, :, [0, 7]]), axis=1)
            ant_data_sym_other = \
                np.concatenate(
                    (d_in[:, (td_shape[1] - cp_len[1]):, sym_other],
                    d_in[:, :, sym_other]), axis=1)
            ant_data_sym_other = np.transpose(
                ant_data_sym_other, (0, 2, 1)).reshape(td_shape[0], 2, -1)
            ant_data_sym_other = np.transpose(ant_data_sym_other, (0, 2, 1))
            ant_data_sym = np.concatenate((ant_data_sym0_7, ant_data_sym_other), axis=1)
            td_add_cp = np.transpose(ant_data_sym, (0, 2, 1)).reshape((td_shape[0], -1))
        else:
            ant_data_sym0 = \
                np.concatenate((d_in[:, (td_shape[1] - cp_len[0]):, 0],
                                d_in[:, :, 0]), axis=1)
            ant_data_sym_other = \
                np.concatenate(
                    (d_in[:, (td_shape[1] - cp_len[1]):, 1:], d_in[:, :, 1:]), axis=1)
            ant_data_sym_other = np.transpose(
                ant_data_sym_other, (0, 2, 1)).reshape(td_shape[0], -1)
            td_add_cp = np.concatenate((ant_data_sym0, ant_data_sym_other), axis=1)
        return td_add_cp

        
    