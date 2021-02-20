#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from browserhelper import *
from media import *
from datetime import datetime


default_wait_time = 10
# Initialize ChromeOptions object
options = webdriver.ChromeOptions()
# Make Chrome use a specific profile, to keep settings
options.add_argument("user-data-dir=chrome_profile")
options.add_argument("start-maximized")
options.add_argument("kiosk")
options.add_argument("enabled")
options.add_argument("disable-infobars")
options.add_argument("autoplay-policy=no-user-gesture-required")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, default_wait_time)
zoom_link = os.environ['ZOOM_LINK']
driver.get(zoom_link)
sleep(5)
el = wait.until(lambda d: d.find_element_by_link_text('Join from Your Browser'))
el.click()
#driver.find_element_by_link_text('Join from Your Browser').click()
# Login
try:
    wait.until(EC.url_contains('idp.tuc.gr/'))
    institutional_login(driver)
except TimeoutException:
    pass

# Join Zoom call
driver.find_element_by_id('joinBtn').click()
# Select computer audio
#driver.find_element_by_css_selector('.join-audio-by-voip > button').click()

join_audio_btn = wait.until(lambda d: d.find_element_by_css_selector('.join-audio-by-voip > button'))
join_audio_btn.click()
#driver.find_element_by_tag_name('body').send_keys(Keys.TAB + Keys.ENTER)
mute_mic(driver)
#driver.fullscreen_window()
# Get current window handle
current_window = driver.current_window_handle

# Start ffmpeg recording
ffmpeg_params = FfmpegExecutorParams(video_encode_preset='ultrafast',
                                     h264_constant_rate_factor=0)

now = datetime.now()
extension = now.strftime('%d-%m-%Y_%H-%M-%S.mkv')
course_name = os.environ['COURSE_NAME'].replace(' ', '_')
path = os.environ['ZREC_OUT_FOLDER'] + '/' + course_name + '_' + extension
sink = Sink(path=path)

ffmpeg_command = get_ffmpeg_command_lossless(ffmpeg_params, sink)
ffmpeg_proc = record(ffmpeg_command)

# Wait until meeting is over
wait_for_meeting_over(driver, wait, ffmpeg_proc)
