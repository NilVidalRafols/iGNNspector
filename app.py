from ignnspector.model.proposers import custom_studies
import eel
import os, random
from pathlib import Path
from datetime import datetime

from torch.functional import split

import persistence as per
from ignnspector import Graph
from ignnspector.analysis import analyse

#app settings needed during the execution of the app
app = {}


@eel.expose
def request_paths(name):
    if name == "" or name == None:
        app['explorer_path'] = Path(per.get_starting_path())
        path = app['explorer_path']
    elif name == "..":
        path = app['explorer_path'].parent
    else:
        path = list(app['explorer_path'].glob(name))[0]
    
    content = ''
    if path.is_file():
        app['file_path'] = path
        eel.set_graph(path.name, False)
    else:
        # return the contents of the selected directory
        content += '<tr value=".."><td>..</td><td></td>'
        for item in path.iterdir():
            content += f'<tr value="{item.name}">'
            content += '<td>' + item.name + '</td>'
            content += '<td>'
            if item.is_file():
                content += str(item.stat().st_size/1000000)
            content += '</td>'
            content += '</tr>'
            eel.set_paths(content)

    app['explorer_path'] = path
    

@eel.expose
def request_saved_reports():
    saved_reports = per.get_saved_reports()
    content = ''
    if len(saved_reports) == 0:
        content += '<p>There are no saved analysis reports.</p>'
    else:
        content += '<tr><td>'
        for report_name in map(lambda r: r['name'], saved_reports):
            content += f'<tr value="{report_name}">'
            content += '<td>' + report_name + '</td>'
            content += '</tr>'

    eel.set_saved_reports(content)


@eel.expose
def analyse_graph(name, is_saved, analysis):
    if is_saved:
        saved_reports = per.get_saved_reports()
        report = next((x for x in saved_reports if x['name'] == name), None)
        G = Graph()
        G.report = report
        # enter STAGE 2 (show analysis results)
        eel.set_stage(2)
    else:
        eel.message('#generating-graph')
        try:
            G = Graph(app['file_path'])
        except Exception:
            # if the graph can not be read, return '' 
            # and do not progress to STAGE 2
            eel.message('')
            eel.message('#not-graph')
            return ''
        else:
            # the graph has been generated successfully
            eel.message('')
            eel.message('#graph-generated')
            # analyse the graph
            eel.message('#analysing-graph')
            if 'time' in analysis.keys():
                G.report = analyse(G, time=analysis['time'])
            else:
                G.report = analyse(G, 
                                split_size=analysis['split_size'], 
                                num_splits=analysis['num_splits'])
            # enter STAGE 2 (show analysis results)
            eel.set_stage(2)
            eel.enable_button('#save-analysis-btn', True)

    app['graph'] = G
    content = ''
    for k, v in report.items():
            content += '<tr>'
            content += '<td>' + k + '</td>'
            if isinstance(v, dict):
                content += '<td>' + str(v['value']) + '</td>'
                content += '<td>' + str(v['time']) + '</td>'
            else:
                content += '<td>' + str(v) + '</td>'
            content += '</tr>'
    eel.set_graph_report(content)


@eel.expose
def save_analysis():
    per.save_analysis(app)

@eel.expose
def propose_models(proposal_settings):
    input_features = proposal_settings['input']
    output_features = proposal_settings['output']
    task = proposal_settings['task']
    preferences = proposal_settings['preferences']

    analysis_report = app['graph'].report

    analysis_report['in_features'] = int(input_features)
    analysis_report['out_features'] = int(output_features)
    analysis_report['task'] = task
    for preference in preferences:
        analysis_report[preference] = 'high'
    
    proposals = custom_studies(analysis_report)
    app['proposals'] = proposals

    content = ''
    for proposal, i in zip(proposals, range(len(proposals))):
        content += f'<tr value="{str(i)}">'
        content += '<td>' + proposal['model_type'] + '</td>'
        content += '<td>' + str(len(proposal['layers'])) + '</td>'
        content += '</tr>'
    eel.set_proposal_table(content)

@eel.expose
def save_proposal(index):
    proposal = app['proposals'][index]
    per.save_proposal(proposal)

def close_callback(route, websockets):
    if not websockets:
        print('Bye!')
        exit()


eel.init('presentation')


eel.start('index.html', mode='chrome', 
                        host='localhost', 
                        port=27000, 
                        block=True, 
                        disable_cache=True, 
                        size=(1280, 720),
                        close_callback=close_callback, 
                        cmdline_args=['--start-fullscreen', 
                                      '--incognito', 
                                      '--no-experiments'
                                    #   '--browser-startup-dialog',
                                      ])