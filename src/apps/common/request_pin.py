from trezor import res, ui
from trezor.messages import PinMatrixRequestType
from trezor.ui.confirm import CONFIRMED, ConfirmDialog
from trezor.ui.pin import PinMatrix


class PinCancelled(Exception):
    pass


@ui.layout
async def request_pin(code: int = None, cancellable: bool = True) -> str:

    def onchange():
        c = dialog.cancel
        if matrix.pin:
            back = res.load(ui.ICON_BACK)
            if c.content is not back:
                c.normal_style = ui.BTN_CLEAR['normal']
                c.content = back
                c.taint()
                c.render()
        else:
            lock = res.load(ui.ICON_LOCK)
            if c.content is not lock and cancellable:
                c.normal_style = ui.BTN_CANCEL['normal']
                c.content = lock
                c.taint()
                c.render()

    label = _get_label(code)
    matrix = PinMatrix(label, with_zero=True)
    matrix.onchange = onchange
    dialog = ConfirmDialog(matrix)
    dialog.cancel.area = ui.grid(12)
    dialog.confirm.area = ui.grid(14)
    matrix.onchange()
    if not cancellable:
        dialog.cancel.content = ''
        dialog.cancel.disable()

    while True:
        result = await dialog
        if result == CONFIRMED:
            return matrix.pin
        elif result != CONFIRMED and matrix.pin:
            matrix.change('')
            continue
        else:
            raise PinCancelled()


def _get_label(code: int):
    if code is None:
        code = PinMatrixRequestType.Current
    if code == PinMatrixRequestType.NewFirst:
        label = 'Enter new PIN'
    elif code == PinMatrixRequestType.NewSecond:
        label = 'Re-enter new PIN'
    else:  # PinMatrixRequestType.Current
        label = 'Enter your PIN'
    return label
