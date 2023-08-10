import ctypes
from time import sleep
from io import BytesIO
from urllib import request
from pathlib import Path
from typing import Union

from PIL import Image
from PIL import ImageDraw


# # 项目根目录
# root_dir = Path(__file__).absolute().parent
# # 壁纸存储路径
# wallpaper_path = root_dir.joinpath(f'wallpaper_{display_width}x{display_height}.jpg')


def create_gradient_image(width: int, height: int, start_color: str, end_color: str) -> Image.Image:
    '''
    创建渐变图片

    Args:
        width - 图片宽度
        height - 图片高度
        start_color - 渐变起始颜色
        end_color - 渐变结束颜色
    '''
    # 创建一张空白图片
    gradient_image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(gradient_image)

    # 绘制渐变色
    for x in range(width):
        # 计算当前列的颜色值
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (x / (width - 1)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (x / (width - 1)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (x / (width - 1)))

        # 绘制当前列的颜色
        draw.line([(x, 0), (x, height)], fill=(r, g, b))

    return gradient_image


def get_myrl(retries: int = 5, retry_interval: Union[int, float] = 3) -> Union[None, Image.Image]:
    '''
    获取摸鱼人日历图片

    Args:
        retries - 重试次数
        retry_interval - 重试间隔(单位:秒)
    '''
    try:
        response = request.urlopen(
            'https://api.vvhan.com/api/moyu',
            timeout=10
        )
        return Image.open(BytesIO(response.read()))
    except Exception as err:
        if retries <= 0:
            return None
        if retry_interval > 0:
            sleep(retry_interval)
        return get_myrl(
            retries=retries-1,
            retry_interval=retry_interval
        )


def get_display_info() -> tuple:
    '''
    获取显示的信息
    '''
    # 显示器宽高
    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)

    return width, height


if __name__ == '__main__':
    # 获取显示器宽高
    display_width, display_height = get_display_info()
    # 获取摸鱼日历图片
    dgrrl_img = get_myrl()
    if not dgrrl_img:
        exit(1)
    # 生成渐变背景图
    background_img = create_gradient_image(display_width, display_height, (51, 33, 117), (4, 129, 129))

    # 将打工人日历图片居中粘贴到背景中
    background_img_width, background_img_height = background_img.size
    dgrrl_img_width, dgrrl_img_height = dgrrl_img.size
    paste_x = (background_img_width - dgrrl_img_width) // 2
    paste_y = (background_img_height - dgrrl_img_height) // 2
    background_img.paste(dgrrl_img, (paste_x, paste_y))

    # 将桌面壁纸存储到本地
    wallpaper_path = Path(__file__).absolute().parent.joinpath(f'wallpaper_{display_width}x{display_height}.png')
    background_img.save(wallpaper_path)

    # 设置为桌面壁纸
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(wallpaper_path), 0)
