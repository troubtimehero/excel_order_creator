# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/28 16:38
# software: PyCharm

"""
文件说明：

"""
try:
    from app import app
except Exception as err:
    with open('error.log', 'a') as f:
        f.write(f'{err}\n')

HOST = "127.0.0.1"
PORT = "9527"

if __name__ == '__main__':
    print("***************************** 操作提示 *****************************")
    print("********************* 请在下面网址复制到浏览器打开 *********************")
    print(f'http://{HOST}:{PORT}/')
    print("******************************************************************")

    try:
        app.run(host=HOST, port=PORT)
    except Exception as err:
        with open('error.log', 'a') as f:
            f.write(f'{err}\n')
