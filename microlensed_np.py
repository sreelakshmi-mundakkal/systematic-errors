import lal
import lalsimulation as lalsim


from gwbench.wf_models import py_lgw

wf_symbs_string= 'f m1 m2 s1x s1y s1z s2x s2y s2z ml yl'

def hfpc (f, m1, m2, s1x, s1y, s1z, s2x, s2y, s2z, ml, yl)
    
    init_prms = dict(f_low=f[0], f_high= f[-1])
    lens_prms = dict(m_lens=ml, y_lens=yl)
    cbc_prms = dict(mass_1=m1, mass_2=m2, spin1x=s1x, spin1y=s1y, spin1z=s1z, spin2x=s2x, spin2y=s2y, spin2z=s2z)
    prms = {**lens_prms, **cbc_prms}
    res = lgw.lensed_pure_polarized_wf_gen(**prms)
    hplus = res['lensed_FD_WF_hp']
    hcross = res['lensed_FD_WF_hc']
    hp= hp[0:len(f)]
    hc= hc[0:len(f)]
    return hp, hc
