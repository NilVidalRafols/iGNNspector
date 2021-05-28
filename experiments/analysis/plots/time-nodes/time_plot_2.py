import sys
import math

sys_path = '/experiments/analysis/ogbn-products'
sys.path.append(sys.path[0].replace(sys_path, ''))

from matplotlib import pyplot as plt
import csv
import yaml

def generate_plot(settings):
    tables = {}
    tables['content'] = []
    for table_path in settings['table_paths']:
        with open(table_path) as f:
            csv_reader = csv.reader(f, delimiter=',')
            tables['header'] = next(csv_reader)
            split_length = []
            execution_time = []
            for row in csv_reader:
                split_length.append(int(row[0]))
                column_index = tables['header'].index(settings['columns'][0])
                execution_time.append(float(row[column_index]))
                content = list(zip(split_length, execution_time))
                tables['content'] = tables['content'] + content
    tables['content'] = list(sorted(tables['content']))

    if settings['scale'] == 'log':
        plt.semilogy()
        # for _, l in execution_time.items():
        #     l = list(map(math.log10, l))

    xpoints = [n for n, _ in tables['content']]
    ypoints = [t for _, t in tables['content']]

    plt.scatter(xpoints, ypoints, s=8, label=settings['columns'][0])

    plt.xlabel('num nodes')
    plt.ylabel('time (s)')

    plt.grid()
    # plt.ylim(0, max([max(l) for _, l in execution_time.items()]) + 1)
    plt.legend()
    plt.savefig(settings['output_path'])
    plt.close()

if __name__ == '__main__':
    # Get settings from yaml file
    settings_path = sys.argv[1]
    with open(settings_path, 'r') as f:
        settings = yaml.full_load(f)

    for plot_settings in settings['plots']:
        plot_settings.update({k:v for k,v in settings.items() if k != 'plots'})
        generate_plot(plot_settings)
