from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import datetime
from reportlab.pdfgen import canvas
import subprocess

img = Image.open('123123.png')
img.save('123.png', format='png')
x = datetime.datetime.now()
hh = x.strftime('%x')


def create_pdf(filename, printer_info_list):
    c = canvas.Canvas(filename, pagesize=landscape(letter))
    pdfmetrics.registerFont(TTFont('arial-unicode-ms', 'arial-unicode-ms.ttf'))

    c.setFont('arial-unicode-ms', 9)
    c.rect(130, 500, width=130, height=80, stroke=1, fill=0)
    c.drawImage('123.png', 140, 510, width=100, height=50)
    c.rect(260, 540, width=400, height=40, stroke=1, fill=0)
    c.drawString(370, 560, 'xxx')
    c.drawString(455, 550, 'xxx')

    c.rect(260, 500, width=400, height=40, stroke=1, fill=0)
    c.setFont('arial-unicode-ms', 12)
    c.drawString(345, 522, 'xxx')
    c.drawString(310, 508, 'xxx')

    c.rect(130, 480, width=127, height=15, stroke=1, fill=0)
    c.rect(263, 480, width=127, height=15, stroke=1, fill=0)
    c.rect(398, 480, width=127, height=15, stroke=1, fill=0)
    c.rect(533, 480, width=127, height=15, stroke=1, fill=0)

    c.setFont('arial-unicode-ms', 7.4)
    c.drawString(143, 485, 'xxx')
    c.drawString(310, 485, 'Revision:00')
    c.drawString(430, 485, 'Rev.Date:' + hh)
    c.drawString(585, 485, 'Page 1/1')

    c.setFont('arial-unicode-ms', 10)
    c.drawString(81, 460, 'xxx:' + hh)
    c.drawString(180, 460, 'xxx')

    c.setFillColorRGB(36, 36, 36)  # choose fill colour
    c.rect(50, 400, width=20, height=45, stroke=1, fill=1)
    c.rect(70, 400, width=160, height=45, stroke=1, fill=1)
    c.rect(230, 400, width=170, height=45, stroke=1, fill=1)
    c.rect(400, 400, width=180, height=45, stroke=1, fill=1)
    c.rect(580, 400, width=170, height=45, stroke=1, fill=1)

    #drawStrings....


    c.setFillColorRGB(0, 0, 0)  # choose fill colour
    c.drawString(55, 420, '№')

    # information
    number = 1
    y_pos = 375
    start_index = 0
    end_index = 26
    replacement = 'Refill '
    while number <= len(printer_info_list):
        c.setFillColorRGB(36, 36, 36)  # choose fill colour
        c.rect(50, y_pos, width=20, height=25, stroke=1, fill=1)
        c.rect(70, y_pos, width=160, height=25, stroke=1, fill=1)
        c.rect(230, y_pos, width=170, height=25, stroke=1, fill=1)
        c.rect(400, y_pos, width=180, height=25, stroke=1, fill=1)
        c.rect(580, y_pos, width=170, height=25, stroke=1, fill=1)

        c.setFillColorRGB(0, 0, 0)  # choose fill colour
        c.setFont('arial-unicode-ms', 9)
        c.drawString(55, y_pos+10, str(number))
        c.drawString(75, y_pos+10, '{}'.format(printer_info_list[number-1][0]))
        c.drawString(260, y_pos+10, '{}'.format(printer_info_list[number-1][1]))
        c.drawString(410, y_pos+10, '{}'.format(printer_info_list[number - 1][2][:start_index]+replacement+printer_info_list[number - 1][2][:end_index]
))
        c.drawString(590, y_pos+10, '{}'.format(printer_info_list[number-1][3]))

        number += 1
        y_pos -= 25

    c.setFont('arial-unicode-ms', 12)
    c.drawString(41, 220, 'xxx')
    c.drawString(41, 190, 'xxx')

    c.setFont('arial-unicode-ms', 9)
    c.line(290, 190, 190, 190)
    c.drawString(190, 180, 'xxx, xxx')

    c.line(310, 190, 410, 190)
    c.drawString(310, 180, 'xxx')

    c.line(430, 190, 530, 190)
    c.drawString(430, 180, 'xxx')

    c.setFont('arial-unicode-ms', 12)

    c.drawString(41, 120, 'xxx')
    c.drawString(41, 90, 'xxx')

    c.line(290, 90, 190, 90)

    c.line(310, 90, 410, 90)

    c.line(430, 90, 530, 90)

    c.save()


def print_pdf(filename, printer_name):
    subprocess.run(['lp', '-d', printer_name, filename], check=True)
