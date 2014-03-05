from baseballprojections import helper
from baseballprojections import projectionmanager as pm
from baseballprojections.schema import *
import os.path




class MyProjectionManager(pm.ProjectionManager):

    def read_fangraphs_actuals(self, base_dir, verbose=False):

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

        fg_pitcher_header = \
            ['year', 
            'full_name', 
            'team',
            'age',
            'w',
            'l',
            'era',
            'g',
            'gs',
            'cg',
            'sho',
            'sv',
            'bs',
            'ip',
            'tbf',
            'h',
            'r',
            'er',
            'hr',
            'bb',
            'ibb',
            'hbp',
            'wp',
            'bk',
            'k',
            'gb',
            'fb',
            'ld',
            'iffb',
            'balls',
            'strikes',
            'pitches',
            'rs',
            'ifh',
            'bu',
            'buh',
            'k9',
            'bb9',
            'k_bb',
            'h9',
            'hr9',
            'avg',
            'whip',
            'babip',
            'lob_pct',
            'fip',
            'gb_fb',
            'ld_pct',
            'gb_pct',
            'fb_pct',
            'iffb_pct',
            'hr_fb',
            'ifh_pct',
            'buh_pct',
            'starting',
            'start_ip',
            'relieving',
            'relief_ip',
            'rar',
            'war',
            '',         # skip dollars
            'tera',
            'xfip',
            'wpa',
            'wpa_minus',
            'wpa_plus',
            're24',
            'rew',
            'pli',
            'inli',
            'gmli',
            'exli',
            'pulls',
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
            'hld',
            'sd',
            'md',
            'era_minus',
            'fip_minus',
            'xfip_minus',
            'k_pct',
            'bb_pct',
            'siera',
            'rs9',
            'ef',
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
            'ra9_war',
            'bip_wins',
            'lob_wins',
            'fdp_wins',
            '',         # skip age range
            'fangraphs_id'
            ]

        self.read_projection_csv(os.path.join(base_dir, 'data/FanGraphs Actual Batting 2004-2013.csv'), 
                                 'actual', 
                                 list(range(2004, 2014)), 
                                 is_actual=True, 
                                 player_type='batter', 
                                 header_row=fg_batter_header,
                                 post_processor=helper.batter_post_processor, 
                                 verbose=verbose)

        self.read_projection_csv(os.path.join(base_dir, 'data/FanGraphs Actual Pitching 2004-2013.csv'), 
                                 'actual', 
                                 list(range(2004, 2014)), 
                                 is_actual=True, 
                                 player_type='pitcher', 
                                 header_row=fg_pitcher_header,
                                 post_processor=helper.pitcher_post_processor, 
                                 verbose=verbose)


    # Hardcoded function to read everything

    def read_everything_csv(self, base_dir, verbose=False):

        print('Reading PECOTA 2011...')
        self.read_pecota_batters_2011(os.path.join(base_dir, 'Pecota Hitters 2011.csv'), verbose=verbose)
        self.read_pecota_pitchers_2011(os.path.join(base_dir, 'Pecota Pitchers 2011.csv'), verbose=verbose)

        print('Reading PECOTA 2012...')
        self.read_pecota_batters_2012(os.path.join(base_dir, 'Pecota Hitters 2012.csv'), verbose=verbose)
        self.read_pecota_pitchers_2012(os.path.join(base_dir, 'Pecota Pitchers 2012.csv'), verbose=verbose)
        
        print('Reading PECOTA 2013...')
        self.read_pecota_batters_2013(os.path.join(base_dir, 'Pecota Hitters 2013.csv'),verbose=verbose)
        self.read_pecota_pitchers_2013(os.path.join(base_dir, 'Pecota Pitchers 2013.csv'), verbose=verbose)

        print('Reading Steamer 2011...')
        self.read_steamer_batters_2011(os.path.join(base_dir, 'Steamer Hitters 2011.csv'), verbose=verbose)
        self.read_steamer_pitchers_2011(os.path.join(base_dir, 'Steamer Pitchers 2011.csv'), verbose=verbose)

        print('Reading Steamer 2012...')
        self.read_steamer_batters_2012(os.path.join(base_dir, 'Steamer Hitters 2012.csv'), verbose=verbose)
        self.read_steamer_pitchers_2012(os.path.join(base_dir, 'Steamer Pitchers 2012.csv'), verbose=verbose)

        print('Reading Steamer 2013...')
        self.read_steamer_batters_2013(os.path.join(base_dir, 'Steamer Hitters 2013.csv'), verbose=verbose)
        self.read_steamer_pitchers_2013(os.path.join(base_dir, 'Steamer Pitchers 2013.csv'), verbose=verbose)

        print('Reading ZIPS 2011...')
        self.read_zips_batters_2011(os.path.join(base_dir, 'ZIPS Hitters 2011.csv'), verbose=verbose)
        self.read_zips_pitchers_2011(os.path.join(base_dir, 'ZIPS Pitchers 2011.csv'), verbose=verbose)

        print('Reading ZIPS 2012...')
        self.read_zips_batters_2012(os.path.join(base_dir, 'ZIPS Hitters 2012.csv'), verbose=verbose)
        self.read_zips_pitchers_2012(os.path.join(base_dir, 'ZIPS Pitchers 2012.csv'), verbose=verbose)

        print('Reading ZIPS 2013...')
        self.read_zips_batters_2013(os.path.join(base_dir, 'ZIPS Hitters 2013.csv'), verbose=verbose)
        self.read_zips_pitchers_2013(os.path.join(base_dir, 'ZIPS Pitchers 2013.csv'), verbose=verbose)

        print('Reading Actuals 2011...')
        self.read_actuals_batters_2011(os.path.join(base_dir, 'Actuals Hitters 2011.csv'), verbose=verbose)
        self.read_actuals_pitchers_2011(os.path.join(base_dir, 'Actuals Pitchers 2011.csv'), verbose=verbose)

        print('Reading Actuals 2012...')
        self.read_actuals_batters_2012(os.path.join(base_dir, 'Actuals Hitters 2012.csv'), verbose=verbose)
        self.read_actuals_pitchers_2012(os.path.join(base_dir, 'Actuals Pitchers 2012.csv'), verbose=verbose)

        print('Reading Actuals 2013...')
        self.read_actuals_batters_2013(os.path.join(base_dir, 'Actuals Hitters 2013.csv'), verbose=verbose)
        self.read_actuals_pitchers_2013(os.path.join(base_dir, 'Actuals Pitchers 2013.csv'), verbose=verbose)

    # Actuals readers


    
    def read_actuals_batters_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', 'pa', 'ab', 'r', 'rbi', 
                      'obp', 'slg', 'sb', 'cs', 'rookie', '']
        self.read_projection_csv(filename, 'actual', 2011,
                                 is_actual=True,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_actuals_pitchers_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', 'w', 'sv', 'g', 'gs', 'ip', 
                      'era', 'k9', 'h', 'bb', '', 'rookie']
        self.read_projection_csv(filename, 'actual', 2011,
                                 is_actual=True,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=actual_pitcher_post_processor,
                                 verbose=verbose)

    def read_actuals_batters_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', 'age', '', 'pa', 'ab', 
                      'obp', 'slg', 'r', 'rbi', 'sb', 'cs', 'rookie', '']
        self.read_projection_csv(filename, 'actual', 2012,
                                 is_actual=True,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_actuals_pitchers_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', 'w', 'sv', 'g', 'gs', 'ip', 
                      'era', 'k9', 'h', 'bb', '', 'hbp', '', 'rookie']
        self.read_projection_csv(filename, 'actual', 2012,
                                 is_actual=True,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=actual_pitcher_post_processor,
                                 verbose=verbose)
        
    def read_actuals_pitchers_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', 'w', 'sv', 'g', 'gs', 'ip', 
                      'era', 'k9', 'h', 'bb', '', 'hbp', '']
        self.read_projection_csv(filename, 'actual', 2013,
                                 is_actual=True,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=actual_pitcher_post_processor,
                                 verbose=verbose)

    def read_actuals_batters_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', 'pa', 'ab', 
                      'obp', 'slg', 'r', 'rbi', 'sb', 'cs', '']
        self.read_projection_csv(filename, 'actual', 2013,
                                 is_actual=True,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    # PECOTA readers

    def read_pecota_batters_2011(self, filename, verbose=False):

        header_row = ['last_name', 'first_name', 'team', '', '', '', '', '', 
                      '', 'birthdate', '', 'pa', 'ab', 'r', 'h1b', 'h2b', 
                      'h3b', 'hr', 'rbi', 'bb', 'hbp', 'k', 'sb', 'cs', 'sac', 
                      'sf', '', '', '', '', '', '', '', '', '', '', '', '', 
                      '', '', '', 'mlb_id', 'retrosheet_id', 'lahman_id']
        self.read_projection_csv(filename, 'pecota', 2011,
                                 is_actual=False,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_pecota_pitchers_2011(self, filename, verbose=False):

        header_row = ['last_name', 'first_name', 'team', '', '', '', '', '', 
                      '', 'birthdate', 'w', 'l', 'sv', 'g', 'gs', 'ip', 'h', 
                      'hr', 'bb', 'hbp', 'k', '', '', '', '', 'whip', 'era', 
                      '', '', '', '', '', '', '', '', 'mlb_id',
                      'retrosheet_id', 'lahman_id']
        self.read_projection_csv(filename, 'pecota', 2011,
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    def read_pecota_batters_2012(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      '', 'team', '', '', '', 'pa', 'ab', 'r', 'h1b', 'h2b', 
                      'h3b', 'hr', 'h', '', 'rbi', 'bb', 'hbp', 'k', 'sac', 
                      'sf', '', 'sb', 'cs', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', '', '', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2012, 
                                 is_actual=False,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_pecota_pitchers_2012(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      'team', '', '', '', 'w', 'l', '', 'sv', 'g', 'gs', 'ip', 
                      'h', 'hr', 'bb', 'k', '', '', '', '', 'whip', 'era', '', 
                      '', '', '', '', '', '', '', '', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2012,
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    def read_pecota_batters_2013(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      '', 'team', '', '', '', 'pa', 'ab', 'r', 'h1b', 'h2b', 
                      'h3b', 'hr', 'h', '', 'rbi', 'bb', 'hbp', 'k', 'sac', 
                      'sf', '', 'sb', 'cs', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', '', '', 'rookie_fl', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2013, 
                                 is_actual=False,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=pecota13_batter_post_processor,
                                 verbose=verbose)

    def read_pecota_pitchers_2013(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      'team', '', '', '', 'w', 'l', '', 'sv', 'g', 'gs', 'ip', 
                      'h', 'hr', 'bb', 'k', '', '', '', '', 'whip', 'era', '', 
                      '', '', '', '', '', '', '', '', 'rookie_fl', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2013,
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=pecota13_pitcher_post_processor,
                                 verbose=verbose)

    # ZIPS readers

    def read_zips_batters_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'last_name', 'first_name', 'team', 
                      '', '', '', '', '', 'avg', 'obp', 'slg', '', 'ab', 'r', 
                      'h', 'h2b', 'h3b', 'hr', 'rbi', 'bb', 'k', 'hbp', 'sb', 
                      'cs', 'sac', 'sf', '', '', '', 'pa']
        self.read_projection_csv(filename, 'zips', 2011, 
                                 is_actual=False,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_zips_pitchers_2011(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'last_name', 'first_name', 'team', 
                      '', '', '', 'w', 'l', 'era', 'g', 'gs', 'ip', 'h', 'r', 
                      'er', 'hr', 'bb', 'k', 'wp', '', 'hbp']
        self.read_projection_csv(filename, 'zips', 2011, 
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    def read_zips_batters_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', '', 'avg', 'obp', 
                      'slg', '', 'ab', 'r', 'h', 'h2b', 'h3b', 'hr', 'rbi', 
                      'bb', 'k', 'hbp', 'sb', 'cs', 'sac', 'sf', '', '', '', 'pa']
        self.read_projection_csv(filename, 'zips', 2012, 
                                 is_actual=False,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_zips_pitchers_2012(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', 'w', 'l', 'era', 
                      'g', 'gs', 'ip', 'h', 'r', 'er', 'hr', 'bb', 'k', 'wp', '', 
                      'hbp']
        self.read_projection_csv(filename, 'zips', 2012, 
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    def read_zips_batters_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', '', 'avg', 'obp', 
                      'slg', '', 'pa', 'ab', 'r', 'h', 'h2b', 'h3b', 'hr', 
                      'rbi', 'bb', 'k', 'hbp', 'sb', 'cs', 'sac', 'sf']
        self.read_projection_csv(filename, 'zips', 2013, 
                                 is_actual=False,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_zips_pitchers_2013(self, filename, verbose=False):

        header_row = ['mlb_id', 'full_name', 'team', '', '', 'w', 'l', 'era', 
                      'g', 'gs', 'ip', 'h', 'r', 'er', 'hr', 'bb', 'k', 'wp', '', 
                      'hbp']
        self.read_projection_csv(filename, 'zips', 2013, 
                                 is_actual=False,
                                 player_type='pitcher',
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
                                 player_type='batter',
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
                                 player_type='pitcher',
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
                                 player_type='batter',
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
                                 player_type='pitcher',
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
                                 player_type='batter',
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
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=steamer2013_post_processor,
                                 verbose=verbose)

def pecota13_pitcher_post_processor(x):
    if x['rookie_fl']=='T':
        x['rookie']=1
    elif x['rookie_fl']=='F':
        x['rookie']=0
    else:
        x['rookie']=None
    return helper.pitcher_post_processor(x)

def pecota13_batter_post_processor(x):
    if x['rookie_fl']=='T':
        x['rookie']=1
    elif x['rookie_fl']=='F':
        x['rookie']=0
    else:
        x['rookie']=None
    return helper.batter_post_processor(x)

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
