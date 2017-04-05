from apostamente.config.logger import logger
import apostamente.core.features as ft
import pandas as pd
import apostamente.dataset.betexplorer.learning as ml
from sklearn.feature_selection import SelectKBest, chi2
from apostamente.config import settings as s
from sklearn.naive_bayes import GaussianNB


# Learning: Naive Bayes + Feature Selection (Method SelectKBest(chi2))

def nb_fs_chi2():

    logger.info('nb_fs_chi2: start')
    groups = ft.get_groups()
    params = {}

    for z in groups:
        params[z] = True

    features = ft.get_list(**params)

    for task in range(1,len(features)):

        df = pd.read_csv(s.PATH_DATAFRAMES + "bts_total.csv")
        X, y = df[features], df['m_bts_result']

        select = SelectKBest(chi2, k=task)
        select.fit_transform(X,y)

        indices = select.get_support(indices=True)

        features_selected = []
        for i in indices:
            features_selected.append(features[i])

        features_total = list(features_selected)
        features_total.extend(['c_championship_id','c_championship_name','c_year','m_match_id',
                               'm_match_group_num','m_bts_result'])

        #print(features_selected)
        new_df = df[features_selected]

        clf = GaussianNB()
        ml.predict_by_all_past_matches('GaussianNB_kbest_chi2', task, df, features_selected, clf)

    logger.info('nb_fs_chi2: end')