#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
from os import environ
from subprocess import TimeoutExpired

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

def institutional_login(driver):
    '''Login to Zoom using instititutional credentials'''
    uni_username = environ['UNI_USERNAME']
    uni_password = environ['UNI_PASSWORD']
    driver.find_element_by_id('username').send_keys(uni_username + Keys.TAB)
    driver.find_element_by_id('password').send_keys(uni_password + Keys.ENTER)
    try:
        driver.find_element_by_name('_eventId_proceed').click()
    except NoSuchElementException as e:
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
                except TimeoutExpired as e:
                    ffmpeg_proc.kill()
                    print('[WARN] ffmpeg process killed' + e)

        except TimeoutException as e:
            pass
