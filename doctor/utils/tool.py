import binascii
from xml.etree.ElementTree import Element, tostring, parse
import io
import os


def dict2xml(tag, d):
    def _f(_tag, _d):
        _tag = str(_tag)
        elem = Element(_tag)
        for k, v in _d.items():
            if isinstance(v, dict):
                child = _f(k, v)
                elem.append(child)
            elif isinstance(v, list):
                for sub_v in v:
                    child = _f(k, sub_v)
                    elem.append(child)
            else:
                if v is None:
                    v = ''
                child = Element(str(k))
                child.text = str(v)
                elem.append(child)
        return elem

    e = _f(tag, d)
    s = tostring(e)
    return s


def xml2dict(s):
    root = parse(io.BytesIO(s)).getroot()

    def _f(e):
        children = e.getchildren()
        if children:
            _d = {}
            for child in children:
                v = _f(child)
                if child.tag in _d:
                    if isinstance(_d[child.tag], list):
                        _d[child.tag].append(v)
                    else:
                        _d[child.tag] = [_d[child.tag], v]
                else:
                    _d[child.tag] = v
            return _d
        else:
            return e.text

    d = _f(root)
    return d


def gen_nonce_str():
    return binascii.b2a_hex(os.urandom(16)).decode('utf-8')