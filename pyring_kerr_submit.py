#code for job submission automation:
#!/usr/bin/env python

from glob import glob
from subprocess import call
import os
import pickle

import sys
sys.path.append('/home/anuj.mishra/git_repos/GWMAT/src/')
# sys.path.append('/mnt/home/student/canujm/my_packages/')
import py_lgw
lgw = py_lgw.lensed_wf_gen()

# sys.dont_write_bytecode = True #to avoide creating .pyc cache files
# import pnt_mlwf_gen as wf_gen

# proc_ID = int(sys.argv[1])

rd_model="Kerr"
kerr_run_tags=["2220", "2221", "domega", "dtau", "domega_dtau"]
pe_model="ul"
set_label="0"
events=["gw150914", "gw190521A"]

data_dir = "/home/sreelakshmi.m/prod_runs/pyring/pyring_runs/s1_ul_vs_ml/data/set_" + set_label + "/"
cwd = os.getcwd()


for event in events:
    injection_info_file = glob(data_dir + event + "/*.pkl")[0]
    with open(injection_info_file, "rb") as f:
        injection_info = pickle.load( f )

    pe_outdir_lev1 = cwd + '/outdirs_'+ event + '_' + pe_model+'_pe_' + rd_model
    try:
        os.mkdir(pe_outdir_lev1)
    except OSError as e:
        print(e)

    for i in range( len( injection_info.keys() ) ):
        for kerr_run_tag in kerr_run_tags:
            os.chdir(cwd)

            label = str(i) + '_' + event + '_' + pe_model + 'pe_' + rd_model + '_' + kerr_run_tag \
                    + '_Mlz' + lgw.str_m(injection_info[str(i)]['m_lens']) + '_y' + lgw.str_y(injection_info[str(i)]['y_lens'])

            pe_outdir_lev2 = pe_outdir_lev1 + '/' + label
            pe_outdir_lev3 = pe_outdir_lev2 + '/outdir'

            try:
                os.mkdir(pe_outdir_lev2)
            except OSError as e:
                print(e)
            try:
                os.mkdir(pe_outdir_lev3)
            except OSError as e:
                print(e)

            data_H1 = glob(data_dir + event + '/' + str(i) + '_H-*.txt')[0]
            data_L1 = glob(data_dir + event + '/' + str(i) + '_L-*.txt')[0]
            data_V1 = glob(data_dir + event + '/' + str(i) + '_V-*.txt')[0]

            config_file = "config_" + rd_model + ".ini"
            call("cp %s %s"%(config_file, pe_outdir_lev2), shell=1)
            call("cp %s %s"%("condor.sub", pe_outdir_lev2), shell=1)
            call("cp %s %s"%("run.sh", pe_outdir_lev2), shell=1)
            os.chdir(pe_outdir_lev2)
            # config_mod_cmd = "sed -i 's/"
            # config_mod_cmd += mod_inj_prms + "/g' %s"%(config_file)
            # call(config_mod_cmd, shell=True)
            ## Modify the config file as per the injection
            call("sed -i 's+output=+output=%s+g' %s"%(pe_outdir_lev3, config_file), shell=1)
            call("sed -i 's+data-H1=+data-H1=%s+g' %s"%(data_H1, config_file), shell=1)
            call("sed -i 's+data-L1=+data-L1=%s+g' %s"%(data_L1, config_file), shell=1)
            call("sed -i 's+data-V1=+data-V1=%s+g' %s"%(data_V1, config_file), shell=1)
            call("sed -i 's+trigtime=+trigtime=%s+g' %s"%(injection_info[str(i)]['trigger_time_at_H1'], config_file), shell=1)
            call("sed -i 's+run-tag=+run-tag=%s+g' %s"%(label, config_file), shell=1)

            mf_estimate = lgw.remnant_prms_estimate(m1=injection_info[str(i)]['mass_1'], m2=injection_info[str(i)]['mass_2'],
                                                    a1=injection_info[str(i)]['a_1'], a2=injection_info[str(i)]['a_2'],
                                                    tilt1=injection_info[str(i)]['tilt_1'], tilt2=injection_info[str(i)]['tilt_2'], phi12=injection_info[str(i)]['phi_12'])['m_f']
            call("sed -i 's+mf-time-prior=+mf-time-prior=%s+g' %s"%(mf_estimate, config_file), shell=1)
            call("sed -i 's+fix-ra=+fix-ra=%s+g' %s"%(injection_info[str(i)]['ra'], config_file), shell=1)
            call("sed -i 's+fix-dec=+fix-dec=%s+g' %s"%(injection_info[str(i)]['dec'], config_file), shell=1)

            if mf_estimate < 100:
                mf_max = 200
            elif 100 <= mf_estimate < 200:
                mf_max = 300
            elif 200 <= mf_estimate < 300:
                mf_max = 400
            else:
                mf_max = 500
            mf_min = 20
            call("sed -i 's+Mf-min=+Mf-min=%s+g' %s"%(mf_min, config_file), shell=1)
            call("sed -i 's+Mf-max=+Mf-max=%s+g' %s"%(mf_max, config_file), shell=1)
             if kerr_run_tag == "2220":
                kerr_mode_array = "[(2,2,2,0)]"
            else:
                kerr_mode_array = "[(2,2,2,0), (2,2,2,1)]"

            if kerr_run_tag == "domega" or kerr_run_tag == "domega_dtau":
                domega_mode_array = "[(2,2,1)]"
            else:
                domega_mode_array = "None"

            if kerr_run_tag == "dtau" or kerr_run_tag == "domega_dtau":
                dtau_mode_array = "[(2,2,1)]"
            else:
                dtau_mode_array = "None"

            call("sed -i 's+kerr-modes=+kerr-modes=%s+g' %s"%(kerr_mode_array, config_file), shell=1)
            call("sed -i 's+domega-tgr-modes=+domega-tgr-modes=%s+g' %s"%(domega_mode_array, config_file), shell=1)
            call("sed -i 's+dtau-tgr-modes=+dtau-tgr-modes=%s+g' %s"%(dtau_mode_array, config_file), shell=1)


            # submittin the runs
            call("sed -i 's+config-file+config-file %s+g' %s"%(config_file, "run.sh"), shell=1)
            call("sed -i 's+batch_name=+batch_name=%s+g' %s"%(label, "condor.sub"), shell=1)
            call("condor_submit condor.sub", shell=1)

                                                                                                                                                                                         44,1          62


