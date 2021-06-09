import os
import pathlib as p
import sys
import yaml

def get_settings():
    stick = '\\' if sys.platform == 'win32' else '/'
    with open('persistence'+stick+'settings.yaml', 'r') as f:
        settings = yaml.full_load(f)
        if settings is None:
            settings = {}
    return settings

def get_starting_path():
    settings = get_settings()
    if 'starting_path' in settings and settings['starting_path'] != "":
        return p.Path(settings['starting_path'])
    else:
        return p.Path.home()

def get_saved_reports():
    stick = '\\' if sys.platform == 'win32' else '/'
    dir = p.Path('persistence'+stick+'reports')
    reports = []
    for path in dir.iterdir():
        if path.is_file():
            with open(path, 'r') as f:
                report = yaml.full_load(f)
            reports.append(report)
    return reports