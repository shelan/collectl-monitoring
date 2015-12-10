import pandas as pd
from jinja2 import Environment, FileSystemLoader

file = open('/Users/shelan/projects/karamel/karamel-stats/172.28.128.7/vm3-hostname-20151209.tab')

data = pd.read_csv(file, delim_whitespace=True, skiprows=14, index_col='timestamp', parse_dates={'timestamp': [0, 1]})

env = Environment(loader=FileSystemLoader('templates'))
env.add_extension("chartkick.ext.charts")
template = env.get_template('report.html')

mem_data = data.ix[:, '[MEM]Free']
cpu_data = data.ix[:, '[CPU]Sys%']

output = template.render(
    mem_data=mem_data.to_json(date_format='iso'),
    cpu_data=cpu_data.to_json(date_format='iso')
)

with open('my_new_html_file.html', 'w') as f:
    f.write(output)
