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

def main(meeting_url, course_name, username, password, output_dir, command_only):
    """
    Main function that implements starting Chrome, joining a Zoom
    meeting and recording it.
    """

    default_wait_time = 10
    wait = WebDriverWait(driver, default_wait_time)
    driver = get_browser()
    join_meeting(driver, wait, meeting_url, username, password)

    # Start ffmpeg recording
    ffmpeg_params = FfmpegExecutorParams(video_encode_preset='ultrafast',
                                         h264_constant_rate_factor=0)
    sink = get_recording_filename(course_name, output_dir)
    ffmpeg_command = get_ffmpeg_command_lossless(ffmpeg_params, sink)
    if command_only:
        ffmpeg_proc = record(ffmpeg_command)
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
args = parser.parse_args()

main(args.meeting_url, args.course_name, args.username, args.password,
     args.output_dir, args.command_only)
