# Copyright (C) 2020  Ssohrab Borhanian
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


"""This script calculates the lamdified derivatives of the waveform polarizations, antenna patterns, and detector responses.

The first lines of output are needed for the main benchmarking methods and should be copied to the main script.

"""

import os

from gwbench import antenna_pattern_np as ant_pat_np
from gwbench import detector_response_derivatives as drd
from gwbench import waveform as wfc

############################################################################
### User Choices
############################################################################

#-----choose waveform model - see below for available waveforms-----
# uncomment chosen waveform model from the list of currently available
if 1:
    wf_model_name = 'tf2'
    #wf_model_name = 'tf2_tidal'

    user_waveform = None

    #-----choose partial derivative variables for the chose waveform model-----
    if wf_model_name == 'tf2':
        wf_other_var_dic = None
        deriv_symbs_string = 'Mc eta chi1z chi2z DL tc phic iota ra dec psi'

    elif wf_model_name == 'tf2_tidal':
        wf_other_var_dic = None
        deriv_symbs_string = 'Mc eta chi1z chi2z DL tc phic iota lam_t ra dec psi'

else:
    wf_model_name    = 'tf2_user'
    wf_other_var_dic = None
    user_waveform   = {'np': '../gwbench/wf_models/tf2_np.py', 'sp':'../gwbench/wf_models/tf2_sp.py'}

#-----choose locations whose detector response derivatives should be calculated-----
# pass a list or None (if all locations, available in gwbench, are supposed to be used)
locs = ['H', 'L', 'V', 'K', 'I', 'ET1', 'ET2', 'ET3', 'C', 'N', 'S']

#-----choose whether antenna patterns and location phase factors should use frquency dependent gmst, thus incorporating the rotation of earth-----
# 1 for True, 0 for False - use 0 for speed or when comparability to code not incorporating the rotation of earth
use_rot = 1

#-----choose where to save the lambidified functions files-----
output_path = None

#-----user defined locations-----
user_locs = {'user-loc':{'longitude': 3.2, 'latitude': 0.4, 'arm_azimuth':0.3, 'which_arm':'y', 'shape':'L'}}

deriv_symbs_string = 'Mc eta DL'
locs = ['H', 'L', 'V', 'user-loc']

############################################################################
### Calculation of Lambdified Functions
############################################################################

#-----waveform settings based on choice-----
wf = wfc.Waveform(wf_model_name, wf_other_var_dic, user_waveform=user_waveform)

#-----antenna pattern symbols-----
ap_symbs_string = ant_pat_np.ap_symbs_string

#-----check partial derivatives based on choice-----
full_set = set( wf.wf_symbs_string.split(' ') + ap_symbs_string.split(' ') )
sub_set  = set( deriv_symbs_string.split(' ') )

if not sub_set <= full_set:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('!The choice of partial derivative variables is not a subset of the waveform and antenna pattern variables!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    quit()

#-----print settings as a check-----
print()
print('Copy the following 4 lines to your main benchmark script.')
print()
print('wf_model_name = \'{}\''.format(wf.wf_model_name))
print('wf_other_var_dic = {}'.format(wf.wf_other_var_dic))
print('deriv_symbs_string = \'{}\''.format(deriv_symbs_string))
print('use_rot = %i'%use_rot)
print()
print()

#-----create the lambidified detector reponses and derivatives-----
drd.generate_det_responses_derivs_sym(wf, deriv_symbs_string, locs=locs,
                                      use_rot=use_rot, user_locs=user_locs,
                                      user_lambdified_functions_path=output_path)
