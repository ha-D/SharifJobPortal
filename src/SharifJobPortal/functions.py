def to_persian_num(num, len=2):
    s = num.__str__()
    while s.__len__() < len:
        s = '0' + s
    ps = u''
    for c in s:
        ps += unichr(ord(c) + 1776 - 48)
    return ps