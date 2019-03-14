from PIL import Image
import os
import glob
import random

picturefolder = 'Pictures/'
finishedfolder = 'Finished/'
validimagefiles = ['.png', '.jpeg']
numbers = '0123456789'


def delete_numbers(string):
    endstring = ''
    for letter in string:
        if letter not in numbers:
            endstring += letter

    return endstring


def fetch_images(picturefolder):
    allfiles = os.listdir(picturefolder)
    #allfiles = ['und.png', 'und.pdf', 'und123.png']

    imagefiles = []
    # delete everything that isn't an image
    for file in allfiles:
        head, tail = os.path.splitext(file)

        if tail not in validimagefiles:
            continue

        head = delete_numbers(head)

        imagefiles.append((head, file))

    print(allfiles)
    print(imagefiles)
    print('--- Images Loaded ---')

    return imagefiles


images = fetch_images(picturefolder)

stringtoimage = 'undead'


def fetch_fitting_image(searchedstring, images):
    pure_image_names = [image[0] for image in images]

    if not searchedstring in pure_image_names:
        return None

    allmatching = [image for image in images if image[0] == searchedstring]

    return random.choice(allmatching)


def select_images(stringtoimage, images):
    remainingstring = stringtoimage
    textimages = []

    while True:
        if remainingstring[0] == ' ':
            print('space')
            textimages.append(('space', 'space'))
            remainingstring = remainingstring[1:]

        i = len(remainingstring)
        while True:
            if i < 0:
                raise Exception('no image found')

            img = fetch_fitting_image(remainingstring[0:i], images)

            if img is not None:
                break

            i -= 1

        textimages.append(img)
        remainingstring = remainingstring[i:]

        if len(remainingstring) < 1:
            break

    print(textimages)

    return textimages


def string_to_image(stringtoimage, images):
    height = 128

    textimages = select_images(stringtoimage, images)

    # open the first image
    imagefile = textimages[0][1]
    imagefile = Image.open(os.path.join(picturefolder, imagefile))
    print(imagefile)

    relativeheight = height / imagefile.size[1]
    resized = imagefile.resize((round(imagefile.size[0] * relativeheight), height))

    endimage = resized

    for img in textimages[1:]:
        offset = endimage.size[0]
        if img[0] == 'space':
            empty = Image.new('RGB', (round(height / 16 * 9), height))
            topaste = empty
        else:
            imagefile = Image.open(os.path.join(picturefolder, img[1]))
            relativeheight = height / imagefile.size[1]
            resized = imagefile.resize((round(imagefile.size[0] * relativeheight), height))
            topaste = resized

        endimage2 = Image.new('RGB', (endimage.size[0] + topaste.size[0], height))
        endimage2.paste(endimage, (0, 0))
        endimage2.paste(topaste, (offset, 0))

        endimage = endimage2
        print(endimage.size[0])

    finalpath = os.path.join(finishedfolder, 'test.png')
    endimage.save(finalpath, 'PNG')

    return finalpath


path = string_to_image(stringtoimage, images)
