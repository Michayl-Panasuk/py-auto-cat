def number(self, event):
    v = event.char
    try:
        v = int(v)
    except ValueError:
        if v != "\x08" and v != "":
            return "break"
