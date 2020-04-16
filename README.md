# TianChi-Quarterly-Revenue-Forecast
This project is to forecast the quarterly revenue of hundreds of company using simply linear regression(with some preprocessing)

The data can be downloaded from https://tianchi.aliyun.com/competition/entrance/231660/information. There are lots of data files. However, I just use 'Income Statement.csv' actually.

To start, you need to download data from the link above and put 'Balance Sheet.xls' into the root dictionary. Then run 'xlstocsv.py'. This step is to transfer the xls file into csv so that we can read the data much faster.

Then you can run linear.py and it'll generate 'result.csv'.

I use raw data, sum of a whole year and growth rate of the whole year revenue to do the regression. Since the data is not clean and there are some strange data like having only one season revenue in a whole year, I use 'except' to identify them and fill in the average as prediction.

The result was good since I could get the No.92 out of thousands of groups and No.57 out of 100 groups in the second stage. (This is a good example that with good data management, the easy model can also be competitive .)
