from baseballprojections import helper
from baseballprojections import projectionmanager as pm
from baseballprojections.schema import *
import os.path

class MyProjectionManager(pm.ProjectionManager):

    # Hardcoded function to read everything

    def read_everything_csv(self, base_dir, verbose=False):

        print('Reading PECOTA 2011...')
        self.read_pecota_batters_2011(os.path.join(base_dir, 'Pecota Hitters 2011.csv'), 
                                      verbose=verbose)
        self.read_pecota_pitchers_2011(os.path.join(base_dir, 'Pecota Pitchers 2011.csv'), 
                                       verbose=verbose)
        print('Reading PECOTA 2012...')
        self.read_pecota_batters_2012(os.path.join(base_dir, 'Pecota Hitters 2012.csv'),
                                      verbose=verbose)
        self.read_pecota_pitchers_2012(os.path.join(base_dir, 'Pecota Pitchers 2012.csv'), 
                                       verbose=verbose)
        print('Reading PECOTA 2013...')
        self.read_pecota_batters_2013(os.path.join(base_dir, 'Pecota Hitters 2013.csv'),
                                      verbose=verbose)
        self.read_pecota_pitchers_2013(os.path.join(base_dir, 'Pecota Pitchers 2013.csv'), 
                                       verbose=verbose)
        print('Reading Steamer 2011...')
        self.read_steamer_batters_2011(os.path.join(base_dir, 'Steamer Hitters 2011.csv'),
                                       verbose=verbose)
        self.read_steamer_pitchers_2011(os.path.join(base_dir, 'Steamer Pitchers 2011.csv'),
                                        verbose=verbose)
        print('Reading Steamer 2012...')
        self.read_steamer_batters_2012(os.path.join(base_dir, 'Steamer Hitters 2012.csv'),
                                       verbose=verbose)
        self.read_steamer_pitchers_2012(os.path.join(base_dir, 'Steamer Pitchers 2012.csv'),
                                        verbose=verbose)
        print('Reading Steamer 2013...')
        self.read_steamer_batters_2013(os.path.join(base_dir, 'Steamer Hitters 2013.csv'),
                                       verbose=verbose)
        self.read_steamer_pitchers_2013(os.path.join(base_dir, 'Steamer Pitchers 2013.csv'),
                                        verbose=verbose)
        print('Reading ZIPS 2011...')
        self.read_zips_batters_2011(os.path.join(base_dir, 'ZIPS Hitters 2011.csv'),
                                    verbose=verbose)
        self.read_zips_pitchers_2011(os.path.join(base_dir, 'ZIPS Pitchers 2011.csv'),
                                     verbose=verbose)
        print('Reading ZIPS 2012...')
        self.read_zips_batters_2012(os.path.join(base_dir, 'ZIPS Hitters 2012.csv'),
                                    verbose=verbose)
        self.read_zips_pitchers_2012(os.path.join(base_dir, 'ZIPS Pitchers 2012.csv'),
                                     verbose=verbose)
        print('Reading ZIPS 2013...')
        self.read_zips_batters_2013(os.path.join(base_dir, 'ZIPS Hitters 2013.csv'),
                                    verbose=verbose)
        self.read_zips_pitchers_2013(os.path.join(base_dir, 'ZIPS Pitchers 2013.csv'),
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
                      '', 'birthdate', 'w', 'l', 'sv', '', '', 'ip', 'h', 
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
                      'team', '', '', '', 'w', 'l', '', 'sv', '', '', 'ip', 
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
                      '', '', '', '', '', '', '', '', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2013, 
                                 is_actual=False,
                                 player_type='batter',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
                                 verbose=verbose)

    def read_pecota_pitchers_2013(self, filename, verbose=False):

        header_row = ['bp_id', 'last_name', 'first_name', '', '', '', '', '', 
                      'team', '', '', '', 'w', 'l', '', 'sv', '', '', 'ip', 
                      'h', 'hr', 'bb', 'k', '', '', '', '', 'whip', 'era', '', 
                      '', '', '', '', '', '', '', '', '', 'mlb_id']
        self.read_projection_csv(filename, 'pecota', 2013,
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
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
                      '', '', '', 'w', 'l', 'era', '', '', 'ip', 'h', 'r', 
                      'er', 'hr', 'bb', 'k', 'wp', '', 'hbp']
        self.read_projection_csv(filename, 'zips', 2011, 
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
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
                      '', '', 'ip', 'h', 'r', 'er', 'hr', 'bb', 'k', 'wp', '', 
                      'hbp']
        self.read_projection_csv(filename, 'zips', 2012, 
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
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
                      '', '', 'ip', 'h', 'r', 'er', 'hr', 'bb', 'k', 'wp', '', 
                      'hbp']
        self.read_projection_csv(filename, 'zips', 2013, 
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.batter_post_processor,
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
                      'ip', '', '', '', '', '', '', 'k', 'bb', 'hbp', '', 'hr',
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
                      '', '', '', 'ip', '', '', '', '', '', '', '',  'k', 'bb', 
                      'hbp', 'h', '', 'hr', '', '', '', '', 'era', '', '', 
                      'er', 'whip', 'w', 'l', 'sv']
        self.read_projection_csv(filename, 'steamer', 2012, 
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=helper.pitcher_post_processor,
                                 verbose=verbose)

    def read_steamer_batters_2013(self, filename, verbose=False):

        header_row = ['steamer_id', 'mlb_id', 'first_name', 'last_name', '', 
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

        header_row = ['steamer_id', 'mlb_id', 'first_name', 'last_name', 'ip',
                      '', '', '', 'sv', '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', '', '', 'era', 'ra', 'k', 'bb', 
                      'hbp', '', '', '', 'h', 'er', 'r', 'whip', 'w', 'l']
        self.read_projection_csv(filename, 'steamer', 2013, 
                                 is_actual=False,
                                 player_type='pitcher',
                                 header_row=header_row, 
                                 post_processor=steamer2013_post_processor,
                                 verbose=verbose)

def steamer2013_post_processor(x):
    '''
    Post-processor specially for Steamer 2013, which weirdly includes only an
    HR/9 field but not an HR field
    '''
    try: x['hr'] = float(x['hr9']) / 9.0 * float(x['ip'])
    except: pass
    return helper.pitcher_post_processor(x)