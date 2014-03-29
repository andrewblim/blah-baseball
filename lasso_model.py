from projections import *
from sklearn.linear_model import LassoLarsCV, LassoCV, LassoLarsIC
import itertools
import numpy
import numpy.ma
import random
import csv
from baseballprojections.aux_vars import *

# There are some warnings from scikit-learn
# This causes them to be ignored
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

base_dir = "C:\\Users\\Benjamin\\Dropbox\\Baseball\\CSVs for DB"
#base_dir = "/Users/andrew_lim/Dropbox/Baseball/CSVs for DB"

#base_dir = "/Users/bhebert/Dropbox/Baseball/CSVs for DB"



pm = MyProjectionManager('sqlite:///projections.db')
#pm = MyProjectionManager()

#pm.read_everything_csv(base_dir = base_dir,read_register=True, verbose=False)

# what coefs get printed to stdout during the run
print_nonzero_coefs_only = True

#player_types = ['batter','pitcher']
#player_types = ['pitcher']
player_types = ['batter']
playing_times = {'batter':'pa', 'pitcher':'ip'}
stats = {'batter':['pa', 'ab', 'obp', 'slg', 'sbrate', 'csrate', 'runrate', 'rbirate'],
         'pitcher':['g','gs','ip','era','whip','saverate','winrate','krate']}
#stats = {'batter':['pa','obp'],'pitcher':['g','ip','winrate']}
        # 'pitcher':['g','era','krate']}
proj_systems = ['pecota', 'zips', 'steamer']
proj_systems_sv = ['pecota','steamer']
all_systems = ['actual','pecota','zips','steamer']

# For each stat, what is the corresponding playing time stat?
ptstats = {'pa': None, 'ab': None, 'obp': 'pa', 'slg': 'ab', 'sbrate': 'tob', 'csrate': 'tob',
           'runrate': 'tob', 'rbirate': 'pa', 'g': None, 'gs': None, 'ip': None, 'krate':'ip',
           'era': 'ip', 'whip': 'ip', 'saverate': 'gr', 'winrate': 'g'}

# model settings
cv_num = 60
num_iter = 2000
min_pts ={'batter':100, 'pitcher':20}
use_lars = True
use_aic = False
norm = True
x2vars = False
use_gls = True

# I think this code is broken. The min sample sized
# needs to be changed to reflect the different pt stats.
filter_rates = False
min_sample_pts = {'batter':300,'pitcher':40}

use_ages = True
use_teams = True


lag_years = 2
first_year = 2004

model_years = [2011]

def stat_ops(p):
    if p.obp is not None and p.slg is not None:
        return p.obp + p.slg
    else:
        return None
def stat_runrate(p):
    if p.pa is not None and p.r is not None and p.pa > 0 and p.obp is not None and p.obp > 0:
        return p.r / (p.pa*p.obp)
    elif p.pa is not None and p.r is not None and p.pa > 0 and p.obp is not None and p.obp == 0:
        return 0
    else:
        return None
def stat_rbirate(p):
    if p.pa is not None and p.rbi is not None and p.pa > 0:
        return p.rbi / p.pa
    else:
        return None
def stat_sbrate(p):
    if p.pa is not None and p.sb is not None and p.pa > 0 and p.obp is not None and p.obp > 0:
        return p.sb / (p.pa*p.obp)
    elif p.pa is not None and p.sb is not None and p.pa > 0 and p.obp is not None and p.obp == 0:
        return 0
    else:
        return None
def stat_csrate(p):
    if p.pa is not None and p.cs is not None and p.pa > 0 and p.obp is not None and p.obp > 0:
        return p.cs / (p.pa*p.obp)
    elif p.pa is not None and p.cs is not None and p.pa > 0 and p.obp is not None and p.obp == 0:
        return 0
    else:
        return None
def stat_saverate(p):
    if p.g is not None and p.gs is not None and (p.g-p.gs) > 0 and p.sv is not None:
        return p.sv / (p.g-p.gs)
    elif p.g is not None and p.gs is not None and p.sv is not None:
        return 0
    else:
        return None
def stat_winrate(p):
    if p.g is not None and p.w is not None and p.g > 0:
        return p.w / p.g
    elif p.g is not None and p.w is not None and p.g ==0 and p.w == 0:
        return 0
    else:
        return None
def stat_krate(p):
    if p.k is not None and p.ip is not None and p.ip > 0:
         return p.k / p.ip
    else:
         return None
def stat_tob(p):
    if p.pa is not None and p.obp is not None:
        return p.pa * p.obp
    else:
        return None
def stat_gr(p):
    if p.g is not None and p.gs is not None:
        return p.g - p.gs
    else:
        return None
