import apostamente.dataset.betexplorer.dataframe as df
from apostamente.config.logger import logger
from apostamente.core import features as ft
from apostamente.config import settings as s


from sklearn.feature_selection import SelectKBest, SelectFpr
from sklearn.feature_selection import chi2
from apostamente.config import settings as s
import pandas as pd

from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
import apostamente.dataset.betexplorer.experiments as exp

def main():

    logger.info('Started3')
    exp.nb_fs_chi2()
    logger.info('Finished')


if __name__ == '__main__':
    main()