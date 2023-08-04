from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql import BrotherQLRaster
from brother_ql.devicedependent import label_type_specs


LABEL_SIZE = '62x100'
MODEL = "QL-570"
BACKEND = "linux_kernel"
PRINTER = "/dev/usb/lp0"
# BACKEND = "pyusb"
# PRINTER = "usb://0x04f9:0x2028"


def draw_label(name, description, date, serial=None):
    # Draw horizontally and rotate later
    dots = label_type_specs[LABEL_SIZE]["dots_printable"]
    image = Image.new("RGB", (dots[1], dots[0]), "white")
    draw = ImageDraw.Draw(image)

    font_small = ImageFont.truetype("DejaVuSansMono.ttf", size=40)
    font = ImageFont.truetype("DejaVuSansMono.ttf", size=60)
    font_medium = ImageFont.truetype("DejaVuSansMono.ttf", size=80)
    font_large = ImageFont.truetype("DejaVuSansMono.ttf", size=150)

    draw.text((dots[1]/2, 10), description, font=font_large, fill="black", anchor="ma")

    
    draw.text((dots[1]/2, 200), "Do not hack until", font=font, fill="black", anchor="ma")
    draw.text((dots[1]/2, 280), date.strftime("%d %b %Y"), font=font_large, fill="black", anchor="ma")

    draw.text((10, 450), "Owner:", font=font, fill="black")
    draw.text((10, 530), name, font=font_medium, fill="black")

    if serial is not None:
        serial_text = f"{serial:08d}"
        draw.text((dots[1]-10, dots[0]-10), serial_text, font=font_small, fill="black", anchor="rd")

    return image


def send_to_printer(image):
    print("printing label")

    qlr = BrotherQLRaster(MODEL)
    qlr.exception_on_warning = True
    instructions = convert(
        qlr=qlr, 
        images=[image],    #  Takes a list of file names or PIL objects.
        label=LABEL_SIZE, 
        rotate='90',    # 'Auto', '0', '90', '270'
        threshold=70.0,    # Black and white threshold in percent.
        dither=False, 
        compress=False, 
        red=False,    # Only True if using Red/Black 62 mm label tape.
        dpi_600=False, 
        hq=True,    # False for low quality.
        cut=True
    )

    send(instructions=instructions, printer_identifier=PRINTER, backend_identifier=BACKEND, blocking=True)
    print("printing done")


def print_project_box_label(name=None, serial=None):
    now = date.today()
    name = name or "___________________"
    expiry = now + timedelta(days=30*6) # Roughly 6 months
    description="Project box"
    image = draw_label(name, description, expiry, serial)
    send_to_printer(image)


def print_short_stay_label(name=None, serial=None):
    now = date.today()
    name = name or "___________________"
    expiry = now + timedelta(days=30) # Roughly 1 month
    description="Short stay"
    image = draw_label(name, description, expiry, serial)
    send_to_printer(image)
