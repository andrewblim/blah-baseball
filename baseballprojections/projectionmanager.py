from baseballprojections.helper import getSQLAlchemyFields
from baseballprojections.schema import *
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
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

    def read_player_csv(self, filename, header_row, 
                        post_processor=None, 
                        skip_rows=1, 
                        commit_frequency=1000,
                        verbose=False):

        """
        Read a CSV file full of player IDs into the database. Generates Players
        but no ProjectionSystems or projections. 
        """

        reader = csv.reader(open(filename, 'r'))
        for i in range(skip_rows):
            next(reader)
        n = len(header_row)

        add_player_args = getSQLAlchemyFields(Player)

        count = 0
        for row in reader:

            player = None
            projection = None

            data = dict(zip(header_row, row[:n]))
            if post_processor is not None:
                data = post_processor(data)

            player_data = { x: data[x] for x in add_player_args if x in data }
            try:
                player = self.add_or_update_player(**player_data)
            except Exception as e:
                print(e)
                        
            if verbose and (player is not None) and (projection is not None):
                print('%s', player)

            count = count + 1
            if count % 1000 == 0:
                print('loaded %d' % count)
                self.session.commit()
                
        self.session.commit()


    def find_player(self, soft_match=False, **kwargs):

        id_clauses = [ (getattr(Player, k) == kwargs[k])
                       for k in Player.id_fields() 
                       if (k in kwargs and kwargs[k] != '' and kwargs[k] is not None) ]

        matches = []

        # first try to match just on id clauses

        if len(id_clauses) > 0:
            matches = self.query(Player).filter(or_(*id_clauses)).all()

        # if nothing, then try to match on first name/last name AND if the
        # player has an MLB ID AND a birthdate AND the birthdate is after 1974

        if soft_match and len(matches) == 0:

            name_clauses = [ (func.lower(getattr(Player, k)) == kwargs[k])
                             for k in ['last_name', 'first_name']
                             if (k in kwargs and kwargs[k] != '' and kwargs[k] is not None) ]
            if len(name_clauses) > 0:
                matches = self.query(Player).filter(and_(*name_clauses), 
                                                    Player.mlb_id != None, 
                                                    Player.birthdate != None,
                                                    func.strftime('%Y', Player.birthdate) > '1974').all()

        return matches


    def add_or_update_player(self, overwrite=False, 
                             **kwargs):
        """
        Add a player to the database. If a player is already found with 
        matching ids, populate any missing fields (overwrite=False) or 
        overwrite whatever values they might have (overwrite=True). 
        """
        
        matches = self.find_player(**kwargs)

        match = None
        if len(matches) > 1:
            raise Exception('Error: multiple matches found: %s' % matches)
        elif len(matches) == 1:
            match = matches[0]
            for field, value in kwargs.items():
                if overwrite or getattr(match, field) is None or getattr(match, field) == '':
                    setattr(match, field, value)
        else:
            match = Player(**kwargs)
            self.session.merge(match)

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
        return projection_system

    def add_batter_projection(self, **kwargs):
        """
        Add a projection for an individual batter to the database. 
        """
        projection = BatterProjection(**kwargs)
        self.session.add(projection)
        return projection

    def add_pitcher_projection(self, **kwargs):
        """
        Add a projection for an individual pitcher to the database. 
        """
        projection = PitcherProjection(**kwargs)
        self.session.add(projection)
        return projection

    def read_projection_csv(self, filename, projection_name, years, is_actual,
                            projection_type, header_row, post_processor=None, 
                            skip_rows=1, error_filename=None, verbose=False):

        if projection_type not in ('batter', 'pitcher'):
            raise Exception('projection_type is %s, must be either '\
                            '"batter" or "pitcher"' % player_type)

        # years can either be a scalar or an iterable
        # if an iterable, you will have to specify a 'year' column in the data
        # indicating what year's projection each row belongs to

        try:
            years = iter(years)
        except TypeError:
            years = iter([years])

        projection_systems = { int(year): self.add_or_update_projection_system(projection_name, year, is_actual)
                               for year in years }

        if len(projection_systems) == 0:
            raise Exception('No projection systems were created (did you specify years?)')
        elif len(projection_systems) == 1:
            year, projection_system = list(projection_systems.items())[0]
            single_projection_system = True
        else:
            single_projection_system = False
        
        reader = csv.reader(open(filename, 'r'))
        for i in range(skip_rows):
            next(reader)
        n = len(header_row)

        if error_filename is not None:
            writer = csv.writer(open(error_filename, 'w'))
            writer.writerow(header_row)

        add_player_args             = getSQLAlchemyFields(Player)
        add_batter_projection_args  = getSQLAlchemyFields(BatterProjection)
        add_pitcher_projection_args = getSQLAlchemyFields(PitcherProjection)

        count = 0

        for row in reader:

            player = None
            projection = None

            raw_data = dict(zip(header_row, row[:n]))
            if post_processor is not None:
                data = post_processor(raw_data)

            if not single_projection_system:
                try: 
                    year = int(data['year'])
                except KeyError:
                    print('Unable to get year column out of data:')
                    print(data)
                    continue
                try:
                    projection_system = projection_systems[year]
                except KeyError:
                    print('Unable to find projection system for %d, was it specified in years?' % year)
                    continue

            player_data = { x: data[x] for x in add_player_args if x in data }
            player_matches = self.find_player(soft_match=True, **player_data)

            if len(player_matches) == 1:
                player = player_matches[0]
                if projection_type == 'batter':
                    projection_data = { x: data[x] for x in add_batter_projection_args if x in data }
                    projection_data['player_id'] = player.id
                    projection_data['projection_system_id'] = projection_system.id
                    projection = self.add_batter_projection(**projection_data)
                else:
                    projection_data = { x: data[x] for x in add_pitcher_projection_args if x in data }
                    projection_data['player_id'] = player.id
                    projection_data['projection_system_id'] = projection_system.id
                    projection = self.add_pitcher_projection(**projection_data)
                if verbose and (player is not None) and (projection is not None):
                    print('%s (%d)' % (player, year))

            elif len(player_matches) > 1:
                print('Multiple players found for the following player data, nothing added')
                print(player_data)
                print()
                if error_filename is not None:
                    writer.writerow(row[:n])
            else:
                print('No players found matching the following player data, nothing added')
                print(player_data)
                print()
                if error_filename is not None:
                    writer.writerow(row[:n])

            count = count+1
            if count % 1000 == 0:
                print('loaded %d' % count)
                self.session.commit()
                
        self.session.commit()

    # shortcuts

    def query(self, *args):
        return self.session.query(*args)

    def rollback(self):
        return self.session.rollback()

    # next two generate an iterator { player: (player, projection) }

    def batter_projection_groups(self, filter_clause=None):

 #       q = self.query(Batter, BatterProjection).\
