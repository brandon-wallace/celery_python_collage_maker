from project.tasks import resize_image, merge_images


def main():
    '''Main function to run application'''

    # Temporary hard coded image filenames!!!!
    images = ['pic1.jpg', 'pic2.jpg', 'pic3.jpg']
    resized = []
    for img in images:
        filename = resize_image(img, 500, border=20)
        resized.append(filename)
    merge_images.delay(resized)


if __name__ == '__main__':
    main()
