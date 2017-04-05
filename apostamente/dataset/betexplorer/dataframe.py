import pandas as pd
from apostamente.config.database import sessionExplorer as session
from apostamente.config.settings import PATH_DATAFRAMES
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import or_

from apostamente.config import logger
from apostamente.core import features as f
from apostamente.dataset.betexplorer.models import Match, Championship, Table, ResumeOddsMLI, ResumeOddsBTS


def add_stats_mean(df):
    for t in f.LIST_TEAMS:
        for s in f.LIST_STATS:
            df[f.get(t, s, f.MEAN)] = df[f.get(t, s)].divide(df[f.get(t, f.MATCHES_PLAYED)])
            df[f.get(t, s, f.HOME, f.MEAN)] = df[f.get(t, s, f.HOME)] / df[f.get(t, f.MATCHES_PLAYED, f.HOME)]
            df[f.get(t, s, f.AWAY, f.MEAN)] = df[f.get(t, s, f.AWAY)] / df[f.get(t, f.MATCHES_PLAYED, f.AWAY)]

            df[f.get(t, s, f.MEAN)].fillna(0, inplace=True)
            df[f.get(t, s, f.HOME, f.MEAN)].fillna(0, inplace=True)
            df[f.get(t, s, f.AWAY, f.MEAN)].fillna(0, inplace=True)


def add_mli_fmu(df):
    for t in f.LIST_ODD_LIMITS:
        home = f.get(f.ODDS_MLI, f.HOME, t)
        draw = f.get(f.ODDS_MLI, f.DRAW, t)
        away = f.get(f.ODDS_MLI, f.AWAY, t)

        fav = f.get(f.ODDS_MLI, f.FAVORITE, t)
        med = f.get(f.ODDS_MLI, f.MEDIUM, t)
        und = f.get(f.ODDS_MLI, f.UNDERDOG, t)

        df[fav] = df.apply(lambda row:
                           evaluate_favorite(row[home], row[draw], row[away], return_odd=True), axis=1)
        df[med] = df.apply(lambda row:
                           evaluate_medium(row[home], row[draw], row[away], return_odd=True), axis=1)
        df[und] = df.apply(lambda row:
                           evaluate_underdog(row[home], row[draw], row[away], return_odd=True), axis=1)

        fav = f.get(f.ODDS_MLI, f.FAVORITE, t, f.COLUMN)
        med = f.get(f.ODDS_MLI, f.MEDIUM, t, f.COLUMN)
        und = f.get(f.ODDS_MLI, f.UNDERDOG, t, f.COLUMN)

        df[fav] = df.apply(lambda row:
                           evaluate_favorite(row[home], row[draw], row[away]), axis=1)
        df[med] = df.apply(lambda row:
                           evaluate_medium(row[home], row[draw], row[away]), axis=1)
        df[und] = df.apply(lambda row:
                           evaluate_underdog(row[home], row[draw], row[away]), axis=1)


def add_mli_prob(df):
    for opt in f.LIST_ODD_LIMITS:

        for i in f.LIST_HDA:
            feature = f.get(f.ODDS_MLI, i, opt)
            df[f.get(feature, f.PROB)] = 1 / df[feature]

        for i in f.LIST_FMU:
            feature = f.get(f.ODDS_MLI, i, opt)
            df[f.get(feature, f.PROB)] = 1 / df[feature]


def add_bts_prob(df):
    for opt in f.LIST_ODD_LIMITS:

        for i in f.LIST_YN:
            feature = f.get(f.ODDS_BTS, i, opt)
            df[f.get(feature, f.PROB)] = 1 / df[feature]

        for i in f.LIST_FU:
            feature = f.get(f.ODDS_BTS, i, opt)
            df[f.get(feature, f.PROB)] = 1 / df[feature]


def add_bts_fu(df):
    for t in f.LIST_ODD_LIMITS:
        yes = f.get(f.ODDS_BTS, f.YES, t)
        no = f.get(f.ODDS_BTS, f.NO, t)

        fav = f.get(f.ODDS_BTS, f.FAVORITE, t)
        und = f.get(f.ODDS_BTS, f.UNDERDOG, t)

        df[fav] = df.apply(lambda row:
                           evaluate_bts(row[yes], row[no], return_odd=True), axis=1)

        df[und] = df.apply(lambda row:
                           evaluate_bts(row[yes], row[no], return_odd=True, return_favorite=False), axis=1)

        fav = f.get(f.ODDS_BTS, f.FAVORITE, t, f.COLUMN)
        und = f.get(f.ODDS_BTS, f.UNDERDOG, t, f.COLUMN)

        df[fav] = df.apply(lambda row:
                           evaluate_bts(row[yes], row[no]), axis=1)

        df[und] = df.apply(lambda row:
                           evaluate_bts(row[yes], row[no], return_favorite=False), axis=1)


def add_results(df):
    df[f.get(f.MATCH, f.RESULT_BTS)] = df.apply(evaluate_result_bts, axis=1)
    df[f.get(f.MATCH, f.RESULT_HDA)] = df.apply(evaluate_result_bts, axis=1)


