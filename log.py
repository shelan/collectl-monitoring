from operator import itemgetter
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

folder = '/Users/shelan/projects/karamel/karamel-stats/terasort-200'
hosts = []
# get all the paths of the root folder
files = [os.path.join(folder, fn) for fn in next(os.walk(folder))[2] if not fn.startswith(".")]

for file in files:
    data = pd.read_csv(file, delim_whitespace=True, comment='#', header=-1, index_col='timestamp',
                       parse_dates={'timestamp': [0, 1]})

    hostname = os.path.basename(file).replace('.tab', "")

    host_data = {}
    host_data['name'] = hostname

    # CPU data
    host_data['cpu_data'] = data.ix[:, 2].to_json(date_format='iso')
    host_data['cpu_load'] = data.ix[:, 16].to_json(date_format='iso')

    # Memorydata
    host_data['mem_data'] = data.ix[:, 20].apply(lambda x: x / 1024000).to_json(date_format='iso')

    # Disk data
    host_data['disk_read'] = data.ix[:, 66].apply(lambda x: x / 1024).to_json(date_format='iso')
    host_data['disk_write'] = data.ix[:, 67].apply(lambda x: x / 1024).to_json(date_format='iso')

    # Network Data


    hosts.append(host_data)

env = Environment(loader=FileSystemLoader('templates'))
env.add_extension("chartkick.ext.charts")

cpu_template = env.get_template('cpu_template.html')
memory_template = env.get_template('memory_template.html')
disk_template = env.get_template('disk_template.html')

cpu_output = cpu_template.render(
    hosts=sorted(hosts, key=itemgetter('name'), reverse=True),
)
memory_output = memory_template.render(
    hosts=sorted(hosts, key=itemgetter('name'), reverse=True),
)
disk_output = disk_template.render(
    hosts=sorted(hosts, key=itemgetter('name'), reverse=True),
)

with open('report_cpu.html', 'w') as f:
    f.write(cpu_output)
with open('report_memory.html', 'w') as f:
    f.write(memory_output)
with open('report_disk.html', 'w') as f:
    f.write(disk_output)
