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

def main():
    """Main function"""

    # Argument parser
    parser = argparse.ArgumentParser(prog='zrecorder',
                                     description='Record Zoom meetings')
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
    parser.add_argument('-f', '--command-only', action='store_false',
                        help='join meeting and output only the ffmpeg command')




if __name__ == "__main__":
    # execute only if run as a script
    main()
