from .make_image import make_double_cheque_image, make_cheque_image
from .generate import _print_cheque

def print_cheque(payee, amount, date, doctor):
    path = make_cheque_image(payee, amount, date, doctor)
    _print_cheque(path, False)


def print_double_cheque(payee, amount, date, doctor):
    path = make_double_cheque_image(payee, amount, date, doctor)
    _print_cheque(path)