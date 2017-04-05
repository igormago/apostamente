from apostamente.config.settings import PATH_PREDICTIONS, PATH_DATAFRAMES
from apostamente.core import features as f
import pandas as pd
from apostamente.dataset.betexplorer.models import Championship
from apostamente.config.logger import logger


def predict_by_all_past_matches(prediction_id, task_id, df, features, clf):

    logger.info('predict_by_all_past_matches: ' + prediction_id + str(task_id))
    #pd.options.mode.chained_assignment = None
    path = PATH_PREDICTIONS + prediction_id + '.csv'
    df_prediction = pd.read_csv(path)

    df.index = df['m_match_id']

    task_id = f.get('pred',str(task_id))

    df_prediction.index = df_prediction.m_match_id

    df_prediction[task_id] = ""
    df_prediction[f.get(task_id,f.YES)] = ""
    df_prediction[f.get(task_id,f.NO)] = ""
    previous_champ = None
    previous_matches = pd.DataFrame()

    for c in Championship.list():

        matches = df[(df.m_championship_id == c.id)]

        if (previous_champ != None and previous_champ != c.name):
            previous_matches = pd.DataFrame()

        if (len(matches) > 11):

            rd_max = matches['m_match_group_num'].max()
            rd_min = matches['m_match_group_num'].min()

            for mid in range(rd_min + 1, rd_max + 1):

                train = matches[matches.m_match_group_num < mid]
                train = train.append(previous_matches)

                if (len(train) < 10):
                    continue
                test = matches[matches.m_match_group_num == mid]

                target = 'm_bts_result'
                X = train[features]
                y = train[target]
                Z = test[features]

                clf.fit(X, y)

                predictions = clf.predict(Z)
                writePredict(df_prediction, task_id, test, predictions)
                probabilities = clf.predict_proba(Z)
                writeProbabilites(df_prediction, task_id, Z, predictions, probabilities)

        previous_matches = previous_matches.append(matches)
        previous_champ = c.name

    df_prediction.to_csv(PATH_PREDICTIONS + prediction_id + '.csv', index=False)
    logger.info('predict_by_all_past_matches: end')

def writePredict(df, idJob, test, predictions):
    for i, pred in zip(test.index, predictions):
        df.set_value(i, idJob, pred)


def writeProbabilites(df, index, test, predictions, probabilities):
    for i, pred, prob in zip(test.index, predictions, probabilities):

        if (len(prob) == 1):
            if (pred == 0):
                prob = [1, 0]
            else:
                prob = [0, 1]

        for idx, cla in enumerate(['no', 'yes']):
            p = index + '_' + cla
            df.set_value(i, p, round(prob[idx], 2))