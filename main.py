import time
from project.tasks import resize_image, merge_images


def task_status(task_id):

    task = merge_images.AsyncResult(task_id)
    return task


def main():
    '''Main function to run application'''

    # Temporary hard coded image filenames!!!!
    # images = ['pic1.jpg', 'pic2.jpg', 'pic3.jpg']
    images = ['pic1.png', 'pic2.png', 'pic3.png']
    resized = []
    for img in images:
        filename = resize_image(img, 500, border=20)
        resized.append(filename)
    task = merge_images.delay(resized)
    while task_status(task.status) != 'SUCCESS':
        time.sleep(1)
        print('PLEASE WAIT...')
        print(f'Status: {task_status(task.status)}')
    print('TASK COMPLETE')
    print(f'Status: {task_status(task.status)}')


if __name__ == '__main__':
    main()