def stat_gfrac(p):
    if p.g is not None and p.gs is not None and p.g > 0:
        return (p.gs*2 > p.g)
    elif p.g is not None and p.gs is not None and p.g ==0 and p.gs == 0:
        return 0
    else:
        return None
def stat_winrate_gf(p):
    if p.g is not None and p.gs is not None and p.g > 0 and p.w is not None: 
        return p.w / p.g * (p.gs*2 > p.g)
    elif p.g is not None and p.w is not None and p.gs is not None and p.g ==0 and (p.w == 0 or p.gs == 0):
        return 0
    else:
        return None
    
def stat_winrate_ngf(p):
    if p.g is not None and p.gs is not None and p.g > 0 and p.w is not None: 
        return p.w / p.g * (p.gs*2 <= p.g)
    elif p.g is not None and p.w is not None and p.gs is not None and p.g ==0 and (p.w == 0 or p.gs == 0):
        return 0
    else:
        return None



        



all_stats = {'batter':['g',
            'ab',
            'pa',
            'h',
            'h1b',
            'h2b',
            'h3b',
            'hr',
            'r',
            'rbi',
            'bb',
            'ibb',
            'k',
            'hbp',
            'sf',
            'sh',
            'gdp',
            'sb',
            'cs',
            'avg',
            'gb',
            'fb',
            'ld',
            'iffb',
            'pitches',
            'balls',
            'strikes',
            'ifh',
            'bu',
            'buh',
            'bb_pct',
            'k_pct',
            'bb_k',
            'obp',
            'slg',
            'ops',
            'iso',
            'babip',
            'gb_fb',
            'ld_pct',
            'gb_pct',
            'fb_pct',
            'hr_fb',
            'iffb_pct',
            'ifh_pct',
            'buh_pct',
            'woba',
            'wraa',
            'wrc',
            'bat',
            'fld',
            'rep',
            'pos',
            'rar',
            'war',
            'spd',
            'wrc_plus',
            'wpa',
            'wpa_minus',
            'wpa_plus',
            're24',
            'rew',
            'pli',
            'phli',
            'ph',
            'wpali',
            'clutch',
            'fb_pct',
            'fbv',
            'sl_pct',
            'slv',
            'ct_pct',
            'ctv',
            'cb_pct',
            'cbv',
            'ch_pct',
            'chv',
            'sf_pct',
            'sfv',
            'kn_pct',
            'knv',
            'xx_pct',
            'po_pct',
            'wfb',
            'wsl',
            'wct',
            'wcb',
            'wch',
            'wsf',
            'wkn',
            'wfbc',
            'wslc',
            'wctc',
            'wcbc',
            'wchc',
            'wsfc',
            'wknc',
            'oswing_pct',
            'zswing_pct',
            'swing_pct',
            'ocontact_pct',
            'zcontact_pct',
            'contact_pct',
            'zone_pct',
            'fstrike_pct',
            'swstr_pct',
            'bsr',
            'fa_pct_pfx',
            'ft_pct_pfx',
            'fc_pct_pfx',
            'fs_pct_pfx',
            'fo_pct_pfx',
            'si_pct_pfx',
            'sl_pct_pfx',
            'cu_pct_pfx',
            'kc_pct_pfx',
            'ep_pct_pfx',
            'ch_pct_pfx',
            'sc_pct_pfx',
            'kn_pct_pfx',
            'un_pct_pfx',
            'vfa_pfx',
            'vft_pfx',
            'vfc_pfx',
            'vfs_pfx',
            'vfo_pfx',
            'vsi_pfx',
            'vsl_pfx',
            'vcu_pfx',
            'vkc_pfx',
            'vep_pfx',
            'vch_pfx',
            'vsc_pfx',
            'vkn_pfx',
            'fa_x_pfx',
            'ft_x_pfx',
            'fc_x_pfx',
            'fs_x_pfx',
            'fo_x_pfx',
            'si_x_pfx',
            'sl_x_pfx',
            'cu_x_pfx',
            'kc_x_pfx',
            'ep_x_pfx',
            'ch_x_pfx',
            'sc_x_pfx',
            'kn_x_pfx',
            'fa_z_pfx',
            'ft_z_pfx',
            'fc_z_pfx',
            'fs_z_pfx',
            'fo_z_pfx',
            'si_z_pfx',
            'sl_z_pfx',
            'cu_z_pfx',
            'kc_z_pfx',
            'ep_z_pfx',
            'ch_z_pfx',
            'sc_z_pfx',
            'kn_z_pfx',
            'wfa_pfx',
            'wft_pfx',
            'wfc_pfx',
            'wfs_pfx',
            'wfo_pfx',
            'wsi_pfx',
            'wsl_pfx',
            'wcu_pfx',
            'wkc_pfx',
            'wep_pfx',
            'wch_pfx',
            'wsc_pfx',
            'wkn_pfx',
            'wfa_c_pfx',
            'wft_c_pfx',
            'wfc_c_pfx',
            'wfs_c_pfx',
            'wfo_c_pfx',
            'wsi_c_pfx',
            'wsl_c_pfx',
            'wcu_c_pfx',
            'wkc_c_pfx',
            'wep_c_pfx',
            'wch_c_pfx',
            'wsc_c_pfx',
            'wkn_c_pfx',
            'oswing_pct_pfx',
            'zswing_pct_pfx',
            'swing_pct_pfx',
            'ocontact_pct_pfx',
            'zcontact_pct_pfx',
            'contact_pct_pfx',
            'zone_pct_pfx',
            'pace',
            'defense',
            'wsb',
            'ubr']}

