import io
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

TEXT_PATH = Path(__file__).parent / "texture2d"
char_mask = Image.open(TEXT_PATH / "char_mask.png")
char_fg = Image.open(TEXT_PATH / "char_fg.png")

# 设置模板目录
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

app = FastAPI()


@app.get("/")
def get_upload_page(request: Request):
    """返回图片上传和处理的HTML页面"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/rover-card/")
def rover_card(image: UploadFile = File(...)):
    """处理上传的图片并返回处理后的图片"""
    try:
        # 验证文件类型
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="请上传有效的图片文件")

        # 读取上传的图片
        role_pile = Image.open(image.file)

        # 确保图片有RGBA模式
        if role_pile.mode != "RGBA":
            role_pile = role_pile.convert("RGBA")

        # 创建最终图片画布，使用与遮罩相同的尺寸
        role_pile_image = Image.new("RGBA", (560, 1000))

        # 调整图片尺寸
        role_pile = resize_and_center_image(role_pile, is_custom=True)
        role_pile_image.paste(
            role_pile,
            ((560 - role_pile.size[0]) // 2, (1000 - role_pile.size[1]) // 2),
            role_pile,
        )

        # 应用遮罩和前景 - 直接在同一画布上操作
        # 创建一个临时图片来应用遮罩效果
        img = Image.new("RGBA", (560, 1000))
        img.paste(role_pile_image, (10, 0), char_mask)
        img.paste(char_fg, (10, 0), char_fg)

        role_pile_image = img

        # 将图片转换为字节流
        img_byte_arr = io.BytesIO()
        role_pile_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # 返回图片流
        return StreamingResponse(
            io.BytesIO(img_byte_arr.read()),
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=processed_card.png"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片处理失败: {str(e)}")


def resize_and_center_image(
    image, output_size=(560, 1000), background_color=(255, 255, 255, 0), is_custom=False
):
    """
    根据输入的图片，调整其尺寸以尽量填充目标尺寸，并保持居中。
    若宽度过长或高度过长，会根据图片的比例自动调整，以保持居中并尽量维持固定尺寸（560x1000）。

    :param image: 原始图片对象
    :param output_size: 输出图片大小 (宽度, 高度)
    :param background_color: 填充背景的颜色 (默认为透明)
    :param is_custom: 是否为自定义面板，决定是否需要调整图片
    :return: 调整后的图片对象
    """
    # 如果不需要自定义调整，直接返回原图
    if not is_custom:
        return image

    image = image.copy()

    # 获取原始图片的宽度和高度
    img_width, img_height = image.size
    target_width, target_height = output_size

    # 如果图片的宽度大于高度，则根据宽度缩放图片
    if img_width > img_height:
        scale_factor = target_width / img_width
        new_width = target_width
        new_height = int(img_height * scale_factor)
    else:
        scale_factor = target_height / img_height
        new_width = int(img_width * scale_factor)
        new_height = target_height

    image = image.resize((new_width, new_height))

    result_image = Image.new("RGBA", output_size, background_color)

    # 计算粘贴位置，居中对齐
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2

    result_image.paste(image, (paste_x, paste_y), image)

    return result_image
