from distutils.dir_util import copy_tree
from operator import itemgetter

import pandas as pd
import sys
from jinja2 import Environment, FileSystemLoader
import os


def generate_reports(folder):
    hosts = []
    # get all the paths of the root folder
    files = [os.path.join(folder, fn) for fn in next(os.walk(folder))[2] if not fn.startswith(".")]

    for logfile in files:
        try:
            data = pd.read_csv(logfile, delim_whitespace=True, comment='#', header=-1, index_col='timestamp',
                               parse_dates={'timestamp': [0, 1]})
            print "reading data from " + logfile
        except Exception, err:
            print "duplicate index occured in " + logfile

            print "There are two similar timestamps in the log." \
                  " To correct that error remove the duplicate entry from " + logfile

        hostname = os.path.basename(logfile).replace('.tab', "")

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
        host_data['net_rx'] = data.ix[:, 57].to_json(date_format='iso')
        host_data['net_tx'] = data.ix[:, 58].to_json(date_format='iso')

        hosts.append(host_data)

    env = Environment(loader=FileSystemLoader('templates'))
    env.add_extension("chartkick.ext.charts")

    cpu_template = env.get_template('cpu_template.html')
    memory_template = env.get_template('memory_template.html')
    disk_template = env.get_template('disk_template.html')
    network_template = env.get_template('network_template.html')

    cpu_output = cpu_template.render(
            hosts=sorted(hosts, key=itemgetter('name'), reverse=True),
    )
    memory_output = memory_template.render(
            hosts=sorted(hosts, key=itemgetter('name'), reverse=True),
    )
    disk_output = disk_template.render(
            hosts=sorted(hosts, key=itemgetter('name'), reverse=True),
    )
    network_output = network_template.render(
            hosts=sorted(hosts, key=itemgetter('name'), reverse=True),
    )

    test_name = os.path.basename(folder)
    test_name += "-report"
    if not os.path.exists(test_name):
        os.mkdir(test_name)

    os.chdir(test_name)



    # creating folder structure
    if not os.path.exists('css'):
        os.mkdir('css')
    if not os.path.exists('js'):
        os.mkdir('js')
    if not os.path.exists('img'):
        os.mkdir('img')
    if not os.path.exists('fonts'):
        os.mkdir('fonts')

    copy_tree(os.path.abspath('../css'), 'css')
    copy_tree(os.path.abspath('../js'), 'js')
    copy_tree(os.path.abspath('../img'), 'img')
    copy_tree(os.path.abspath('../fonts'), 'fonts')

    with open('report_cpu.html', 'w') as f:
        f.write(cpu_output)
    with open('report_memory.html', 'w') as f:
        f.write(memory_output)
    with open('report_disk.html', 'w') as f:
        f.write(disk_output)
    with open('report_network.html', 'w') as f:
        f.write(network_output)


def main(argv):
    try:
        folder = argv[1].strip()
        generate_reports(folder)
        print "########################################"
        print "report generated successfully"
    except Exception, err:
        print err.message
        print "should provide an input folder. ex : python plotter.py <input-folder>"


if __name__ == '__main__':
    main(sys.argv)
