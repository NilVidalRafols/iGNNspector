import sys
import math

sys_path = '/experiments/analysis/ogbn-products'
sys.path.append(sys.path[0].replace(sys_path, ''))

from matplotlib import pyplot as plt
import csv
import yaml


def generate_plot(settings):
    table_path = settings['table_path']
    columns = settings['columns']
    output_path = settings['output_path']

    # read csv table file
    with open(table_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        # extract ls with the data
        split_length = []
        execution_time = { key:[] for key in columns}
        line_count = 0
        header = next(csv_reader)
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                split_length.append(int(row[0]))
                for key, l in execution_time.items():
                    column_index = header.index(key)
                    l.append(float(row[column_index]))
                line_count += 1
        print(f'Processed {line_count} lines.')
        # print(split_length)
        # print(execution_time)

    if settings['scale'] == 'log':
        plt.semilogy()
        # for _, l in execution_time.items():
        #     l = list(map(math.log10, l))

    xpoints = split_length

    for key, l in execution_time.items():
        plt.scatter(xpoints, l, s=8)
        plt.plot(xpoints, l, label=key)

    if settings['annotate']:
        for key, l in execution_time.items():
            for x,y in zip(xpoints, l):
                label = "{:.2f}".format(y)
                plt.annotate(label, # this is the text
                            (x,y), # this is the point to label
                            textcoords="offset points", # how to position the text
                            xytext=(0,8), # distance from text to points (x,y)
                            ha='center',
                            fontsize=8) # horizontal alignment can be left, right or center

    plt.xlabel('num nodes')
    plt.ylabel('time (s)')

    plt.grid()
    # plt.ylim(0, max([max(l) for _, l in execution_time.items()]) + 1)
    plt.legend()
    plt.savefig(output_path)
    plt.close()


if __name__ == '__main__':
    # Get settings from yaml file
    settings_path = sys.argv[1]
    with open(settings_path, 'r') as f:
        settings = yaml.full_load(f)

    for plot_settings in settings['plots']:
        generate_plot(plot_settings)