#                 join(BatterProjection).join(ProjectionSystem)
        q = self.query(Player, BatterProjection).\
                 join(BatterProjection).join(ProjectionSystem)
        if filter_clause is not None:
            q = q.filter(filter_clause)
        q = q.order_by(Player.id)
        return itertools.groupby(q, lambda x: x[0])

    def pitcher_projection_groups(self, filter_clause=None):

 #       q = self.query(Pitcher, PitcherProjection).\
#                 join(PitcherProjection).join(ProjectionSystem)
        q = self.query(Player, PitcherProjection).\
                 join(PitcherProjection).join(ProjectionSystem)
        if filter_clause is not None:
            q = q.filter(filter_clause)
        q = q.order_by(Player.id)
        return itertools.groupby(q, lambda x: x[0])

    # Helper functions for the Lasso code

    def get_player_year_data(self, years, systems, player_type, stats, 
                             stat_functions, includeMissing=False):

        proj_data = {}

        for stat in stats:
            stat_function = stat_functions[stat]
            proj_data[stat] = {}

            systems2 = list(filter(lambda s: not ((stat in ['sv','saverate']) and s=='zips'),systems))
            
            if stat_function is None:
                stat_function = lambda projection: getattr(projection, stat)

            for year in years:

                group_filter = and_(ProjectionSystem.year == year,
                                    ProjectionSystem.name.in_(systems2))
                if player_type == 'batter':
                    players = self.batter_projection_groups(group_filter)
                else:
                    players = self.pitcher_projection_groups(group_filter)

                for player, pair in players:
                    #print player, pair
                    key = str(player.fg_id) + "_" + str(year)
                    projs = { system: None for system in systems2 }

                    for (_, projection) in pair:
                        sys = projection.projection_system
                        if sys.name in projs:
                            projs[sys.name] = stat_function(projection)

                    if includeMissing or not any(map(lambda x: x is None, projs.values())):
                        #print "ADDING %s, %s: %s" % (player.last_name, player.first_name, projs)
                        proj_data[stat][key] = projs
                    #else:
                        #print "NOT ADDING %s, %s: %s" % (player.last_name, player.first_name, projs)

        return proj_data

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
                if verbose: print(player)
                row = { 'last_name': player.last_name,
                        'first_name': player.first_name,
                        'mlb_id': player.mlb_id }
                for (_, projection) in pairs:
                    system = projection.projection_system
                    for stat in stats:
                        col = "%s_%d_%s" % (system.name, system.year, stat)
                        row[col] = getattr(projection, stat)
                writer.writerow(row)
