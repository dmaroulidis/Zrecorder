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
from config import *

def main(meeting_url, course_name, username, password, output_dir, command_only):
    """
    Main function that implements starting Chrome, joining a Zoom
    meeting and recording it.
    """

    default_wait_time = 10
    driver = get_browser()
    wait = WebDriverWait(driver, default_wait_time)
    join_meeting(driver, wait, meeting_url, username, password)

    # Start ffmpeg recording
    ffmpeg_params = FfmpegExecutorParams(video_encode_preset='ultrafast',
                                         h264_constant_rate_factor=0)
    sink = get_recording_filename(course_name, output_dir)
    ffmpeg_command = get_ffmpeg_command_lossless(ffmpeg_params, sink)
    if command_only:
        ffmpeg_proc = record(' '.join(ffmpeg_command))
        print('main(): Switching to wait_for_meeting_over()')
        wait_for_meeting_over(driver, wait, ffmpeg_proc)
    else:
        print(' '.join(ffmpeg_command))


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
parser.add_argument('-o', '--output-dir', action='store', type=Path,
                    help='directory to store recordings')
parser.add_argument('-f', '--command-only', action='store_false',
                    help='print ffmpeg command instead of recording meeting')
parser.add_argument('-c', '--config-file', type=argparse.FileType('r'),
                    help='INI file containing program configuration',
                    default='')
args = parser.parse_args()

if args.config_file:
    cfg = load_config(args.config_file)
    args.course_name, args.meeting_url, args.output_dir = get_course_info(cfg, print_menu(cfg))
    args.username = cfg['DEFAULT']['username']
    args.password = cfg['DEFAULT']['password']
#    args.output_dir = cfg['DEFAULT']['outputdir']
    print(args)

main(args.meeting_url, args.course_name, args.username, args.password,
     args.output_dir, args.command_only)
