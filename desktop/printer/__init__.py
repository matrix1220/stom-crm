from .make_image import make_double_cheque_image, make_cheque_image
from .print_image import _print_image

def print_cheque(data):
    path = make_cheque_image(data)
    _print_image(path, False)


def print_double_cheque(data):
    path = make_double_cheque_image(data)
    _print_image(path)