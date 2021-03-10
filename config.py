#!/usr/bin/env python3
import configparser
import cli_ui
from pathlib import Path

def load_config(config_file):
    """
    Return configparser object containing parsed config from file object
    config_file.
    """
    cfg = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    cfg.read_file(config_file)
    return cfg

def get_course_info(cfg, course_name):
    """
    Return course name, and meeting_url.
    """
    if cfg.getboolean('DEFAULT', 'UseDefaultOutputDir', fallback=False):
        output_dir = cfg['DEFAULT']['outputdir']
    else:
        output_dir = cfg[course_name]['outputdir']
    return (course_name,
            cfg[course_name]['meetingurl'],
            output_dir)

def print_menu(cfg):
    """
    Print menu listing courses from cfg.
    """
    choice = cli_ui.ask_choice('Select course', choices=cfg.sections())
    return choice
