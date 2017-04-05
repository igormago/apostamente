from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import or_
from sqlalchemy.sql.expression import distinct

from apostamente.config.database import Base
from apostamente.config.database import sessionExplorer as session


class ModelMixin(object):

    def save(self):
        session.add(self)

    @classmethod
    def list(cls):
        return session.query(cls).filter().all()

    def __init__(self,*args,**kwargs):
        pass


class Championship(Base ,ModelMixin):

    __tablename__ = 'championships'

    id = Column("championship_id" ,Integer, primary_key=True, autoincrement=True)
    name = Column("championship_name" ,String(100))
    year = Column(Integer)

    def __repr__(self):
        r = "Championship: ", self.id, self.name, self.year
        return (str(r))

    @staticmethod
    def get (championship_name, year):
        return session.query(Championship).filter(Championship.name == championship_name,
                                                  Championship.year == year).one()

    @staticmethod
    def get_by_id (champId):
        return session.query(Championship).filter(Championship.id == champId).one()

    @staticmethod
    def list_by_name (championship_name):
        return session.query(Championship).filter(Championship.name == championship_name).all()

    def list_matches (self):
        return session.query(Match).filter(Match.championshipId == self.id).order_by(Match.matchDate).all()

    def get_file_name(self):
        return self.name + "-" + str(self.year) + ".html"

    def list_teams(self):
        return session.query(Team).filter(or_(Match.away_team_id == Team.id, Match.homeTeamId == Team.id), \
                                          Match.championship_id == self.id).distinct().all()

    def list_tables(self):
        return session.query(Table).filter(Table.championship_id == self.id,
                                           Table.last_matches_num == Table.matches_played,
                                           Table.next_match_id == Match.id).order_by(Match.matchGroupNum).all()
    @staticmethod
    def list_names():
        return session.query(distinct(Championship.name)).all()


class Team(Base, ModelMixin):
    __tablename__ = 'teams'

    id = Column('team_id', Integer, primary_key=True, autoincrement=True)
    name = Column('team_name', String(45))

    def __repr__(self):
        r = "Team: ", self.id, self.name
        return (str(r))

    def get(self, teamName):
        return session.query(Team).filter(Team.name == teamName).one()

    def get_by_id(self, teamId):
        return session.query(Team).filter(Team.id == teamId).one()

    def list_matches(self, championship_id):
        return session.query(Match).filter(or_(Match.away_team_id == self.id, Match.home_team_id == self.id), \
                                           Match.championship_id == championship_id).order_by(Match.match_date).all()


class Match(Base, ModelMixin):

    __tablename__ = 'matches'

    RESULT_HOME_WINNER = 'H'
    RESULT_DRAW = 'D'
    RESULT_AWAY_WINNER = 'A'

    id = Column("match_id", String(45), primary_key=True)
    championship_id = Column("championship_id", Integer, ForeignKey('championships.championship_id'))
    home_team_id = Column (Integer, ForeignKey('teams.team_id'))
    away_team_id = Column(Integer, ForeignKey('teams.team_id'))
    goals_home = Column(Integer)
    goals_away = Column(Integer)
    column_result = Column(String(1))
    match_date = Column(Date)
    round_num = Column(Integer)
    odd_home = Column( Numeric)
    odd_draw = Column(Numeric)
    odd_away = Column( Numeric)
    match_num = Column (Integer)
    match_group_num = Column(Integer)

    championship = relationship("Championship")

    def __repr__(self):
        return "ID: " + self.id + ": " + str(self.homeTeamId) + \
               "(" + str(self.goalsHome) + ") x (" + str(self.goalsAway) + ")" + str(self.awayTeamId)

    @staticmethod
    def get(match_id):
        return session.query(Match).filter(Match.id == match_id).one()

    def get_file_name(self, oddType):
        return self.id + "_" + oddType + ".html"

    @staticmethod
    def list():
        return session.query(Match).filter().all()


