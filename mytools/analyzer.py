import pandas as pd

sample_df = [
        (1, 'test1', 13.1, 13.1, 7.2, 3, 0, 0, '2021-04-29'),
        (2, 'test1', 75.5, 75.5, 7.5, 2, 0, 0, '2021-04-29'),
        (3, 'test1', 70.5, 71.5, 2.5, 5, 0, 0, '2021-04-30')
    ]

mydataDf = pd.DataFrame(sample_df,
                        columns=[
                            'id',
                            'username',
                            'operationTime',
                            'totalWorkingTime',
                            'longestOpenedTime',
                            'blinkCount',
                            'warningCount',
                            'alertCount',
                            'create_date'
                        ])

df_a = mydataDf.drop(['id', 'username'], axis=1)

print(df_a.info())

df_a_grouped = df_a.groupby(df_a['create_date'])

print(df_a_grouped.sum())
