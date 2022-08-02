#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'tongbin'

import re
import rpm


class BOOLEAN(int):
    def __new__(cls, x):
        if str(x).lower() in {'1', 'true', '0x1'}:
            x = True
        elif str(x).lower() in {'0', 'false', '0x0'}:
            x = False
        else:
            x = bool(x)
        return super(BOOLEAN, cls).__new__(cls, x)


class IPV4_ADDRESS(object):
    def __init__(self, ip):
        if isinstance(ip, IPV4_ADDRESS):
            self._x = ip._x
            return
        regex_ip_address = r'\b([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})/?([0-9]{1,2})?\b'

        check = lambda a: None if a is None else int(a)
        reg_res = re.match(regex_ip_address, ip)
        if reg_res is None or any(int(reg_res[i]) > 255 for i in range(1, 5)):
            raise Exception('Type Error: ipv4_address')
        if reg_res[5] and int(reg_res[5]) > 32:
            raise Exception('Type Error: ipv4_address')
        self._x = tuple(check(reg_res[i]) for i in range(1, 6))

    def __cmp__(self, x):
        if not isinstance(x, IPV4_ADDRESS):
            x = IPV4_ADDRESS(x)
        if self._x[-1] != x._x[-1]:
            raise Exception('ipv4_address prefix is different')
        return next(
            (self._x[i] - x._x[i] for i in range(4) if self._x[i] != x._x[i]), 0
        )


class EVR_STRING(object):
    def __init__(self, x):
        if isinstance(x, EVR_STRING):
            self._x = x._x
            return
        regex_evr = r'([A-Za-z0-9\.]+):([A-Za-z0-9\.]+)-([A-Za-z0-9\.]+)'
        if reg_res := re.search(regex_evr, x):
            self._x = tuple(reg_res[i] for i in range(1, 4))
        else:
            raise Exception('Type Error: evr_string')

    def __cmp__(self, evr):
        if not isinstance(evr, EVR_STRING):
            evr = EVR_STRING(evr)
        return rpm.labelCompare(self._x, evr._x)


class INT(int):
    def __new__(cls, x):
        if isinstance(x, basestring) and x.startswith('0x'):
            x = int(x, 16)
        return super(INT, cls).__new__(cls, x)

STRING = str

FLOAT = float