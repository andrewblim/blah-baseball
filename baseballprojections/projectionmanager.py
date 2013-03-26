from helper import getSQLAlchemyFields
from schema import *
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
import csv
import datetime
import inspect
import itertools

Session = sessionmaker()

class ProjectionManager(object):

    def __init__(self, dburl='sqlite://'):
        
        self.engine = create_engine(dburl)
        Session.configure(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def add_or_update_player(self, player_type, overwrite=False, 
                             **kwargs):
        """
        Add a player to the database. If a player is already found with 
        matching ids, populate any missing fields (overwrite=False) or 
        overwrite whatever values they might have (overwrite=True). 

        If no id fields are supplied but last_name and first_name (and 
        optionally birthdate) are supplied, tries to match on that. Not ideal
        due to nicknames, name changes, players with identical names, etc. In
        this case this function will _not_ try to create a new player, but 
        will raise an exception if no players are found. 
        """

        if player_type == 'batter':
            player_class = Batter
        elif player_type == 'pitcher':
            player_class = Pitcher
        else:
            raise Exception('Error: add_or_update_player must be called with '\
                            'player_type = either "batter" or "pitcher"')

        matches = []
        id_clauses = [ (getattr(player_class, k) == kwargs[k])
                       for k in Player.id_fields() 
                       if (k in kwargs and kwargs[k] != '') ]
        name_clauses = [ (getattr(player_class, k) == kwargs[k])
                         for k in Player.name_fields()
                         if (k in kwargs and kwargs[k] != '') ]
        
        criteria = {}
        if len(id_clauses) > 0:
            matches = self.query(player_class).filter(or_(*id_clauses)).all()
            names_only = False
        elif len(name_clauses) > 0:
            matches = self.query(player_class).filter(and_(*name_clauses)).all()
            names_only = True
        else:
            raise Exception('Error: add_or_update_player must be called with '\
                            'at least one id parameter or both last_name and '\
                            'first_name parameters')

        if len(matches) > 1:
            raise Exception('Error: multiple matches found: %s' % matches)
        elif len(matches) == 1:
            match = matches[0]
            for field, value in kwargs.iteritems():
                if overwrite or getattr(match, field) is None or getattr(match, field) == '':
                    setattr(match, field, value)
        else:
            if names_only:
                raise Exception('Error: could not find player matching '\
                                'criteria %s' % kwargs)
            else:
                match = player_class(**kwargs)
                self.session.add(match)

        self.session.commit()
        return match

    def add_or_update_projection_system(self, name, year, is_actual):
        """
        Add a projection system to the database. 
        """
        projection_system = self.query(ProjectionSystem).\
                                 filter(ProjectionSystem.name == name).\
                                 filter(ProjectionSystem.year == year).\
                                 first()
        if projection_system is None:
            projection_system = ProjectionSystem(name=name, year=year, 
                                                 is_actual=is_actual)
            self.session.add(projection_system)
            self.session.commit()
        return projection_system

    def add_batter_projection(self, **kwargs):
        """
        Add a projection for an individual batter to the database. 
        """
        projection = BatterProjection(**kwargs)
        self.session.add(projection)
        self.session.commit()
        return projection

    def add_pitcher_projection(self, **kwargs):
        """
        Add a projection for an individual pitcher to the database. 
        """
        projection = PitcherProjection(**kwargs)
        self.session.add(projection)
        self.session.commit()
        return projection

    def read_projection_csv(self, filename, projection_name, year, is_actual,
                            player_type, header_row, post_processor=None, 
                            skip_rows=1, verbose=False):

        if player_type not in ('batter', 'pitcher'):
            raise Exception('player_type is %s, must be either '\
                            '"batter" or "pitcher"' % player_type)

        projection_system = self.add_or_update_projection_system('%s' % projection_name, 
                                                                 year, 
                                                                 is_actual)
        reader = csv.reader(open(filename, 'r'))
        for i in range(skip_rows):
            reader.next()
        n = len(header_row)

        add_batter_args = getSQLAlchemyFields(Batter)
        add_pitcher_args = getSQLAlchemyFields(Pitcher)
        add_batter_projection_args = getSQLAlchemyFields(BatterProjection)
        add_pitcher_projection_args = getSQLAlchemyFields(PitcherProjection)

        for row in reader:

            data = dict(zip(header_row, row[:n]))
            if post_processor is not None:
                data = post_processor(data)

            if player_type == 'batter':
                player_data = { x: data[x] for x in add_batter_args if x in data }
                player_data['player_type'] = 'batter'
                try:
                    player = self.add_or_update_player(**player_data)
                    projection_data = { x: data[x] for x in add_batter_projection_args
                                        if x in data }
                    projection_data['batter_id'] = player.id
                    projection_data['projection_system_id'] = projection_system.id
                    projection = self.add_batter_projection(**projection_data)
                except Exception as e:
                    if verbose:
                        print e

            else:
                player_data = { x: data[x] for x in add_pitcher_args if x in data }
                player_data['player_type'] = 'pitcher'
                try:
                    player = self.add_or_update_player(**player_data)
                    projection_data = { x: data[x] for x in add_pitcher_projection_args
                                        if x in data }
                    projection_data['pitcher_id'] = player.id
                    projection_data['projection_system_id'] = projection_system.id
                    projection = self.add_pitcher_projection(**projection_data)
                except Exception as e:
                    if verbose:
                        print e

            if verbose:
                print('%s, %s' % (player, projection))

    # shortcuts

    def query(self, *args):
        return self.session.query(*args)

    def rollback(self):
        return self.session.rollback()

    # csv generation

    def batter_projection_groups(self, filter_clause=None):

        q = self.query(Batter, BatterProjection).\
                 join(BatterProjection).join(ProjectionSystem)
        if filter_clause is not None:
            q = q.filter(filter_clause)
        q = q.order_by(Batter.id)
        return itertools.groupby(q, lambda x: x[0])

    def pitcher_projection_groups(self, filter_clause=None):

        q = self.query(Pitcher, PitcherProjection).\
                 join(PitcherProjection).join(ProjectionSystem)
        if filter_clause is not None:
            q = q.filter(filter_clause)
        q = q.order_by(Pitcher.id)
        return itertools.groupby(q, lambda x: x[0])

    # Helper functions for the Lasso code

    def get_proj_data(self, years, player_type, stat):
        proj_data = {}
        for year in years:
            if player_type == 'batter':
                players = self.batter_projection_groups(filter_clause=ProjectionSystem.year==year)
            else:
                players = self.pitcher_projection_groups(filter_clause=ProjectionSystem.year==year)

            for player, pairs in players:
                key = str(player.mlb_id) + "_" + str(year)
                projs = [-1, -1, -1]

                for (_, projection) in pairs:
                    sys = projection.projection_system

                    if sys.name == 'pecota' :
                        projs[0] = getattr(projection,stat)
                    elif sys.name == 'zips' :
                        projs[1] = getattr(projection,stat)
                    elif sys.name == 'steamer' :
                        projs[2] = getattr(projection,stat)

                if min(projs) > 0:
                    proj_data[key] = projs
                    
        return proj_data

    def get_actual_data(self, years, player_type, stat):
        act_data = {}
        for year in years:
            if player_type == 'batter':
                players = self.batter_projection_groups(filter_clause=ProjectionSystem.year==year)
            else:
                players = self.pitcher_projection_groups(filter_clause=ProjectionSystem.year==year)

            for player, pairs in players:
                key = str(player.mlb_id) + "_" + str(year)
                act = -1

                for (_, projection) in pairs:
                    sys = projection.projection_system

                    if sys.is_actual:
                        act = getattr(projection,stat)

                if act > 0:
                    act_data[key] = act
                    
        return act_data

    def cross_projection_csv(self, csvfile, player_type, stats, 
                             filter_clause=None, verbose=False):

        if player_type == 'batter':
            player_class = Batter
        elif player_type == 'pitcher':
            player_class = Pitcher
        else:
            raise Exception('Error: cross_projection_csv must be called with '\
                            'player_type = either "batter" or "pitcher"')

        systems = self.query(ProjectionSystem).\
                       order_by(ProjectionSystem.name, ProjectionSystem.year)
        statcols = itertools.product(stats, systems)
        statcols = ["%s_%d_%s" % (system.name, system.year, stat)
                    for stat, system in statcols]
        cols = ['last_name', 'first_name', 'mlb_id']
        cols.extend(statcols)

        if player_type == 'batter':
            players = self.batter_projection_groups(filter_clause=filter_clause)
        else:
            players = self.pitcher_projection_groups(filter_clause=filter_clause)

        with open(csvfile, 'w') as f:
            writer = csv.DictWriter(f, cols)
            writer.writeheader()
            for player, pairs in players:
                if verbose: print player
                row = { 'last_name': player.last_name,
                        'first_name': player.first_name,
                        'mlb_id': player.mlb_id }
                for (_, projection) in pairs:
                    system = projection.projection_system
                    for stat in stats:
                        col = "%s_%d_%s" % (system.name, system.year, stat)
                        row[col] = getattr(projection, stat)
                writer.writerow(row)