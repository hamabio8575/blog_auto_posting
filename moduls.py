import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.Qt import *

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import threading
import pandas as pd
import numpy as np
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
import pyautogui

import requests
import os
import random
from datetime import datetime

import pywinauto
from pywinauto import application
import autoit
import logging

import types, json


# print(pywinauto.__version__) # 0.6.3
#
# import inspect
# print(inspect.getfile(pywinauto))