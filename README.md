# TianChi-Quarterly-Revenue-Forecast
This project is to forecast the quarterly revenue of hundreds of company using simply linear regression(with some preprocessing)

The data can be downloaded from https://tianchi.aliyun.com/competition/entrance/231660/information. There are lots of data files. However, I just use 'Balance Sheet.xls' actually.

To start, you need to download data from the link above and put 'Balance Sheet.xls' into the root dictionary. Then run 'xlstocsv.py'. This step is to transfer the xls file into csv so that we can read the data much faster.

Then you can run linear.py and it'll generate 'result.csv'.
