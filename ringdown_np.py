### addition in gwbench for ringdown-only analysis
import pyRing
import numpy as np
import pycbc
import scipy
from scipy.interpolate import interp1d
from pycbc.types import TimeSeries
from pyRing import waveform as wf
import sys
sys.path.append('/home/sreelakshmi.m/gwmat/src')
import py_lgw
lgw = py_lgw.lensed_wf_gen()

wf_symbs_string = 'f t0 Mf af A_lmn D_L iota phi tc phic'


def hfpc(f,t0, Mf, af, A_lmn, D_L, iota, phi, tc, phic):
    #f_min   = f[0]
    #delta_f = f[1] - f[0]
    #f_max   = f[-1] + delta_f

    t0 = t0 
    Mf = Mf
    af = af   
    amps = A_lmn
    r = D_L
    iota = iota
    phi  = phi
    
    Kerr = wf.KerrBH(t0,Mf,af,amps,r,iota,phi)
    t= np.arange(0.0033, 0.05, 2e-4)
    waveform = Kerr.waveform(t)
    hp = waveform[3]
    hc = waveform[4]
    hp = TimeSeries(hp, delta_t=t[1]-t[0])
    hc = TimeSeries(hc, delta_t=t[1]-t[0])
    hp_ = lgw.wf_len_mod_start(hp, extra=0.2, **{'sample_rate':hp.sample_rate})
    hc_ = lgw.wf_len_mod_start(hc, extra=0.2, **{'sample_rate':hp.sample_rate})
    f_hp = hp_.to_frequencyseries(delta_f=hp_.delta_f)
    f_hc = hp_.to_frequencyseries(delta_f=hc_.delta_f)
    
    wfs_res = {'hp':f_hp, 'hc':f_hc}
    res = dict()

    frequency_vector = f #Desired frequency vector

    for key in wfs_res.keys():

        temp_fd = wfs_res[key]
        log_strain_array = np.log10(np.array(temp_fd, dtype=np.complex128))
        log_abs = np.real(log_strain_array)
        phase = np.array(pycbc.waveform.utils.phase_from_frequencyseries(temp_fd))
        if_log_abs = interp1d(temp_fd.sample_frequencies[:], log_abs[:], kind='linear')
        if_phase = interp1d(temp_fd.sample_frequencies[:], phase[:], kind='linear')
        interpolated_abs = np.concatenate(([0], 10**(if_log_abs(frequency_vector[1:]))))
        interpolated_phase = np.concatenate(([0], if_phase(frequency_vector[1:])))
        interpolated_strain = interpolated_abs * np.exp(1j * interpolated_phase)
        frequency_bounds = (frequency_vector >= frequency_vector[0]) * (frequency_vector<= frequency_vector[-1])
        interpolated_strain *= frequency_bounds
        assert len(interpolated_strain) == len(f)
        res[key] = interpolated_strain
        hfp = res['hp']
        hfc = res['hc']

    return res['hp'], res['hc']
