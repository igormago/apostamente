from apostamente.config.settings import PATH_PREDICTIONS
import pandas as pd

df = pd.read_csv(PATH_PREDICTIONS + 'GaussianNB_kbest_chi2.csv')

def accuracy (df, pred):

    res = 'm_bts_result'
    #book = 'bts_fav_avg_col'

    p1 = df[(df[pred] == 1)]
    p0 = df[(df[pred] == 0)]

    p0_r1 = p0[p0[res] == 1]
    p0_r0 = p0[p0[res] == 0]
    p1_r0 = p1[p1[res] == 0]
    p1_r1 = p1[p1[res] == 1]

    c01 = len(p0_r1)
    c00 = len(p0_r0)
    c10 = len(p1_r0)
    c11 = len(p1_r1)

    cp1 = c10 + c11
    cp0 = c01 + c00

    resume = pd.DataFrame()
    resume['result'] = ['Yes' ,'No']
    resume['pred_yes'] = [c11, c10]
    resume['pred_no'] = [c01, c00]

    cr1 = c01 + c11
    cr0 = c10 + c00

    resume['p_yes'] = [ c11 /cr1, c10/ cr0]
    resume['p_no'] = [c01 / cr1, c00 / cr0]

    ACC = round((c11 + c00) / (cr1 + cr0) * 100, 2)
    PPV = round(c11 / cp1 * 100, 2)
    NPV = round(c00 / cp0 * 100, 2)

    pl_11 = p1_r1['bts_yes_avg'].sum()
    pl_00 = p0_r0['bts_no_avg'].sum()

    pl_total = pl_11 + pl_00 - cp1 - cp0
    #     print('Pl TOTAL: ',cp1+cp0, pl_11+pl_00- cp1-cp0)
    #     print('Pl YES: ', pl_11-cp1)
    #     print('Pl NO: ', pl_00-cp0)

    print(ACC, PPV, NPV, pl_total)


for x in range(1, 20):
    print('-------------- ', x)
    accuracy(df, 'pred_' + str(x))

print("---------")
accuracy(df, 'bts_fav_avg_col')