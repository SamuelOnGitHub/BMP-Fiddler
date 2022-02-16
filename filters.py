import math
import copy

def dimensions(pixels):
    height = len(pixels)
    width = len(pixels[0])
    i = 1
    while pixels[0][-i] == 0:
        width -= 1
        i += 1
    return height, width

def greyscale(pixels):

    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            brightness = 0
            for c in range(len(pixels[h][w])):
                pixels[h][w][c] = int((pixels[h][w][0] + pixels[h][w][1] + pixels[h][w][2]) / 3)
    return pixels
            
def reflect(pixels):

    height, width = dimensions(pixels)

    for h in range(height):
        row = pixels[h].copy()
        for w in range(width):
            pixels[h][w] = row[width - (w + 1)]

    return pixels

def verticalreflect(pixels):

    height, width = dimensions(pixels)

    for w in range(width):
        row = []
        for h in range(height):
            row.append(pixels[h][w])
        for h in range(height):
            pixels[h][w] = row[height - (h + 1)]

    return pixels

def colourscreen(pixels, colour):
    n = 0
    if colour == "b":
        n = 0
    elif colour == "g":
        n = 1
    elif colour == "r":
        n = 2

    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            for c in range(3):
                if c != n:
                    pixels[h][w][c] = 0

    return pixels
        
def colourfilter(pixels, colour): ##work on
    n = 0
    if colour == "b":
        n = 0
    elif colour == "g":
        n = 1
    elif colour == "r":
        n = 2

    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            total = pixels[h][w][0] + pixels[h][w][1] + pixels[h][w][2]
            if pixels[h][w][n] - pixels[h][w][(n+1) % 3] < 25 or pixels[h][w][n] - pixels[h][w][(n+2) % 3] < 25:
                pixels[h][w][0] = int(total/3)
                pixels[h][w][1] = int(total/3)
                pixels[h][w][2] = int(total/3)

    return pixels

def blur(pixels, blurriness):

    height, width = dimensions(pixels)

    pixelcopy = copy.deepcopy(pixels)

    for h in range(height):
        for w in range(width):
            bluetotal = 0
            greentotal = 0
            redtotal = 0
            i = 0
            for y in range(-blurriness, blurriness):
                for x in range(-blurriness, blurriness):
                    if h + y < height and h + y >= 0 and w + x < width and w + x >= 0:
                        bluetotal += pixelcopy[h+y][w+x][0]
                        greentotal += pixelcopy[h+y][w+x][1]
                        redtotal += pixelcopy[h+y][w+x][2]
                        i += 1
            pixels[h][w][0] = int(bluetotal / i)
            pixels[h][w][1] = int(greentotal / i)
            pixels[h][w][2] = int(redtotal / i)

    return pixels

def closeness(pixels, a, b, n):

    height, width = dimensions(pixels)

    y = int(a * height)
    x = int(b * width)

    for h in range(height):
        for w in range(width):
            distance = math.sqrt( pow(abs(y - h),2) + pow(abs(x - w),2) )
            if distance > n :
                closeScore = n / distance
            else:
                closeScore = 1
            pixels[h][w][0] = int(pixels[h][w][0] * closeScore)
            pixels[h][w][1] = int(pixels[h][w][1] * closeScore)
            pixels[h][w][2] = int(pixels[h][w][2] * closeScore)

    return pixels

def invert(pixels):

    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            pixels[h][w][0] = 255 - pixels[h][w][0]
            pixels[h][w][1] = 255 - pixels[h][w][1]
            pixels[h][w][2] = 255 - pixels[h][w][2]

    return pixels

def edgedetect(pixels):

    height, width = dimensions(pixels)
    pixelscopy = copy.deepcopy(pixels)

    for h in range(height):
        for w in range(width):
            for c in range(3):
                totalY = 0
                totalX = 0
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        if h + y >=0 and h + y < height and w + x >= 0 and w + x < width:
                            totalY += (y * (2 - abs(x))) * pixelscopy[h+y][w+x][c]
                            totalX += (x * (2 - abs(y))) * pixelscopy[h+y][w+x][c]
                gValue = math.sqrt(pow(totalY,2) + pow(totalX,2))
                if gValue > 255:
                    gValue = 255
                pixels[h][w][c] = int(gValue)

    return pixels
                                
def greenscreen(pixels1, pixels2):
    strength = 10
    height1, width1 = dimensions(pixels1)
    height2, width2 = dimensions(pixels2)

    height = min(height1, height2)
    width = min(width1, width2)

    for h in range(height):
        for w in range(width):
            if pixels1[h][w][0] < strength and pixels1[h][w][1] < strength and pixels1[h][w][2] > 255 - strength:
                pixels1[h][w] = pixels2[h][w]
    return pixels1

def brightness(pixels):
    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            for c in range(3):
                pixels[h][w][c] += 20
                if pixels[h][w][c] > 255:
                    pixels[h][w][c] = 255
    return pixels

def dimness(pixels):
    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            for c in range(3):
                pixels[h][w][c] -= 20
                if pixels[h][w][c] < 0:
                    pixels[h][w][c] = 0
    return pixels

def desaturate(pixels):
    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            average = (pixels[h][w][0] + pixels[h][w][1] + pixels[h][w][2]) / 3
            for c in range(3):
                pixels[h][w][c] = int(((pixels[h][w][c] * 2) + average) / 3) 
    return pixels

def saturate(pixels):
    height, width = dimensions(pixels)

    pixelscopy = copy.deepcopy(pixels)
    for h in range(height):
        for w in range(width):
            average = (pixelscopy[h][w][0] + pixelscopy[h][w][1] + pixelscopy[h][w][2]) / 3
            for c in range(3):
                if pixels[h][w][c] != average:
                    newpixel = (2 * pixels[h][w][c]) - average
                    if newpixel > 255:
                        newpixel = 255
                    elif newpixel < 0:
                        newpixel = 0
                else:
                    newpixel = average

                pixels[h][w][c] = int(newpixel) 
    return pixels

def sincolours(pixels):
    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            for c in range(3):
                pixels[h][w][c] = int(abs(pixels[h][w][c] * math.sin((pixels[h][w][c] / 255) * (math.pi*2))))

    return pixels

def sinbrightness(pixels):
    height, width = dimensions(pixels)

    for h in range(height):
        for w in range(width):
            brightness = (pixels[h][w][0] + pixels[h][w][1] + pixels[h][w][2]) / 3
            for c in range(3):
                pixels[h][w][c] = int(abs(pixels[h][w][c] * math.sin((brightness / 255) * (math.pi * 2))))
    return pixels
