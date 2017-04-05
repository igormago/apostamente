MATCH = 'm'
CHAMPIONSHIP = 'c'
STATS_HOME = 'h'
STATS_AWAY = 'a'

RESULT_BTS = 'bts_result'
RESULT_HDA = 'hda_result'

ODDS_MLI = 'mli'
ODDS_BTS = 'bts'

COLUMN = 'col'
RESULT = 'result'

FAVORITE = 'fav'
MEDIUM = 'med'
UNDERDOG = 'und'

HOME = 'home'
DRAW = 'draw'
AWAY = 'away'

YES = 'yes'
NO = 'no'

GOALS = 'goals'

LIST_STATS_TAB = ['matches_played', 'wins', 'draws', 'loses', 'goals_for', 'goals_against', 'points']
LIST_STATS_BTS = ['bts_yes', 'bts_no']
LIST_STATS = LIST_STATS_TAB + LIST_STATS_BTS

LIST_TEAMS = ['h', 'a']
LIST_LOCALES = ['home', 'away', None]
LIST_ODD_LIMITS = ['max', 'min', 'avg']
LIST_HDA = ['home', 'draw', 'away']
LIST_FMU = ['fav', 'med', 'und']
LIST_FU = ['fav', 'und']
LIST_YN = ['yes', 'no']

MATCHES_PLAYED = 'matches_played'
STATS = 'stats'
TABLE = 'tab'
HDA = 'hda'
FMU = 'fmu'
FU = 'fu'
YN = 'yn'

ODDS = 'o'
MEAN = 'm'
PROB = 'p'


def get(*params):
    if (len(params) <= 1):
        return None
    else:
        r = params[0]
        for p in params[1:]:
            r = r + "_" + p
    return r


TEAMS = 'team_id'
STATS_TAB = get(STATS, TABLE)
STATS_TAB_MEAN = get(STATS, TABLE, MEAN)
STATS_BTS = get(STATS, ODDS_BTS)
STATS_BTS_MEAN = get(STATS, ODDS_BTS, MEAN)
MLI_HDA_ODDS = get(ODDS_MLI, HDA, ODDS)
MLI_HDA_PROB = get(ODDS_MLI, HDA, PROB)
MLI_FMU_ODDS = get(ODDS_MLI, FMU, ODDS)
MLI_FMU_PROB = get(ODDS_MLI, FMU, PROB)
MLI_FMU_COLUMN = get(ODDS_MLI, FMU, COLUMN)
BTS_YN_ODDS = get(ODDS_BTS, YN, ODDS)
BTS_YN_PROB = get(ODDS_BTS, YN, PROB)
BTS_FU_ODDS = get(ODDS_BTS, YN, ODDS)
BTS_FU_PROB = get(ODDS_BTS, YN, PROB)
BTS_FU_COLUMN = get(ODDS_BTS, YN, COLUMN)


def add_stats_mean(features, transform=False):
    for t in LIST_TEAMS:
        for s in LIST_STATS_TAB:
            for l in LIST_LOCALES:
                if (l == None):
                    feature = get(t, s)
                else:
                    feature = get(t, s, l)

                if (transform and s != 'matches_played'):
                    feature = get(feature, MEAN)
                features.append(feature)


def add_ml_odds_hda(features, transform=False):
    for i in LIST_HDA:

        for oc in LIST_ODD_LIMITS:
            ft = get(ODDS_MLI, i, oc)

            if (transform and oc != 'std_dev'):
                ft = get(ft, PROB)

            features.append(ft)


def add_ml_odds_fmu(features, transform=False):
    for i in LIST_FMU:

        for oc in LIST_ODD_LIMITS:
            ft = get(ODDS_MLI, i, oc)

            if (transform and oc != 'std_dev'):
                ft = get(ft, PROB)
            features.append(ft)


def add_bts_stats(features, transform=False):
    for t in LIST_TEAMS:
        for s in LIST_STATS_BTS:
            for l in LIST_LOCALES:
                if (l == None):
                    feature = get(t, s)
                else:
                    feature = get(t, s, l)

                if (transform):
                    feature = get(feature, MEAN)
                features.append(feature)


def add_bts_odds(features, transform=False):
    for i in LIST_YN:

        for oc in LIST_ODD_LIMITS:
            feature = get(ODDS_BTS, i, oc)

            if (transform and oc != 'std'):
                feature = get(feature, PROB)
            features.append(feature)


def add_team_id(features):
    features.append("m_home_team_id")
    features.append("m_away_team_id")


def get_list(**options):
    features = []

    if (options.get(TEAMS)):
        add_team_id(features)

    if (options.get(STATS_TAB)):
        add_stats_mean(features)

    if (options.get(STATS_TAB_MEAN)):
        add_stats_mean(features, transform=True)

    if (options.get(STATS_BTS)):
        add_bts_stats(features)

    if (options.get(STATS_BTS_MEAN)):
        add_bts_stats(features, transform=True)

    if (options.get(MLI_HDA_ODDS)):
        add_ml_odds_hda(features)

    if (options.get(MLI_HDA_PROB)):
        add_ml_odds_hda(features, transform=True)

    if (options.get(MLI_FMU_ODDS)):
        add_ml_odds_fmu(features)

    if (options.get(MLI_FMU_PROB)):
        add_ml_odds_fmu(features, transform=True)

    if (options.get(BTS_YN_ODDS)):
        add_bts_odds(features)

    if (options.get(BTS_YN_PROB)):
        add_bts_odds(features, transform=True)

    return features


def get_groups():
    return [TEAMS, STATS_TAB, STATS_TAB_MEAN, STATS_BTS, STATS_BTS_MEAN, \
            MLI_HDA_ODDS, MLI_HDA_PROB, MLI_FMU_ODDS, MLI_FMU_PROB, MLI_FMU_COLUMN,
            BTS_YN_ODDS, BTS_YN_PROB, BTS_FU_ODDS, BTS_FU_PROB, BTS_FU_COLUMN]

