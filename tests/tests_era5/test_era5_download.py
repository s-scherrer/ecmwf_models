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
from ecmwf_models.era5.download import download_and_move
import os
from tempfile import TemporaryDirectory
import shutil
from datetime import datetime

def test_dry_download_nc_era5():

    with TemporaryDirectory() as dl_path:
        thefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                "ecmwf_models-test-data", "era5", "download", "20100101_20100101.nc")
        dldir = os.path.join(dl_path, 'temp_downloaded')
        os.makedirs(dldir, exist_ok=True)
        shutil.copyfile(thefile, os.path.join(dldir, '20100101_20100101.nc'))

        startdate = enddate = datetime(2010,1,1)

        download_and_move(dl_path, startdate, enddate, variables=['swvl1', 'swvl2', 'lsm'],
                          keep_original=False, h_steps=[0, 6, 12, 18], grb=False, dry_run=True)

        assert(os.listdir(dl_path) == ['2010'])
        assert(os.listdir(os.path.join(dl_path, '2010')) == ['001'])

        should_dlfiles = ['ERA5_AN_20100101_0000.nc',
                          'ERA5_AN_20100101_0600.nc',
                          'ERA5_AN_20100101_1200.nc',
                          'ERA5_AN_20100101_1800.nc']

        assert(len(os.listdir(os.path.join(dl_path, '2010', '001'))) == len(should_dlfiles))


        assert(sorted(os.listdir(os.path.join(dl_path, '2010', '001'))) == sorted(should_dlfiles))


def test_dry_download_grb_era5():

    with TemporaryDirectory() as dl_path:

        dldir = os.path.join(dl_path, 'temp_downloaded')
        os.makedirs(dldir, exist_ok=True)

        thefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                  "ecmwf_models-test-data", "era5", "download", "20100101_20100101.grb")
        shutil.copyfile(thefile, os.path.join(dldir, '20100101_20100101.grb'))

        startdate = enddate = datetime(2010, 1, 1)

        download_and_move(dl_path, startdate, enddate, variables=['swvl1', 'swvl2', 'lsm'],
                          keep_original=False, h_steps=[0, 6, 12, 18],
                          grb=True, dry_run=True)

        assert(os.listdir(dl_path) == ['2010'])
        assert(os.listdir(os.path.join(dl_path, '2010')) == ['001'])

        should_dlfiles = ['ERA5_AN_20100101_0000.grb',
                          'ERA5_AN_20100101_0600.grb',
                          'ERA5_AN_20100101_1200.grb',
                          'ERA5_AN_20100101_1800.grb']

        assert(len(os.listdir(os.path.join(dl_path, '2010', '001'))) == len(should_dlfiles))
        assert(sorted(os.listdir(os.path.join(dl_path, '2010', '001'))) == sorted(should_dlfiles))

if __name__ == '__main__':
    test_dry_download_grb_era5()