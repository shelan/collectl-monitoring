import json
from jinja2 import Template, Environment, FileSystemLoader
import pandas as pd
import pandas_highcharts
from pandas_highcharts.core import serialize

file = open('/Users/shelan/projects/karamel/karamel-stats/172.28.128.7/vm3-hostname-20151209.tab')

# data = {}
# times = []
#
# x = []
# y = []
#
# for line in file:
#
#     if line.startswith('#'):
#         #print(line)
#
#     if not line.startswith('#'):
#         items = line.split(' ')
#         data[items[1]] = items[2::]
#         time = items[1].split(':')
#
#         # date_time = str(items[0]) + '' + str(items[1])
#
#         # times.append(datetime.strptime(date_time,"%Y%m%d%H:%M:%S"))
#
#         times.append(items[1])
#         # times.append(datetime.strptime(date_time, '%Y%m%d%H:%M:%S').date())
#         y.append(items[4])
#
# # print(data.values())
# # print(data.keys())

data = pd.read_csv(file, delim_whitespace=True, skiprows=14, index_col='timestamp', parse_dates={'timestamp': [0,1]})

print data

#
# print data.to_json()
# print data.to_dict()

env = Environment(loader=FileSystemLoader('templates'))
env.add_extension("chartkick.ext.charts")
template = env.get_template('report.html')

data_cpu = data.ix[:, '[MEM]Free']
print data_cpu.to_dict()
# chart = serialize(data_cpu, render_to='my-chart',output_type='json')


data_to_render = {}

data_to_render["data"] = data_cpu.to_json()

exchange = {'2001-01-31': 1.064, '2002-01-31': 1.1305,
            '2003-01-31': 0.9417, '2004-01-31': 0.7937,
            '2005-01-31': 0.7609, '2006-01-31': 0.827,
            '2007-01-31': 0.7692, '2008-01-31': 0.6801,
            '2009-01-31': 0.7491, '2010-01-31': 0.7002,
            '2011-01-31': 0.7489, '2012-01-31': 0.7755,
            '2013-01-31': 0.7531,
            }

#data['timestamp'] = pd.to_datetime(data['timestamp'],unit='s')

output = template.render(data=data_cpu.to_dict())


print data_to_render

with open('my_new_html_file.html', 'w') as f:
    f.write(output)

with open('report.html', 'w') as f:
    f.write(data.to_html())



# print chart




# x = range(len(data))
#
# # dates = plt.matplotlib.dates.date2num(times)
# plt.plot_date(x, y,'-o')
#
# plt.subplots_adjust(bottom=0.15)
# plt.xticks(x, times, rotation='vertical')
# plt.gcf().autofmt_xdate()
#
# # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d%H:%M:%S'))
# # plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
# # plt.plot(x, y)
# # plt.gcf().autofmt_xdate()
#
# plt.show()
