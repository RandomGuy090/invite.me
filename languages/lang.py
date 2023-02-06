import os, locale

class Language():
    def __init__(self):
        local = locale.getdefaultlocale()[0]
        if local.startswith("pl"):
            from .pl import PL_lang
            self.lang = PL_lang()
        else:
            from .en import EN_lang
            self.lang = EN_lang()