#mosiac.py




import PIL
from PIL import Image
import requests
from io import BytesIO
from PIL import ImageFilter
from PIL import ImageEnhance
from IPython.display import display
import numpy as np
import cv2
from itertools import product




#Open an image
# URL = "https://predictivehacks.com/wp-content/uploads/2019/08/RGBA.png"
URL = "https://i.ytimg.com/vi/L_LUpnjgPso/maxresdefault.jpg"
URL = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/natural-real-lightning-over-the-city-royalty-free-image-1592226477.jpg?crop=0.668xw:1.00xh;0.190xw,0&resize=640:*"
URL = "https://cdn.britannica.com/37/190637-050-E76719D7/Lightning-farm-field-energy-tree-Weather-electricity.jpg"
URL = "https://www.sciencealert.com/images/2019-04/processed/lightning_bolts_needles_1024.jpg"
URL = "https://cdn.pixabay.com/photo/2015/04/19/08/33/flower-729512__340.jpg"
response = requests.get(URL)
image = Image.open(BytesIO(response.content))
imgPath = "org.png"
image.save(imgPath)
averageColor = averagePixel(image)

makeSet = True
# image = image.resize((int(image.width/4),int(image.height/4)))

# get the mode of the image
h, w = image.height, image.width
image.mode
# it returns 'rgb'

#Choose mosiac parameters
gridw = 20*3
gridh = 20*3
blockw, blockh = int(w/gridw), int(h/gridh)

#create canvas
quality = 8
fh,fw = blockh * quality * gridh , blockw * quality * gridw
finalImage = Image.new('RGB', (fw, fh))

#currentColorAverage
def averagePixel(image,quality = 5):
    blocksum = [0,0,0]
    for pos in product(range(int(image.height/quality)), range(int(image.width/quality))):
        # print(pos)
        x = pos[0]*quality
        y = pos[1]*quality
        pixel = image.getpixel((y,x))
        blocksum[0] += pixel[0]
        blocksum[1] += pixel[1]
        blocksum[2] += pixel[2]
    finalColor = []
    for i in blocksum:
        finalColor.append(int(i/(image.width*image.height/(quality*quality))))
    return finalColor

def decrease_brightness(img, constant = 1.5):
    source = img.split()

    R, G, B = 0, 1, 2
    constant = 1.5 # constant by which each pixel is divided

    Red =   source[R].point(lambda i: max(0,min(i/constant,255)))
    Green = source[G].point(lambda i: max(0,min(i/constant,255)))
    Blue =  source[B].point(lambda i: max(0,min(i/constant,255)))

    im = Image.merge(img.mode, (Red, Green, Blue))
    return im
def increase_brightness(img, constant = 1.5):


    if constant < 1:
        return decrease_brightness(image,1/constant)
    source = img.split()

    R, G, B = 0, 1, 2
    constant = 1.5 # constant by which each pixel is divided

    Red =   source[R].point(lambda i: max(0,min(i*constant,255)))
    Green = source[G].point(lambda i: max(0,min(i*constant,255)))
    Blue =  source[B].point(lambda i: max(0,min(i*constant,255)))

    im = Image.merge(img.mode, (Red, Green, Blue))
    return im

def colorDiff(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

# print(f"{block} finalColor {finalColor}")
# for i in range(min(averageColor))
# collection.append([averageColor[0]-i,averageColor[1]-i,averageColor[2]-i])
# for i in range(255-max(averageColor))
# collection.append([averageColor[0]+i,averageColor[1]+i,averageColor[2]+i])
###### MAKE ACTUAL COLLECTION
imageSet = []
collection = {}
temp1, temp2 = image,image
enhancer = ImageEnhance.Brightness(image)
for i in range(30):
    pPath = f"imageP{i}.png"
    mPath = f"imageM{i}.png"
    if makeSet:
        temp1 = enhancer.enhance(1+i/10)
        temp2 = enhancer.enhance(1-i/30)
        temp1.save(pPath)
        temp2.save(mPath)
    else:
        temp1 = Image.open(pPath)
        temp2 = Image.open(mPath)
    imageSet.append(pPath)
    imageSet.append(mPath)
    collection[pPath] = averagePixel(temp1)
    collection[mPath] = averagePixel(temp2)


# collection[imagePath] = averagePixel(image)

# for imgPath in imageSet:



#Scan Blocks to get averate colors
blocks = {}
for block in product(range(gridw), range(gridh)):
    startx, starty = block[0]*blockw, block[1]*blockh
    # pxcount = 0
    blocksum = [0,0,0]
    for pos in product(range(blockw), range(blockh)):
        # print(f"pos {pos}")
        x,y = pos
        x += startx
        y += starty
        pixel = image.getpixel((x,y))
        # print(f"pixel {pixel[0]} {pixel[1]} {pixel[2]}")

        blocksum[0] += pixel[0]
        blocksum[1] += pixel[1]
        blocksum[2] += pixel[2]
    finalColor = []
    for i in blocksum:
        finalColor.append(int(i/(blockw*blockh)))
    print("....................")
    print(f"{block} finalColor {finalColor}")
    dmax, chosen = 999999999, None
    for av in collection:
        diff = colorDiff(collection[av],finalColor)
        print(collection[av])
        # print(diff)
        # print("...............")
        if diff < dmax:
            # print("@@@@@@@@@@@@",av)
            dmax = diff
            chosen = av
    print("....................")
    # print("XXXXXXXXXX")

    blocks[block] = finalColor, chosen

#build final image
for block in blocks:
    # print(block,blocks[block])
    startx, starty = block[0]*blockw*quality, block[1]*blockh*quality
    # print(blocks[block][1])
    chosenImage = Image.open(blocks[block][1])
    resized = chosenImage.resize((blockw*quality,blockh*quality))
    print(block)
    # print((startx,starty,startx+blockw*quality,starty+blockh*quality))
    # print(resized.width,resized.height)
    finalImage.paste(resized,(startx,starty,startx+resized.width,starty+resized.height))
    # finalImage add patch resized at startx, starty

finalImage.save("final2.png")


print("@@@@@@@@@@@@@ DONE")
finalImage.show()

#for every block find closest image

#resize and patch mosiac on canvas
