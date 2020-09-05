# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/21 15:13
# software: PyCharm

"""
文件说明：

"""
# from PIL import Image
import os
import ctypes


def tips_only(msg, title):
    ctypes.windll.user32.MessageBoxW(0, msg, title, 1)
