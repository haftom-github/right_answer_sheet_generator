import qrcode.constants
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode

def create_qr_code(data, file_name):
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10,
        border=0
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

def create_answer_sheet(filename):
    # paddings
    padding_top = 50
    padding_left = 50
    padding = 20

    # qr_section dimentions
    qr_sec_width = 80
    qr_sec_height = 80

    # info_section dimentions
    info_sec_width = 250
    info_sec_height = 80

    # sig_section dimentions
    sig_sec_width = 80
    sig_sec_height = 80

    # answer section dimentions
    ans_sec_width = padding+qr_sec_width+info_sec_width - 2*padding
    ans_sec_height = 580

    # cautions section dimentions
    caution_sec_width = 80
    caution_sec_height = 580

    # corner marker section dimentions
    cor_sec_width = 10
    cor_sec_height = 10

    # circle dimentions
    cir_radius = 5

    # init canvas

    c = canvas.Canvas(filename, pagesize=A4)
    c.translate(0, 841.89)  # Move origin from bottom-left to top-left
    c.scale(1, -1)
    width, height = A4
    qr_file_name = "qr_code.png"
    create_qr_code("student_id, course_code, teacher_id, test_no, paper_no, date", qr_file_name)

    # draw qr section
    qr_image = ImageReader(qr_file_name)
    c.drawImage(qr_image, padding_left, padding_top, width=qr_sec_width, height=qr_sec_height)  # Adjust size as needed    x_start = 100

    # draw info section
    c.rect(
        padding_left+qr_sec_width+padding, 
        padding_top, 
        info_sec_width, 
        info_sec_height
    )

    # draw signature section
    c.rect(
        padding_left+qr_sec_width+padding*2 + info_sec_width,
        padding_top, 
        sig_sec_width,
        sig_sec_height
    )

    # draw ans section 
    c.setLineWidth(2)
    c.rect(
        padding_left + padding*2, 
        padding_top + padding + qr_sec_height, 
        ans_sec_width, 
        ans_sec_height,
    )

    c.setLineWidth(1)

    # draw causion section
    c.rect(
        padding_left + padding*3 + ans_sec_width, 
        padding_top + padding + sig_sec_height, 
        caution_sec_width, 
        caution_sec_height
    )

    # draw the corner markers
    c.rect(
        padding_left + qr_sec_width + info_sec_width +sig_sec_width + 3*padding,
        padding_top,
        cor_sec_width, 
        cor_sec_height,
        fill=1
    )
    c.rect(
        padding_left + qr_sec_width + info_sec_width +sig_sec_width + 3*padding,
        padding_top + qr_sec_height + caution_sec_height + 3*padding,
        cor_sec_width, 
        cor_sec_height,
        fill=1
    )
    c.rect(
        padding_left,
        padding_top + qr_sec_height + caution_sec_height + 3*padding,
        cor_sec_width, 
        cor_sec_height,
        fill=1
    )

    c.translate(0, 841.89)
    c.scale(1, -1)
    font_size = 10
    c.setFont("Helvetica", font_size)
    x_start = padding_left + 3*padding
    y_start = padding_top + qr_sec_height - 4 * padding + ans_sec_height 
    for i in range(25):
        c.drawString(x_start, y_start - 1 - i * padding, str(i + 1))
        for j in range(5):
            c.circle(
                x_start + padding*1.5 + (cir_radius/2) + j * (padding), 
                y_start + (cir_radius/2) - i * (padding), 
                cir_radius
            )

    x_start = padding_left + 3*padding + ans_sec_width/2
    for i in range(25):
        c.drawString(x_start, y_start -1 - i * padding, str(i + 1 + 25))
        
        #draw the circle row marker  for the circles
        c.rect(
            padding_left, 
            y_start - i * (padding),
            2*cor_sec_width,
            cir_radius,
            fill=1
        )

        for j in range(5):
            c.circle(
                x_start + padding*1.5 + (cir_radius/2) + j * (padding), 
                y_start + (cir_radius/2) - i * (padding), 
                cir_radius
            )
    

    c.translate(0, 841.89)
    c.scale(1, -1)

    # draw the circle column markers
    x_start = padding_left + 4.5 * padding
    y_start = padding_top + qr_sec_height + caution_sec_height + 2.5 * padding
    for k in range(5):
        c.rect(
            x_start + k * padding,
            y_start, 
            cir_radius, 
            2*cor_sec_width,
            fill=1
        )
        c.rect(
            x_start + k * padding + ans_sec_width/2,
            y_start, 
            cir_radius, 
            2*cor_sec_width,
            fill=1
        )
            
    c.showPage()
    c.save()

create_answer_sheet("test.pdf")