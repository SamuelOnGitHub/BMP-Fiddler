import random

class unpackedBMP:
    def __init__(self, header, offset, pixels, width, height, byteDepth, padding):
        self.header = header
        self.offset = offset
        self.pixels = pixels
        self.width = width
        self.height = height
        self.byteDepth = byteDepth
        self.padding = padding


#Decompose source BMP into unpackedBMP, all values as int
def unpackBMP(source):
    name = source + ".bmp"
    with open(name, "rb") as image:
    
        image.seek(10)
        pixelOffset = int.from_bytes(image.read(4), "little")

        image.seek(0)
        header = int.from_bytes(image.read(pixelOffset), "little")

        image.seek(18)
        imageWidth = int.from_bytes(image.read(4),"little")

        image.seek(22)
        imageHeight = int.from_bytes(image.read(4),"little")

        image.seek(28)
        bitsPerPixel = int.from_bytes(image.read(2),"little")

        image.seek(pixelOffset)
        data = image.read()

    bytesPerPixel = int(bitsPerPixel / 8)
    padding = (4 - ((imageWidth * bytesPerPixel) % 4)) % 4

    pixels = []

    i = 0
    for y in range(imageHeight):
        pixels.append([])
        for x in range(imageWidth):
            pixels[y].append([])
            for c in range(bytesPerPixel):
                pixels[y][x].append(data[i])
                i += 1
        for p in range(padding):
            pixels[y].append(0)
            i += 1

    unpacked = unpackedBMP(header, pixelOffset, pixels, imageWidth, imageHeight, bytesPerPixel, padding)
    return unpacked

#Turn unpackedBMP object into bmp file
def craftBMP(source, unpacked):

    name = source + ".bmp"
    print("Crafted ",name)
    with open(name, "ab") as image:

        image.write(unpacked.header.to_bytes(unpacked.offset, "little"))

        i = 0
        for y in range(unpacked.height):
            for x in range(unpacked.width):
                for c in range(unpacked.byteDepth):
                    image.write(unpacked.pixels[y][x][c].to_bytes(1, "little"))
                    i += 1
            for p in range(unpacked.padding):
                image.write((0).to_bytes(1, "little"))
                i += 1
    return True

#Create blank bmp
def newBMP(source, width, height, colour):
    #file header

    bmpIdentifier = 19778
    sizeOfFile = 0 #set later
    reservedBytes = 0
    pixelOffset = 54
    
    #infoheader
    
    sizeOfInfoHeader = 40
    imageWidth = 0
    imageHeight = 0
    displayPlanes = 1
    bitsPerPixel = 24
    compressionType = 0
    bytesInPicture = 0
    horizontalResolution = 3780
    verticalResolution = 3780
    noOfColours = 0
    importantColours = 0
    
    #userinput
    
    bytesPerPixel = int(bitsPerPixel / 8)
    imageWidth = width
    imageHeight = height
    
    padding = (4 - ((imageWidth * bytesPerPixel) % 4)) % 4
    
    bytesInPicture = ((imageWidth * bytesPerPixel) + padding) * imageHeight
    sizeOfFile = bytesInPicture + 54
    
    data  = []
    for i in range(imageHeight):
        data.append([])
        for j in range(imageWidth):
            data[i].append([])
            for c in range(3):
                data[i][j].append(colour)
        for p in range(padding):
            data[i].append(0)
    
    #add to byte array
    ##file header
    picture = bytearray()
    
    picture += ( bmpIdentifier.to_bytes(2, "little") )
    picture += ( sizeOfFile.to_bytes(4, "little") )
    picture += ( reservedBytes.to_bytes(4, "little") )
    picture += ( pixelOffset.to_bytes(4, "little") )
    
    ##infoheader
    picture += ( sizeOfInfoHeader.to_bytes(4, "little") )
    picture += ( imageWidth.to_bytes(4, "little") )
    picture += ( imageHeight.to_bytes(4, "little") )
    picture += ( displayPlanes.to_bytes(2, "little") )
    picture += ( bitsPerPixel.to_bytes(2, "little") )
    picture += ( compressionType.to_bytes(4, "little") )
    picture += ( bytesInPicture.to_bytes(4, "little") )
    picture += ( horizontalResolution.to_bytes(4, "little") )
    picture += ( verticalResolution.to_bytes(4, "little") )
    picture += ( noOfColours.to_bytes(4, "little") )
    picture += ( importantColours.to_bytes(4, "little") )

    header = int.from_bytes(picture, "little")
    ##data
    
    for r in range(len(data)):
        for p in range(len(data[r])):
            for x in range(len(data[r][p])):
                picture+=( data[r][p][x].to_bytes(1, "little"))
    
    with open(source + ".bmp", "ab") as image:
        image.write(picture)
        print("Created ", source + ".bmp")
    
    unpacked = unpackedBMP(header, pixelOffset, data, imageWidth, imageHeight, bytesPerPixel, padding)
    return unpacked









