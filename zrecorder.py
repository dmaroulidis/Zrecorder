#!/usr/bin/env python

import argparse
import os
import datetime
from browserhelper import *
from media import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path

def main(meeting_url, course_name, username, password, output_dir):
    """
    Main function that implements starting Chrome, joining a Zoom
    meeting and recording it.
    """

    pass

# Argument parser
parser = argparse.ArgumentParser(
    description='''Record Zoom meetings. With no options, all required
    information will be read from environment variables.
    ''')
parser.add_argument('-m', '--meeting-url', action='store',
                    help='Zoom Meeting URL')
parser.add_argument('-u', '--username', action='store',
                    help='username to use when loging in to Zoom')
parser.add_argument('-p', '--password', action='store',
                    help='password to use when loging in to Zoom')
parser.add_argument('-n', '--course-name', action='store',
                    help='name of course to be recorded')
parser.add_argument('-o', '-output-dir', action='store', type=Path,
                    help='directory to store recordings')
args = parser.parse_args()