stat_functions = { stat: None for stat in (set(all_stats['batter']) | (set(stats['batter'])) | set(stats['pitcher'])) }

stat_functions['ops'] = stat_ops
stat_functions['runrate'] = stat_runrate
stat_functions['rbirate'] = stat_rbirate
stat_functions['sbrate'] = stat_sbrate
stat_functions['csrate'] = stat_csrate
stat_functions['saverate'] = stat_saverate
stat_functions['winrate'] = stat_winrate
stat_functions['krate'] = stat_krate
stat_functions['tob'] = stat_tob
stat_functions['gr'] = stat_gr
stat_functions['gfrac'] = stat_gfrac
stat_functions['winrate_gf'] = stat_winrate_gf
stat_functions['winrate_ngf'] = stat_winrate_ngf


for player_type in player_types:


    for proj_year in model_years:
        all_years = range(2004,proj_year)
        proj_years = range(2004+lag_years,proj_year)

        csvfile = "Lasso_" + player_type + "%d.csv" % proj_year

        models = {}
        final_projs = {}

        ivars = {}
        ivars2 = []
        depvars = {}
        ptvars = {}

        player_lists = {}

        proj_stats = set(stats[player_type]) | set(all_stats[player_type])

        data = pm.get_player_year_data(all_years,
                                        ['actual'],player_type,
                                        proj_stats, stat_functions,
                                        True)
        
        for stat in stats[player_type]:

            actuals = pm.get_player_year_data(proj_years, ['actual'],
                                              player_type, [stat],
                                              stat_functions)[stat]

            pset = set(actuals.keys())

            ptstat = ptstats[stat]

            if ptstat is not None:

                actualspt = pm.get_player_year_data(proj_years, ['actual'], 
                                            player_type, [ptstat], 
                                            stat_functions)[ptstat]
                pset = pset & set(actualspt.keys())
     

            player_years = list(pset)
                
            player_lists[stat] = player_years

            ivars[stat] = []
            depvars[stat] = []
            ptvars[stat] = []
            coef_cols = []

            for i in range(1,lag_years+1):
                for st in proj_stats:
                    coef_cols.append("%s_lag_%d" % (st, i))
                    coef_cols.append("%s_lag_%d_missing" % (st, i))
               
            for pyear in player_years:
                row = []

                vals = pyear.split('_')
        
                for i in range(1,lag_years+1):
                    prev_pyear = "%s_%d" % (vals[0],int(vals[1])-i)

                    for st in proj_stats:
                        if prev_pyear in data[st] and data[st][prev_pyear]['actual'] is not None:
                            row.extend([data[st][prev_pyear]['actual']])
                            row.extend([0])
                        else:
                            row.extend([0])
                            row.extend([1])
                
                ivars[stat].append(row)
                depvars[stat].append(actuals[pyear]['actual'])
                
                if ptstat is not None:
                    ptvars[stat].append(actualspt[pyear]['actual'])

            x0 = numpy.array(ivars[stat])
            y = numpy.array(depvars[stat])
     
            # start adding in auxiliaries
            aux =     get_year_var(player_years, proj_years)
      
            aux_cols = list(map(lambda yr: 'yr_lt_%d' % yr, proj_years[0:-1]))

            if use_ages:
                ages =    get_age_var(player_years, proj_years, 'actual', player_type, pm,-1)
                aux = numpy.hstack((aux,ages))
                aux_cols.extend(['ages'])

            aux2 = aux
            
      #      aux2 = add_quad_interactions(aux)
      #      aux_cols.extend(["%s * %s" % (c1, c2)
      #                  for (c1, c2) in itertools.combinations(aux_cols, 2)])

            if use_teams:
                teams   = get_team_vars(player_years, proj_years, 'actual', player_type, pm)
                aux2 = numpy.hstack((aux2,teams))
                aux_cols.extend(list(map(lambda team: 'team_%s' % team, helper.valid_teams[2:])))

            use_x2vars = x2vars
            #or (special_winrate and stat == 'winrate')

            x = get_final_regs(x0,aux2,-1,use_x2vars)
            #x = numpy.hstack((x0,aux2))
            
            cross_cols = []
            for i in range(len(coef_cols)):
                if use_x2vars:
                    for j in range(i, len(coef_cols)):
                        cross_cols.append("%s * %s" % (coef_cols[i], coef_cols[j]))
                for aux_col in aux_cols:
                    cross_cols.append("%s * %s" % (coef_cols[i], aux_col))

            coef_cols.extend(aux_cols)
            coef_cols.extend(cross_cols)

            using_gls = use_gls and ptstat is not None

            if use_lars:
                models[stat] = LassoLarsCV(cv=cv_num, normalize=norm and not using_gls, fit_intercept=not using_gls, max_iter = num_iter)
            elif use_aic:
                models[stat] = LassoLarsIC(criterion='aic', normalize=norm and not using_gls, fit_intercept=not using_gls, max_iter = num_iter)
            else:
                models[stat] = LassoCV(cv=cv_num, normalize=norm and not using_gls, fit_intercept=not using_gls, max_iter = num_iter)

            if using_gls:
                pt = numpy.array(ptvars[stat])
                for j in range(0,len(x[0])):
                    x[:,j] = standardize(x[:,j],1)
                msqpt = numpy.mean(numpy.sqrt(pt))
                y = numpy.multiply(y,numpy.sqrt(pt)) / msqpt
                x = numpy.dot(numpy.diag(numpy.sqrt(pt)),x)
                x = numpy.hstack((x,numpy.sqrt(pt).reshape(-1,1))) / msqpt
                coef_cols.extend(['intercept'])

     

                
            models[stat].fit(x,y)

            print("Model for " + stat)
            print("Num of player-seasons in sample: " + str(len(player_years)))
            if len(coef_cols) != len(models[stat].coef_):
                print("WARNING COL MISMATCH")
            else:
                for coef_col, coef in zip(coef_cols, models[stat].coef_):
                    if not (coef == 0 and print_nonzero_coefs_only):
                        print("%40s : %f" % (coef_col, coef))
                if not using_gls:
                    print("%40s : %f" % ('intercept', models[stat].intercept_))
            #print models[stat].coef_
            #print models[stat].intercept_

        # choose a sample to forecast
        pecota_sample = pm.get_player_year_data([proj_year], ['pecota'],
                                              player_type, ['pa'],
                                              stat_functions)['pa']

        pset = set(pecota_sample.keys())
        player_years = list(pset)

        for pyear in player_years:
            row = []

            vals = pyear.split('_')
        
            for i in range(1,lag_years+1):
                prev_pyear = "%s_%d" % (vals[0],int(vals[1])-i)

                for st in proj_stats:
                    if prev_pyear in data[st] and data[st][prev_pyear]['actual'] is not None:
                        row.extend([data[st][prev_pyear]['actual']])
                        row.extend([0])
                    else:
                        row.extend([0])
                        row.extend([1])
                
            ivars2.append(row)

        x2 = numpy.array(ivars2)

        aux =     get_year_var(player_years, proj_years)
      

     
        ages =    get_age_var(player_years, [proj_year], 'actual', player_type, pm,-1)

        if use_ages:
            aux = numpy.hstack((aux,ages))

        aux2 = aux
            
      #      aux2 = add_quad_interactions(aux)


        if use_teams:
            teams   = get_team_vars(player_years, [proj_year], 'actual', player_type, pm)
            aux2 = numpy.hstack((aux2,teams))
             
        use_x2vars = x2vars
            #or (special_winrate and stat == 'winrate')

        x3 = get_final_regs(x2,aux2,-1,use_x2vars)
        #x3 = numpy.hstack((x2,aux2))

       

        for stat in stats[player_type]:
            ptstat = ptstats[stat]

            using_gls = use_gls and ptstat is not None
            x4 = x3.copy()
            if using_gls:
                for j in range(0,len(x4[0])):
                    x4[:,j] = standardize(x4[:,j],1)
                x4 = numpy.hstack((x4, numpy.ones_like(ages)))
                
            final_stat_proj = models[stat].predict(x4)
            final_projs[stat] = dict(zip(player_years,final_stat_proj))

        cols = ['fg_id']
        #,'last_name','first_name']
        cols.extend(stats[player_type])

        playing_time = playing_times[player_type]

        with open(csvfile, 'w') as f:

            writer = csv.DictWriter(f, cols)
            writer.writeheader()

            player_years.sort(key=lambda k: final_projs[playing_time][k])
            player_years.reverse()

            for k in player_years:
                vals = k.split('_')
                row = {'fg_id': vals[0]}
                     #  'last_name': pecota_sample['last_name'][k]['pecota'],
                     #  'first_name': pecota_sample['first_name'][k]['pecota']}

                for stat in stats[player_type]:
                    row[stat] = final_projs[stat][k]
                writer.writerow(row)


          