class Table(Base, ModelMixin):
    LOCAL_HOME = 'H'
    LOCAL_AWAY = 'A'

    __tablename__ = 'round_tables'
    championship_id = Column("championship_id", Integer, ForeignKey('championships.championship_id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'), primary_key=True)
    matches_played = Column( Integer, primary_key=True)
    last_matches_num = Column(Integer, primary_key=True)
    wins = Column(Integer)
    draws = Column(Integer)
    loses = Column(Integer)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    points = Column(Integer)
    matches_played_home = Column(Integer)
    wins_home = Column(Integer)
    draws_home = Column(Integer)
    loses_home = Column(Integer)
    goals_for_home = Column(Integer)
    goals_against_home = Column(Integer)
    points_home = Column(Integer)
    matches_played_away = Column(Integer)
    wins_away = Column(String)
    draws_away = Column(Integer)
    loses_away = Column(Integer)
    goals_for_away = Column(Integer)
    goals_against_away = Column(Integer)
    points_away = Column(Integer)
    last_match_local = Column(String(1))
    next_match_id = Column(String(45), ForeignKey('matches.match_id'))
    bts_yes = Column (Integer)
    bts_no = Column (Integer)
    bts_yes_home = Column(Integer)
    bts_no_home = Column(Integer)
    bts_yes_away = Column(Integer)
    bts_no_away = Column(Integer)

    @classmethod
    def fromData(cls, champ_id, team_id, last_match_local, \
                 matches_played, wins, draws, loses, goals_for, goals_against, points, \
                 matches_played_home, wins_home, draws_home, loses_home, goals_for_home, goals_against_home, points_home, \
                 matches_played_away, wins_away, draws_away, loses_away, goals_for_away, goals_against_away, points_away
                 ):
        cls.championship_id = champ_id
        cls.team_id = team_id
        cls.last_match_local = last_match_local
        cls.last_matches_num = matches_played

        cls.matches_played = matches_played
        cls.wins = wins
        cls.draws = draws
        cls.loses = loses
        cls.goals_for = goals_for
        cls.goals_against = goals_against
        cls.points = points

        cls.matches_played_home = matches_played_home
        cls.wins_home = wins_home
        cls.draws_home = draws_home
        cls.loses_home = loses_home
        cls.goals_for_home = goals_for_home
        cls.goals_against_home = goals_against_home
        cls.points_home = points_home

        cls.matches_played_away = matches_played_away
        cls.wins_away = wins_away
        cls.draws_away = draws_away
        cls.loses_away = loses_away
        cls.goals_for_away = goals_for_away
        cls.goals_against_away = goals_against_away
        cls.points_away = points_away

        return cls

    @staticmethod
    def get_by_match(match_id):
        return session.query(Table).filter(Table.next_match_id == match_id).all()


class ResumeOddsMLI(Base, ModelMixin):
    __tablename__ = 'resume_odds_mli'

    match_id = Column(String(45), ForeignKey('matches.match_id'), primary_key=True)
    home_avg = Column(Numeric)
    draw_avg = Column(Numeric)
    away_avg = Column(Numeric)
    home_max = Column(Numeric)
    draw_max = Column(Numeric)
    away_max = Column(Numeric)
    home_min = Column(Numeric)
    draw_min = Column(Numeric)
    away_min = Column(Numeric)
    home_std = Column(Numeric)
    draw_std = Column(Numeric)
    away_std = Column(Numeric)
    odds_num = Column(Integer)

    @staticmethod
    def get(match_id):
        return session.query(ResumeOddsMLI).filter(ResumeOddsMLI.match_id == match_id).one()

    @staticmethod
    def list():
        return session.query(ResumeOddsMLI).filter().all()


class ResumeOddsBTS(Base, ModelMixin):
    __tablename__ = 'resume_odds_bts'

    match_id = Column("match_id", String(45), ForeignKey('matches.match_id'), primary_key=True)
    yes_avg = Column(Numeric)
    no_avg = Column(Numeric)
    yes_max = Column(Numeric)
    no_max = Column(Numeric)
    yes_min = Column(Numeric)
    no_min = Column(Numeric)
    yes_std = Column(Numeric)
    no_std = Column(Numeric)

    odds_num = Column("odds_num", Integer)

    def get(self, match_id):
        return session.query(ResumeOddsBTS).filter(ResumeOddsBTS.match_id == match_id).one()

    def list(self):
        return session.query(ResumeOddsBTS).filter().all()
