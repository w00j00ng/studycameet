import pandas as pd
import matplotlib.pyplot as plt

sample_df = [
        (88.6, 88.6, 95.2, 3, 0, 0, '2021-04-29'),
        (70.5, 71.5, 94.5, 5, 0, 0, '2021-04-30')
    ]

mydataDf = pd.DataFrame(sample_df,
                        columns=[
                            'operationTime',
                            'totalWorkingTime',
                            'percentage',
                            'blinkCount',
                            'warningCount',
                            'alertCount',
                            'create_date'
                        ])

print(mydataDf.info())

print(mydataDf)

# plt.plot(mydataDf['create_date'], mydataDf['percentage'])
plt.plot(mydataDf['create_date'], mydataDf['warningCount'])
plt.plot(mydataDf['create_date'], mydataDf['alertCount'])

plt.show()
