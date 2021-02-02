# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2018, TU Wien
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Tests for transferring downloaded data to netcdf or grib files
'''

from ecmwf_models.erainterim.download import download_and_move

import os
import shutil
from datetime import datetime
from tempfile import TemporaryDirectory

def test_dry_download_nc_eraint():

    with TemporaryDirectory() as dl_path:

        dldir = os.path.join(dl_path, 'temp_downloaded')
        os.makedirs(dldir, exist_ok=True)

        thefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                  "ecmwf_models-test-data", "eraint", "download", "20000101_20000101.nc")
        shutil.copyfile(thefile, os.path.join(dl_path, 'temp_downloaded', '20000101_20000101.nc'))

        startdate = enddate = datetime(2000, 1, 1)

        download_and_move(dl_path, startdate, enddate, variables=['swvl1', 'swvl2', 'lsm'],
                          keep_original=False, h_steps=[0, 6, 12, 18],
                          grb=False, dry_run=True)

        assert(os.listdir(dl_path) == ['2000'])
        assert(os.listdir(os.path.join(dl_path, '2000')) == ['001'])

        should_dlfiles = ['ERAINT_AN_20000101_0000.nc',
                          'ERAINT_AN_20000101_0600.nc',
                          'ERAINT_AN_20000101_1200.nc',
                          'ERAINT_AN_20000101_1800.nc']

        assert(len(os.listdir(os.path.join(dl_path, '2000', '001'))) == len(should_dlfiles))

        assert(sorted(os.listdir(os.path.join(dl_path, '2000', '001'))) == sorted(should_dlfiles))



def test_dry_download_grb_eraint():

    with TemporaryDirectory() as dl_path:

        dldir = os.path.join(dl_path, 'temp_downloaded')
        os.makedirs(dldir, exist_ok=True)

        thefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                  "ecmwf_models-test-data", "eraint", "download", "20000101_20000101.grb")
        shutil.copyfile(thefile, os.path.join(dl_path, 'temp_downloaded', '20000101_20000101.grb'))

        startdate = enddate = datetime(2000, 1, 1)

        download_and_move(dl_path, startdate, enddate, variables=['swvl1', 'swvl2', 'lsm'],
                          keep_original=False, h_steps=[0, 6, 12, 18],
                          grb=True, dry_run=True)

        assert(os.listdir(dl_path) == ['2000'])
        assert(os.listdir(os.path.join(dl_path, '2000')) == ['001'])

        should_dlfiles = ['ERAINT_AN_20000101_0000.grb',
                          'ERAINT_AN_20000101_0600.grb',
                          'ERAINT_AN_20000101_1200.grb',
                          'ERAINT_AN_20000101_1800.grb']
        assert(len(os.listdir(os.path.join(dl_path, '2000', '001'))) == len(should_dlfiles))

        assert(sorted(os.listdir(os.path.join(dl_path, '2000', '001'))) == sorted(should_dlfiles))