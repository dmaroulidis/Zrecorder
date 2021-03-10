#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
from os import environ
from subprocess import TimeoutExpired

def get_browser():
    """
    Initializes a new Chrome instance with specific options and returns
    a Selenium webdriver object.
    """
    options = webdriver.ChromeOptions()

    prefs = {'hardware.audio_capture_enabled': True,
    'hardware.video_capture_enabled': True,
    'hardware.audio_capture_allowed_urls': ['https://tuc-gr.zoom.us'],
    'hardware.video_capture_allowed_urls': ['https://tuc-gr.zoom.us'],
    'URL_allow_list': ['zoommtg://'],
    'protocol_handler.allowed_origin_protocol_pairs': \
             {'https://tuc-gr.zoom.us': {'zoommtg': True}}}
    # Add prefs to Chrome's profile preferences
    options.add_experimental_option('prefs',prefs)
    options.add_argument("start-maximized")
    options.add_argument("kiosk")
    options.add_argument("enabled")
    options.add_argument("disable-infobars")
    options.add_argument("autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=options)
    return driver


def join_meeting(driver, wait, meeting_url, username, password):
    """
    Join Zoom meeting and login to Zoom if necessary. After getting into
    the meeting connect computer audio and mute the microphone if necessary.
    """
    driver.get(meeting_url)
    sleep(5)
    el = wait.until(
        lambda d: d.find_element_by_link_text('Join from Your Browser'))
    el.click()

    try:
        wait.until(EC.url_contains('idp.tuc.gr/'))
        institutional_login(driver, username, password)
    except TimeoutException:
        pass

    # Click Join button to join meeting
    el = wait.until(lambda d: d.find_element_by_id('joinBtn'))
    el.click()

    flag = False
    while not flag:
        try:
            title = wait.until(
                EC.title_contains('The meeting has not started - Zoom'))
            sleep(3)
        except TimeoutException:
            flag = True

    join_audio_btn = wait.until(lambda d:
        d.find_element_by_css_selector('.join-audio-by-voip > button'))
    #wait.until(EC.element_to_be_clickable(join_audio_btn))
    join_audio_btn.click()
    try:
        view_btn = wait.until(lambda d:
            d.find_element_by_css_selector(
                '#wc-container-left > div.full-screen-icon > div > button'))
        view_btn.click()
        fullscreen_btn = wait.until(lambda d:
            d.find_element_by_css_selector(
                '#wc-container-left > div.full-screen-icon > div > ul > li:nth-child(3) > a'))
        fullscreen_btn.click()
        try:
            collapse_menu = wait.until(lambda d:
                d.find_element_by_css_selector('body > div:nth-child(15) > div > div > div > div.suspension-window-container__tabs.suspension-window-container__tabs--hide'))
            minimize_panel_btn = wait.until(lambda d:
                d.find_element_by_css_selector('body > div:nth-child(15) > div > div > div > div > button:nth-child(1)'))

            ActionChains(driver).move_to_element(collapse_menu).click(minimize_panel_btn).perform()
        except TimeoutException:
            minimize_panel_btn = wait.until(lambda d:
                d.find_element_by_css_selector('body > div:nth-child(15) > div > div > div > div > button:nth-child(1)'))
        minimize_panel_btn.click()
    except TimeoutException:
        pass
    mute_mic(driver)


def quit_meeting(driver, wait):
    '''Quit Zoom meeting'''
    leave_button = driver.find_element_by_css_selector('.footer__leave-btn-container > button')
    if leave_button.text == 'Leave':
        leave_button.click()
        confirmation_btn = wait.until(lambda d: d.find_element_by_css_selector(
            '.leave-meeting-options__inner > button'))
        confirmation_btn.click()
        driver.quit()

def launch_meeting(driver):
    '''Launch meeting in Chrome'''
    pass

def institutional_login(driver, username, password):
    '''Login to Zoom using instititutional credentials'''
    username_field = driver.find_element_by_id('username')
    username_field.send_keys(username + Keys.TAB)
    password_field = driver.find_element_by_id('password')
    password_field.send_keys(password + Keys.ENTER)

    try:
        driver.find_element_by_name('_eventId_proceed').click()
    except NoSuchElementException:
        pass

def mute_mic(driver):
    '''Mute our microphone if unmuted'''
    mic_button = driver.find_element_by_css_selector('.join-audio-container > button')

    if mic_button.text == 'Mute':
        # Mute our microphone
        mic_button.click()

def wait_for_meeting_over(driver, wait, ffmpeg_proc):
    '''Wait until the meeting has ended'''
    flag = False
    while not flag:
        try:
            popup = wait.until(lambda d: d.find_element_by_css_selector('.zm-modal-body-content'))

            if popup.text == 'This meeting has been ended by host.':
                driver.quit()
                flag = True
                try:
                    cmdout = ffmpeg_proc.communicate(input='q', timeout=10)
                    print('Meeting ended. Stopping ffmpeg recording.')
                    print(cmdout)
                except TimeoutExpired as e:
                    ffmpeg_proc.kill()
                    print('[WARN] ffmpeg process killed' + e)

        except TimeoutException as e:
            pass
