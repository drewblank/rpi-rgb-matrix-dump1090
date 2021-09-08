from PIL import Image
from PIL import ImageDraw
import schedule
import time
import json
import requests
#from rgbmatrix import RGBMatrix, RGBMatrixOptions #real 
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics #test 


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
matrix = RGBMatrix(options = options)




def drawimage(path):
    image = Image.open(path)
    image.thumbnail((25, 25))
    matrix.SetImage(image.convert('RGB'),32,5)

def job():
    # Clear matrix
    matrix.Clear()
    dump1090 = 0

#        flight_number = dump1090.name() 

    flight_number = 'AAL4567'
    altitude = 35000
    speed = 150 
    longitude = 42.4234
    latitude = 86.2345


    airline = flight_number[0:3]

    #Draw Airline Icon
    if(airline == 'AAL'):
        drawimage('icons/' + '01d' + '.png')
    if(airline == 'UAL'):
        drawimage('icons/' + 'ual' + '.png')
    if(airline == 'DAL'):
        drawimage('icons/' + 'dal' + '.png')
    if(airline == 'SWA'):
        drawimage('icons/' + 'swa' + '.png')
    if(airline == 'FDX'):
        drawimage('icons/' + 'fdx' + '.png')
    if(airline == 'UPS'):
        drawimage('icons/' + 'ups' + '.png')


    font = graphics.Font()
    font.LoadFont("../../rpi-rgb-led-matrix/fonts/4x6.bdf")
    textColor = graphics.Color(255, 255, 255)

    start_pos = 20

    line1 = flight_number
    graphics.DrawText(matrix, font, 1, start_pos, textColor, line1)
    line2 = 'ALT: ' + str(altitude) + ' ft'
    graphics.DrawText(matrix, font, 1, start_pos + 7, textColor, line2)
    line3 = 'SPD: ' + str(speed) + ' knts'
    graphics.DrawText(matrix, font, 1, start_pos + 14, textColor, line3)
    line4 = 'LAT: ' + str(latitude) 
    graphics.DrawText(matrix, font, 1, start_pos + 21, textColor, line4)
    line5 = 'LON: ' + str(longitude) 
    graphics.DrawText(matrix, font, 1, start_pos + 28, textColor, line5)


job()
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)