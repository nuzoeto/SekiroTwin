# WhiterKang Bot
# Copyright (C) 2022 Davi
#
# This file is a part of < https://github.com/DaviTudoPlugins1234/WhiterKang/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/DaviTudoPlugins1234/WhiterKang/blob/master/LICENSE/>.

## WhiterKang Decorators

def input_str(message) -> str:
    return " ".join(message.text.split()[1:])
