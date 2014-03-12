from baseballprojections import helper
from baseballprojections import projectionmanager as pm
from baseballprojections.schema import *
import os.path

class MyProjectionManager(pm.ProjectionManager):

    # Hardcoded function to read everything

    def read_everything_csv(self, base_dir, read_register=True, verbose=False):

        if read_register:
            print('Reading Chadwick Register...')
            self.read_register(os.path.join(base_dir, 'register.csv'), verbose=verbose)

        print('Reading PECOTA 2011...')
        self.read_pecota_batters_2011(os.path.join(base_dir, 'PecotaHitters2011.csv'), verbose=verbose)
        self.read_pecota_pitchers_2011(os.path.join(base_dir, 'Pecota Pitchers 2011.csv'), verbose=verbose)

        print('Reading PECOTA 2012...')
        self.read_pecota_batters_2012(os.path.join(base_dir, 'PecotaHitters2012.csv'), verbose=verbose)
        self.read_pecota_pitchers_2012(os.path.join(base_dir, 'Pecota Pitchers 2012.csv'), verbose=verbose)
        
        print('Reading PECOTA 2013...')
        self.read_pecota_batters_2013(os.path.join(base_dir, 'PecotaHitters2013.csv'),verbose=verbose)
        self.read_pecota_pitchers_2013(os.path.join(base_dir, 'Pecota Pitchers 2013.csv'), verbose=verbose)

        print('Reading PECOTA 2014...')
        self.read_pecota_batters_2014(os.path.join(base_dir, 'PecotaHitters2014.csv'),verbose=verbose)
        self.read_pecota_pitchers_2014(os.path.join(base_dir, 'Pecota Pitchers 2014.csv'), verbose=verbose)
        self.read_pecota_pfm_2014(os.path.join(base_dir, 'BP_PFM_2014.csv'),verbose=verbose)

        print('Reading Steamer 2011...')
        self.read_steamer_batters_2011(os.path.join(base_dir, 'SteamerHitters2011.csv'), verbose=verbose)
        self.read_steamer_pitchers_2011(os.path.join(base_dir, 'Steamer Pitchers 2011.csv'), verbose=verbose)

        print('Reading Steamer 2012...')
        self.read_steamer_batters_2012(os.path.join(base_dir, 'SteamerHitters2012.csv'), verbose=verbose)
        self.read_steamer_pitchers_2012(os.path.join(base_dir, 'Steamer Pitchers 2012.csv'), verbose=verbose)

        print('Reading Steamer 2013...')
        self.read_steamer_batters_2013(os.path.join(base_dir, 'SteamerHitters2013.csv'), verbose=verbose)
        self.read_steamer_pitchers_2013(os.path.join(base_dir, 'Steamer Pitchers 2013.csv'), verbose=verbose)

        print('Reading Steamer 2014...')
        self.read_steamer_batters_2014(os.path.join(base_dir, 'SteamerHitters2014.csv'), verbose=verbose)
        self.read_steamer_pitchers_2014(os.path.join(base_dir, 'Steamer Pitchers 2014.csv'), verbose=verbose)


        print('Reading ZIPS 2011...')
        self.read_zips_batters_2011(os.path.join(base_dir, 'ZIPSHitters2011.csv'), verbose=verbose)
        self.read_zips_pitchers_2011(os.path.join(base_dir, 'ZIPS Pitchers 2011.csv'), verbose=verbose)

        print('Reading ZIPS 2012...')
        self.read_zips_batters_2012(os.path.join(base_dir, 'ZIPSHitters2012.csv'), verbose=verbose)
        self.read_zips_pitchers_2012(os.path.join(base_dir, 'ZIPS Pitchers 2012.csv'), verbose=verbose)

        print('Reading ZIPS 2013...')
        self.read_zips_batters_2013(os.path.join(base_dir, 'ZIPSHitters2013.csv'), verbose=verbose)
        self.read_zips_pitchers_2013(os.path.join(base_dir, 'ZIPS Pitchers 2013.csv'), verbose=verbose)

        print('Reading ZIPS 2014...')
        self.read_zips_batters_2014(os.path.join(base_dir, 'ZipsHitters2014.csv'), verbose=verbose)
        self.read_zips_pitchers_2014(os.path.join(base_dir, 'ZIPS Pitchers 2014.csv'), verbose=verbose)

        print('Reading Actuals 2011...')
        self.read_actuals_batters_2011(os.path.join(base_dir, 'ActualsHitters2011.csv'), verbose=verbose)
        self.read_actuals_pitchers_2011(os.path.join(base_dir, 'ActualsPitchers2011.csv'), verbose=verbose)

        print('Reading Actuals 2012...')
        self.read_actuals_batters_2012(os.path.join(base_dir, 'ActualsHitters2012.csv'), verbose=verbose)
        self.read_actuals_pitchers_2012(os.path.join(base_dir, 'ActualsPitchers2012.csv'), verbose=verbose)

        print('Reading Actuals 2013...')
        self.read_actuals_batters_2013(os.path.join(base_dir, 'ActualsHitters2013.csv'), verbose=verbose)
        self.read_actuals_pitchers_2013(os.path.join(base_dir, 'ActualsPitchers2013.csv'), verbose=verbose)


    # This reads the Chadwick register, to load up all the IDs.

    def read_register(self, filename, verbose=False):

        header_row = ['chadwick_short_id', 'chadwick_id', 
                      'mlb_id', 'retrosheet_id', 'br_id', 'br_minor_id', 
                      'bp_id', 'davenport_id', 'fg_id', 'fg_minor_id', 'npb_id', 
                      'last_name', 'first_name', '', '', '', '', 
                      'bats', 'throws', 'height', 'weight', 
                      'birth_year', 'birth_month', 'birth_day']
        self.read_player_csv(filename, 
                             header_row=header_row, 
                             post_processor=register_processor,
                             verbose=verbose)

    # Actuals readers
    
    def read_fangraphs_batters(self, filename, verbose=False):

        fg_batter_header = \
            [
            'year', 
            'full_name', 
            'team',
            'age',
            'g',
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
            '',     # skip dollars
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
            'wpa_li',
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
            'fapct_pfx',
            'ftpct_pfx',
            'fcpct_pfx',
            'fspct_pfx',
            'fopct_pfx',
            'sipct_pfx',
            'slpct_pfx',
            'cupct_pfx',
            'kcpct_pfx',
            'eppct_pfx',
            'chpct_pfx',
            'scpct_pfx',
            'knpct_pfx',
            'unpct_pfx',
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
            'ubr',
            '',     # skip age range
            'off',
            'lg',
            'fangraphs_id',
            ]

        self.read_projection_csv(os.path.join(base_dir, 'filename'), 
                                 'actual', 
                                 range(2004, 2014), 
                                 is_actual=True, 
                                 projection_type='batter', 
                                 header_row=fg_batter_header,
                                 post_processor=helper.batter_post_processor, 
                                 verbose=verbose)


    def read_actuals_pitchers_2011(self, filename, verbose=False):

        header_row = ['full_name', 'team', 'w', 'sv', 'g', 'gs', 'ip', 
                      'era', 'k9', 'h', 'bb', 'fg_id', 'rookie']
        self.read_projection_csv(filename, 'actual', 2011,
                                 is_actual=True,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=actual_pitcher_post_processor,
                                 verbose=verbose)



    def read_pecota_pitchers_2011(self, filename, verbose=False):

        header_row = ['last_name', 'first_name', 'team', '', '', '', '', '', 
                      '', 'birthdate', 'w', 'l', 'sv', 'g', 'gs', 'ip', 'h', 
                      'hr', 'bb', 'hbp', 'k', '', '', '', '', 'whip', 'era', 
                      '', '', '', '', '', '', '', '', 'mlb_id',
                      'retrosheet_id', 'lahman_id']
        self.read_projection_csv(filename, 'pecota', 2011,
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=pecota_dc_pitcher_post_processor,
                                 verbose=verbose)

    def read_pecota_batters_2012(self, filename, verbose=False):

        header_row = ['mlb_id','bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      '', 'team', '', '', '', 'pa', 'ab', 'r', 'h1b', 'h2b', 
                      'h3b', 'hr', 'h', '', 'rbi', 'bb', 'hbp', 'k', 'sac', 
                      'sf', '', 'sb', 'cs', '', 'obp', 'slg', '', '', '', '', '', '',
                      '', '', '', '', '', '', 'dc_fl']
        self.read_projection_csv(filename, 'pecota', 2012, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=pecota_dc_batter_post_processor,
                                 verbose=verbose)

    def read_pecota_pitchers_2012(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      'team', '', '', '', 'w', 'l', '', 'sv', 'g', 'gs', 'ip', 
                      'h', 'hr', 'bb', 'k', '', '', '', '', 'whip', 'era', '', 
                      '', '', '', '', '', '', '', 'dc_fl', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2012,
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=pecota_dc_pitcher_post_processor,
                                 verbose=verbose)

    def read_pecota_batters_2013(self, filename, verbose=False):

        header_row = ['mlb_id','full_name','bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      '','team', '', '', '', 'pa', 'ab', 'r', 'h1b', 'h2b', 
                      'h3b', 'hr', 'h', '', 'rbi', 'bb', 'hbp', 'k', 'sac', 
                      'sf', '', 'sb', 'cs', '', 'obp', 'slg', '', '', '', '', '', '',
                      '', '', '', '', '', '', 'dc_fl', 'rookie_fl']
        self.read_projection_csv(filename, 'pecota', 2013, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=pecota_rdc_batter_post_processor,
                                 verbose=verbose)

    def read_pecota_pitchers_2013(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      'team', '', '', '', 'w', 'l', '', 'sv', 'g', 'gs', 'ip', 
                      'h', 'hr', 'bb', 'k', '', '', '', '', 'whip', 'era', '', 
                      '', '', '', '', '', '', '', 'dc_fl', 'rookie_fl', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2013,
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=pecota_rdc_pitcher_post_processor,
                                 verbose=verbose)

    def read_pecota_pfm_2014(self, filename, verbose=False):

        header_row = ['full_name', 'positions', 'mlb_id', '', '', '', '', 'dollars']
        self.read_projection_csv(filename, 'pfm', 2014, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=pfm_processor,
                                 verbose=verbose)

    def read_pecota_batters_2014(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', 'positions', '', '', '', '', 
                      '','team', '', '', '', 'pa', 'ab', 'r', 'h1b', 'h2b', 
                      'h3b', 'hr', 'h', '', 'rbi', 'bb', 'hbp', 'k', 'sac', 
                      'sf', '', 'sb', 'cs', '', 'obp', 'slg', '', '', '', '', '', '',
                      '', '', '', '', '', '', '', '','','','dc_fl','rookie_fl','mlb_id','','']
        self.read_projection_csv(filename, 'pecota', 2014, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=pecota_rdc_batter_post_processor,
                                 verbose=verbose)

    def read_pecota_pitchers_2014(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      'team', '', '', '', 'w', 'l', '', 'sv', 'g', 'gs', 'ip', 
                      'h', 'hr', 'bb', 'hbp','k', '', '', '', '', 'whip', 'era', '', 
                      '', '', '', '', '', '', '', 'dc_fl', 'rookie_fl', 'mlb_id','','']
        self.read_projection_csv(filename, 'pecota', 2014,
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=pecota_rdc_pitcher_post_processor,
                                 verbose=verbose)

    # ZIPS readers

    def read_zips_batters_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'last_name', 'first_name', 'team', 
                      '', '', '', '', '', 'avg', 'obp', 'slg', '', 'ab', 'r', 
                      'h', 'h2b', 'h3b', 'hr', 'rbi', 'bb', 'k', 'hbp', 'sb', 
                      'cs', 'sac', 'sf', '', '', '', 'pa']
        self.read_projection_csv(filename, 'zips', 2011, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=zips_batter_post_processor,
                                 verbose=verbose)

    def read_zips_pitchers_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'last_name', 'first_name', 'team', 
                      '', '', '', 'w', 'l', 'era', 'g', 'gs', 'ip', 'h', 'r', 
                      'er', 'hr', 'bb', 'k', 'wp', '', 'hbp']
        self.read_projection_csv(filename, 'zips', 2011, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=zips_pitcher_post_processor,
                                 verbose=verbose)

    def read_zips_batters_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', '', 'avg', 'obp', 
                      'slg', '', 'ab', 'r', 'h', 'h2b', 'h3b', 'hr', 'rbi', 
                      'bb', 'k', 'hbp', 'sb', 'cs', 'sac', 'sf', '', '', '', 'pa']
        self.read_projection_csv(filename, 'zips', 2012, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=zips_batter_post_processor,
                                 verbose=verbose)

    def read_zips_pitchers_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', 'w', 'l', 'era', 
                      'g', 'gs', 'ip', 'h', 'r', 'er', 'hr', 'bb', 'k', 'wp', '', 
                      'hbp']
        self.read_projection_csv(filename, 'zips', 2012, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=zips_pitcher_post_processor,
                                 verbose=verbose)

    def read_zips_batters_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', '', 'avg', 'obp', 
                      'slg', '', 'pa', 'ab', 'r', 'h', 'h2b', 'h3b', 'hr', 
                      'rbi', 'bb', 'k', 'hbp', 'sb', 'cs', 'sac', 'sf']
        self.read_projection_csv(filename, 'zips', 2013, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=zips_batter_post_processor,
                                 verbose=verbose)
        
    def read_zips_batters_2014(self, filename, verbose=False):

        header_row = ['full_name', 'g','pa', 'ab', 'h', 'h2b', 'h3b', 'hr', 
                      'r','rbi', 'bb', 'k', 'hbp', 'sb', 'cs', 'avg', 'obp','slg','','','','','','fg_id']
        self.read_projection_csv(filename, 'zips', 2014, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_zips_pitchers_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', 'w', 'l', 'era', 
                      'g', 'gs', 'ip', 'h', 'r', 'er', 'hr', 'bb', 'k', 'wp', '', 
                      'hbp']
        self.read_projection_csv(filename, 'zips', 2013, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=zips_pitcher_post_processor,
                                 verbose=verbose)

    def read_zips_pitchers_2014(self, filename, verbose=False):

        header_row = [ 'full_name', 'w', 'l', 'era', 'gs', 'g', 'ip', 
                      'h', 'er', 'hr', 'k', 'bb', 'whip', '', '', '', '', 'fg_id'] 
        self.read_projection_csv(filename, 'zips', 2014, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    # Steamer readers

    def read_steamer_batters_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', '', 'team', '', '', '', '', '',
                      'pa', 'bb', 'hbp', 'sac', 'sf', 'ab', 'k', '', 'h', 
                      'h1b', 'h2b', 'h3b', 'hr', '', 'sb', 'cs', 'avg', 'obp', 
                      'slg', 'ops', '', 'r', 'rbi']
        self.read_projection_csv(filename, 'steamer', 2011, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_steamer_pitchers_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', '', '', '', 'team', '', '', '', 
                      'ip', 'g', 'gs', '', '', '', '', 'k', 'bb', 'hbp', '', 'hr',
                      '', '', '', '', 'era', 'er', 'h', 'whip', '', '', 'w', 
                      'l', 'sv']
        self.read_projection_csv(filename, 'steamer', 2011, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    def read_steamer_batters_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', '', '', '', '', '', 'team', '', 
                      '', '', 'pa', 'ab', 'bb', 'hbp', 'sac', 'sf', 'k', '', 
                      '', 'h', 'h3b', 'h2b', 'h1b', 'hr', 'r', 'rbi', 'sb', 
                      'cs', 'avg', 'obp', 'slg']
        self.read_projection_csv(filename, 'steamer', 2012, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_steamer_pitchers_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', '', '', 'birthdate', '', 'team', 
                      '', 'g', 'gs', 'ip', '', '', '', '', '', '', '',  'k', 'bb', 
                      'hbp', 'h', '', 'hr', '', '', '', '', 'era', '', '', 
                      'er', 'whip', 'w', 'l', 'sv']
        self.read_projection_csv(filename, 'steamer', 2012, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    def read_steamer_batters_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'first_name', 'last_name', 'positions', 
                      '', '', 'team', 'pa', '', '', 'bb', 'k', 'hbp', '', 
                      'sac', 'sf', 'ab', 'h', 'h1b', 'h2b', 'h3b', 'hr', 'avg',
                      'obp', 'slg', '', 'sb', 'cs', 'r', 'rbi']
        self.read_projection_csv(filename, 'steamer', 2013, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_steamer_pitchers_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name','first_name', 'last_name', 'ip',
                      'g', 'gs', '', 'sv', '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', '', '', 'era', 'ra', 'k', 'bb', 
                      'hbp', '', '', 'hr9', 'h', 'er', 'r', 'whip', 'w', 'l']
        self.read_projection_csv(filename, 'steamer', 2013, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=steamer2013_post_processor,
                                 verbose=verbose)
        
    def read_steamer_batters_2014(self, filename, verbose=False):

        header_row = ['full_name', 'pa', 'ab', 'h', 'h2b', 'h3b', 'hr', 
                      'r','rbi', 'bb', 'k', 'hbp', 'sb', 'cs', 'avg', 'obp','slg','','','','','','fg_id']
        self.read_projection_csv(filename, 'steamer', 2014, 
                                 is_actual=False,
                                 projection_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_steamer_pitchers_2014(self, filename, verbose=False):

        header_row = [ 'full_name', 'w', 'l', 'era', 'gs', 'g', 'sv','ip', 
                      'h', 'er', 'hr', 'k', 'bb', 'whip', '', '', '', '', 'fg_id'] 
        self.read_projection_csv(filename, 'steamer', 2014, 
                                 is_actual=False,
                                 projection_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

def register_processor(x):

    if x['br_id'] is None or x['br_id']=='':
        x['br_id'] = x['br_minor_id']

    if x['fg_id'] is None or x['fg_id']=='':
        x['fg_id'] = x['fg_minor_id']

    for id in ['chadwick_id', 'mlb_id', 'fg_id']:
        if x[id] == '': 
            x[id] = None

    if (x['birth_year'] is not None and x['birth_day'] is not None and x['birth_month'] is not None and
        len(x['birth_year'])>0 and len(x['birth_day'])>0 and len(x['birth_month'])>0):
        strdate= '%s/%s/%s' % (x['birth_month'],x['birth_day'],x['birth_year'])
        try:
            x['birthdate']= datetime.datetime.strptime(strdate.rstrip(), '%m/%d/%Y')
        except Exception as e:
            print('Error computing birthdate')
            print(x)

    return x

def pfm_processor(x):
    if x['positions'] in ['RP','SP','Swing']:
        return {}
    else:
        return x

def zips_batter_post_processor(x):
    if x['mlb_id'] in ['#N/A','']:
        del x['mlb_id']

    return helper.batter_post_processor(x)

def zips_pitcher_post_processor(x):
    if x['mlb_id'] in ['#N/A','']:
        del x['mlb_id']

    return helper.pitcher_post_processor(x)

def pecota_dc_batter_post_processor(x):
    x2 = helper.batter_post_processor(x)
    
    if 'dc_fl' not in x2:
        x2['dc_fl'] = 'NA'
    return x2

def pecota_dc_pitcher_post_processor(x):

    x2 = helper.pitcher_post_processor(x)

    if 'dc_fl' not in x2:
        x2['dc_fl'] = 'NA'

    return x2

def pecota_rdc_pitcher_post_processor(x):
    if x['rookie_fl']=='T':
        x['rookie']=1
    elif x['rookie_fl']=='F':
        x['rookie']=0
    else:
        x['rookie']=None
    return helper.pitcher_post_processor(x)

def pecota_rdc_batter_post_processor(x):
    if x['rookie_fl']=='T':
        x['rookie']=1
    elif x['rookie_fl']=='F':
        x['rookie']=0
    else:
        x['rookie']=None
    return pecota_dc_batter_post_processor(x)



def actual_pitcher_post_processor(x):
    '''
    Convert K/9 to K
    '''
    try: x['k'] = float(x['k9']) / 9.0 * float(x['ip'])
    except: pass
    return helper.pitcher_post_processor_with_ip_fix(x)

def steamer2013_post_processor(x):
    '''
    Post-processor specially for Steamer 2013, which weirdly includes only an
    HR/9 field but not an HR field
    '''

    try: x['hr'] = float(x['hr9']) / 9.0 * float(x['ip'])
    except: pass
    return helper.pitcher_post_processor(x)
