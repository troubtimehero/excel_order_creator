# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/28 16:38
# software: PyCharm

"""
文件说明：

"""
import ctypes

from app import settings

try:
    from app import app
except Exception as err:
    print(err)
    with open('error.log', 'a') as f:
        f.write(f'{err}\n')


def main():
    print(f'http://{settings.HOST}:{settings.PORT}/order_creator')
    try:
        # ------------------- 隐藏窗口 -------------------
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
            ctypes.windll.kernel32.CloseHandle(whnd)

        app.run(host=settings.HOST, port=settings.PORT)
    except Exception as err:
        print(err)
        with open('error.log', 'a') as f:
            f.write(f'{err}\n')


if __name__ == '__main__':
    main()
