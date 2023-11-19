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

import numpy as np
from pycbc.waveform import ringdown

wf_symbs_string = 'f f_lmn tau amp phi_lmn t_0 l m n inclination azimuthal harmonics final_spin tc phic'

def hfpc(f, f_lmn, tau, amp, phi_lmn, t_0, l, m, n, inclination , azimuthal, harmonics, final_spin, tc, phic):
    f_min   = f[0]
    delta_f = f[1] - f[0]
    f_max   = f[-1] + delta_f

   
    
    hfp, hfc = ringdown.fd_damped_sinusoid(f_0 = f_lmn, tau= tau, amp=amp, phi= phi_lmn, freqs= f, t_0= t_0, l=l, m=m, n=n, inclination=inclination, azimuthal=azimuthal, harmonics=harmonics, 
                    final_spin = final_spin)
   

    
    return hfp, hfc
