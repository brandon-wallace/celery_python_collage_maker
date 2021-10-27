import time
from datetime import datetime
from celery import Celery
from PIL import Image, ImageOps


celery = Celery('tasks', backend='rpc://', broker='pyamqp://guest@127.0.0.1')


def open_file(filename):
    '''Open image file with pillow'''

    try:
        img_obj = Image.open(filename)
        return img_obj
    except FileNotFoundError as e:
        print(e)
        exit()


def resize_image(image_file, size=500, border=10, bg=(0, 0, 0, 0)):
    '''Resize images to square shapes'''

    image = open_file(image_file)
    image_png = image.convert('RGBA')
    image_resized = image_png.resize((size, size))
    image_with_border = ImageOps.expand(image_resized, border=border, fill=bg)
    filename = f'resized_{datetime.utcnow().strftime("%Y%m%d%H%M%S%f")}.png'
    image_with_border.save(f'{filename}')
    return filename


@celery.task(bind=True)
def merge_images(self, images):
    '''Create collage by merging images together'''

    time.sleep(10)
    image_objects = []
    for filename in images:
        img_obj = open_file(filename)
        image_objects.append(img_obj)
    total_width = sum(img.width for img in image_objects)
    merged_image = Image.new('RGBA', (total_width, image_objects[0].height))
    x_axis = 0
    for img in image_objects:
        merged_image.paste(img, (x_axis, 0))
        x_axis += img.width
    filename = f'collage_{datetime.utcnow().strftime("%Y%m%d%H%M%S%f")}.png'
    merged_image.save(f'{filename}')
    return 'COMPLETED'
