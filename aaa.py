import datetime

format = '%Y-%m-%dT%H:%M:%S'
dat = "2022-12-03T19:16:33+0300"[:-5]
datetime = datetime.datetime.strptime(dat, format)
print(datetime.date())
