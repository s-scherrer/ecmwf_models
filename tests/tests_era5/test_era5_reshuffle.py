# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2016, TU Wien
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
Test module for image to time series conversion.
'''

import os
import glob
from tempfile import TemporaryDirectory
import numpy as np
import numpy.testing as nptest

from ecmwf_models.era5.reshuffle import main
from ecmwf_models import ERATs

def test_ERA5_reshuffle_nc():
    # test reshuffling era5 netcdf images to time series

    inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                          "ecmwf_models-test-data", "era5", "nc")

    startdate = '2010-01-01'
    enddate = '2010-01-01'
    parameters = ["swvl1", "swvl2"]
    h_steps = ['--h_steps', '0', '12']
    landpoints = ['--land_points', 'True']

    with TemporaryDirectory() as ts_path:
        args = [inpath, ts_path, startdate, enddate] + parameters + h_steps + landpoints
        main(args)
        assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == 948 # less files because only land points
        ds = ERATs(ts_path, ioclass_kws={'read_bulk':True})
        ts = ds.read(15, 48)
        swvl1_values_should = np.array([0.402825,  0.390983], dtype=np.float32)
        nptest.assert_array_almost_equal(ts['swvl1'].values, swvl1_values_should, decimal=5)
        swvl2_values_should = np.array([0.390512,  0.390981], dtype=np.float32)
        nptest.assert_array_almost_equal(ts['swvl2'].values, swvl2_values_should, decimal=5)
        ds.close()

def test_ERA5_reshuffle_grb():
    # test reshuffling era5 netcdf images to time series

    inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                          "ecmwf_models-test-data", "era5", "nc")

    startdate = '2010-01-01'
    enddate = '2010-01-01'
    parameters = ["swvl1", "swvl2"]
    h_steps = ['--h_steps', '0', '12']
    landpoints = ['--land_points', 'False']

    with TemporaryDirectory() as ts_path:
        args = [inpath, ts_path, startdate, enddate] + parameters + h_steps + landpoints
        main(args)
        assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == 2593 # more files because all points
        ds = ERATs(ts_path, ioclass_kws={'read_bulk':True})
        ts = ds.read(15, 48)
        swvl1_values_should = np.array([0.402824,  0.390979], dtype=np.float32)
        nptest.assert_almost_equal(ts['swvl1'].values, swvl1_values_should, decimal=5)
        swvl2_values_should = np.array([0.390514,  0.390980], dtype=np.float32)
        nptest.assert_almost_equal(ts['swvl2'].values, swvl2_values_should, decimal=5)
        ds.close()


if __name__ == '__main__':
    test_ERA5_reshuffle_nc()