def evaluate_result_hda(row, odd_limit=None):
    goals_home = row[f.get(f.MATCH, f.GOALS, f.HOME)]
    goals_away = row[f.get(f.MATCH, f.GOALS, f.AWAY)]

    if (goals_home > goals_away):
        return 1
    elif (goals_home < goals_away):
        return 2
    return 0


def evaluate_result_bts(row, odd_limit=None):
    goals_home = row[f.get(f.MATCH, f.GOALS, f.HOME)]
    goals_away = row[f.get(f.MATCH, f.GOALS, f.AWAY)]

    if (goals_home > 0 and goals_away > 0):
        return 1
    return 0


def evaluate_favorite(odd_home, odd_draw, odd_away, return_odd=False):
    if (odd_home <= odd_draw and odd_home <= odd_away):

        if (return_odd):
            return odd_home
        return 1;

    elif (odd_draw <= odd_away):

        if (return_odd):
            return odd_draw
        return 0;

    if (return_odd):
        return odd_away

    return 2;


def evaluate_medium(odd_home, odd_draw, odd_away, return_odd=False):
    if (odd_home <= odd_draw):

        if (odd_draw <= odd_away):

            if (return_odd):
                return odd_draw
            return 0
        elif (odd_home <= odd_away):

            if (return_odd):
                return odd_away
            return 2
        else:
            if (return_odd):
                return odd_home
            return 1

    elif (odd_home > odd_draw):

        if (odd_draw > odd_draw):
            if (return_odd):
                return odd_draw
            return 0
        elif (odd_home > odd_away):
            if (return_odd):
                return odd_away
            return 2
        else:
            if (return_odd):
                return odd_home
            return 1


def evaluate_underdog(odd_home, odd_draw, odd_away, return_odd=False):
    if (odd_home > odd_draw and odd_home > odd_away):
        if (return_odd):
            return odd_home
        return 1
    elif (odd_away >= odd_draw):
        if (return_odd):
            return odd_away
        return 2
    if (return_odd):
        return odd_draw
    return 0


def evaluate_bts(odd_yes, odd_no, return_favorite=True, return_odd=False):
    if (odd_yes <= odd_no):
        if (return_favorite):
            if (return_odd):
                return odd_yes
            return 1
        else:
            if (return_odd):
                return odd_no
            return 0
    else:
        if (return_favorite):
            if (return_odd):
                return odd_no
            return 0
        else:
            if (return_odd):
                return odd_yes
            return 1


def create_dataframe_with_stats():

    logger.info("begin - create_dataframe_with_stats")

    TMatch = aliased(Match, name=f.MATCH)
    TChamp = aliased(Championship, name=f.CHAMPIONSHIP)
    THome = aliased(Table, name=f.STATS_HOME)
    TAway = aliased(Table, name=f.STATS_AWAY)

    results = session.query(TChamp, TMatch, THome, TAway).filter(
        TChamp.id == TMatch.championship_id,
        TMatch.home_team_id == THome.team_id, TMatch.away_team_id == TAway.team_id,
        TMatch.id == THome.next_match_id, TMatch.id == TAway.next_match_id,
        THome.matches_played == THome.last_matches_num,
        TAway.matches_played == TAway.last_matches_num).order_by(TMatch.championship_id, TMatch.match_date)

    # with_labels() beacause exists ambiguous columns name.
    df = pd.read_sql(results.with_labels().statement, session.bind)

    add_stats_mean(df)
    add_results(df)

    df.to_csv(PATH_DATAFRAMES + 'bts_stats.csv', index=False);

    logger.info("end - create_dataframe_with_stats")


def create_dataframe_with_odds():
    logger.info("create_dataframe_with_odds: begin")

    TMatch = aliased(Match, name=f.MATCH)
    TChamp = aliased(Championship, name=f.CHAMPIONSHIP)
    TOddsML = aliased(ResumeOddsMLI, name=f.ODDS_MLI)
    TOddsBTS = aliased(ResumeOddsBTS, name=f.ODDS_BTS)
    THome = aliased(Table, name=f.STATS_HOME)
    TAway = aliased(Table, name=f.STATS_AWAY)

    results = session.query(TChamp, TMatch, TOddsML, TOddsBTS, THome, TAway).filter(
        TChamp.id == TMatch.championship_id,
        TMatch.id == TOddsBTS.match_id,
        TMatch.home_team_id == THome.team_id, TMatch.away_team_id == TAway.team_id,
        TMatch.id == THome.next_match_id, TMatch.id == TAway.next_match_id,
        or_(THome.last_matches_num == THome.matches_played, THome.last_matches_num == None),
        or_(TAway.last_matches_num == TAway.matches_played, TAway.last_matches_num == None),
        TMatch.id == TOddsML.match_id).order_by(TMatch.championship_id, TMatch.match_date)

    # with_labels() beacause exists ambiguous columns name.
    df = pd.read_sql(results.with_labels().statement, session.bind)

    add_stats_mean(df)

    add_mli_fmu(df)
    add_mli_prob(df)

    add_bts_fu(df)
    add_bts_prob(df)

    add_results(df)

    df.to_csv(PATH_DATAFRAMES + 'bts_total.csv', index=False);

    # print(*df.columns,sep='\n')
    logger.info("create_dataframe_with_odds: end")