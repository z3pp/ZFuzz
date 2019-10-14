import re

from zfuzz.cli import ZFuzzCLI


def replace_kv_dict(d, keyword, string):

    """ Replace each key and value of a dict

        :param d: The dict to replace
        :param keyword: The keyword to replace in the dict
        :param string: The string that will replace the keyword
    """

    for k, v in d.items():
        new_k = k.replace(keyword, string)
        new_v = v.replace(keyword, string)
        d[new_k] = new_v
        if new_k != k:
            del d[k]
    return d


def get_code_color(code):

    """ Return http code colors

        :param code: HTTP Status code
        :returns: HTTP Code color
    """

    colors = ZFuzzCLI()

    if code in range(200, 299):
        color = colors.green
    elif code in range(300, 399):
        color = colors.blue
    else:
        color = colors.red
    return color


def is_matching(code, hc, sc, content, lenght, hs, ss, hr, sr, hl, sl):

    """ Determinate if the given response match the given filters

        :param code: HTTP Status code
        :param hc: HTTP Code(s) to hide
        :param sc: HTTP Code(s) to show
        :param content: Response content
        :param hs: Hide response with hs
        :param ss: Show response with ss
        :param hr: Hide reponse with hr (regex)
        :param sr: Show reponse with sr (regex)

        :returns: True/False, depending of the filter
    """

    ret = True

    if len(sc) > 0:
        ret = ret if code in sc else False
    if len(hc) > 0:
        ret = False if code in hc else ret

    if hs is not None:
        ret = False if hs in content else ret
    if ss is not None:
        ret = ret if ss in content else False

    if hr is not None:
        ret = False if re.match(hr, content) else ret
    if sr is not None:
        ret = ret if re.match(sr, content) else False

    if hl is not None:
        ret = False if hl == lenght else ret
    if sl is not None:
        ret = ret if sl == lenght else False
    return ret
