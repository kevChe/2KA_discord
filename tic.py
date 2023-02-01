from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

LEFT = 325
MID_COL = 435
RIGHT = 540
TOP = 20
MID_ROW = 125
BOTTOM = 230

position = [ [LEFT, TOP], [MID_COL, TOP], [RIGHT, TOP], 
             [LEFT, MID_ROW], [MID_COL, MID_ROW], [RIGHT, MID_ROW],
             [LEFT, BOTTOM], [MID_COL, BOTTOM], [RIGHT, BOTTOM] ]

img = Image.open('inaforehead.png')

I1 =  ImageDraw.Draw(img)

font = ImageFont.truetype('wt009.ttf', size=100)
counter = 0
for pos in position:
    text = "X"
    if counter % 2 == 0:
        text = "O"
    counter += 1
    I1.text(pos, text, font=font, fill=(0, 0, 0))

img.show()