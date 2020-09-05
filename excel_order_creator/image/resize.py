# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/4 17:35
# software: PyCharm

"""
文件说明：
更改图片尺寸大小
"""
import os
import os.path
from PIL import Image
'''
file_in: 输入图片
file_out: 输出图片
width: 输出图片宽度
height:输出图片高度
type:输出图片类型（png, gif, jpeg...）
'''


def resize_image(filein, fileout, width, height, _type):
    img = Image.open(filein)
    out = img.resize((width, height), Image.ANTIALIAS)      # resize image with high-quality
    out.save(fileout, _type)


def get_size(file):
    with Image.open(file) as im:    # 返回一个Image对象
        return im.size


def get_scale_to_tar_size(file, width, height):
    size = get_size(file)
    scale = min(width / size[0], height / size[1])
    print(f'[in] w: {size[0]}, h: {size[1]}  [out] scale:{scale}, width:{scale * size[0]}')
    return scale, scale*size[0]
