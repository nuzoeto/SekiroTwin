class Fonts:
    ARIAL = 'megumin/plugins/misc/fonts/arial-unicode-ms.ttf'
    OPEN_BOLD = 'megumin/plugins/misc/fonts/OpenSans-Bold.ttf'
    OPEN_SANS = 'megumin/plugins/misc/fonts/OpenSans-Regular.ttf'
    POPPINS = 'megumin/plugins/misc/fonts/Poppins-SemiBold.ttf'

def truncate(text, font, limit):
    edited = True if font.getsize(text)[0] > limit else False
    while font.getsize(text)[0] > limit:
        text = text[:-1]
    if edited:
        return(text.strip() + '..')
    else:
        return(text.strip())


def checkUnicode(text):
    return text == str(text.encode('utf-8'))[2:-1]
