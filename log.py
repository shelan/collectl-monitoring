from operator import itemgetter

import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

folder = '/Users/shelan/projects/karamel/karamel-stats/new-temp/tmp'
hosts =[]
# get all the paths of the root folder
files = [os.path.join(folder, fn) for fn in next(os.walk(folder))[2] if not fn.startswith(".")]

for file in files:
    data = pd.read_csv(file, delim_whitespace=True, comment='#', header=-1, index_col='timestamp',
                       parse_dates={'timestamp': [0, 1]})

    hostname = os.path.basename(file).replace('.tab', "")

    host_data ={}
    host_data ['name'] = hostname

    host_data['mem_data'] = data.ix[:, 20].to_json(date_format='iso')
    host_data['cpu_data'] = data.ix[:, 2].to_json(date_format='iso')
    host_data['cpu_load'] = data.ix[:, 16].to_json(date_format='iso')

    disk_read = data.ix[:, 64]
    disk_write = data.ix[:, 65]

    hosts.append(host_data)


env = Environment(loader=FileSystemLoader('templates'))
env.add_extension("chartkick.ext.charts")
template = env.get_template('cpu_template.html')

output = template.render(
    hosts=sorted(hosts, key=itemgetter('name'),reverse=True) ,
)

with open('report_memory.html', 'w') as f:
    f.write(output)

