# -*- coding: utf-8 -*-
from __future__ import absolute_import

import ctypes
import os
import distutils.sysconfig as sysconfig
import inspect
import evdev
from uinput.ev import *

_UINPUT_MAX_NAME_SIZE = 80
_ABS_CNT = ABS_MAX[1] + 1

class _struct_input_id(ctypes.Structure):
    _fields_ = [("bustype", ctypes.c_int16),
                ("vendor", ctypes.c_int16),
                ("product", ctypes.c_int16),
                ("version", ctypes.c_int16),
                ]

class _struct_uinput_user_dev(ctypes.Structure):
    _fields_ = [("name", ctypes.c_char * _UINPUT_MAX_NAME_SIZE),
                ("id", _struct_input_id),
                ("ff_effects_max", ctypes.c_int),
                ("absmax", ctypes.c_int * _ABS_CNT),
                ("absmin", ctypes.c_int * _ABS_CNT),
                ("absfuzz", ctypes.c_int * _ABS_CNT),
                ("absflat", ctypes.c_int * _ABS_CNT),
                ]

def _error_handler(result, fn, args):
    if result == -1:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code))
    elif result < -1:
        raise RuntimeError("unexpected return value: %s" % result)
    return result

_libsuinput_path = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(evdev)), "..", "_libsuinput" + sysconfig.get_config_var("SO")))
_libsuinput = ctypes.CDLL(_libsuinput_path, use_errno=True)
_libsuinput.suinput_open.errcheck = _error_handler
_libsuinput.suinput_enable_event.errcheck = _error_handler
_libsuinput.suinput_create.errcheck = _error_handler
_libsuinput.suinput_write_event.errcheck = _error_handler
_libsuinput.suinput_emit.errcheck = _error_handler
_libsuinput.suinput_emit_click.errcheck = _error_handler
_libsuinput.suinput_emit_combo.errcheck = _error_handler
_libsuinput.suinput_syn.errcheck = _error_handler
_libsuinput.suinput_destroy.errcheck = _error_handler

_CHAR_MAP = {
    "a":  KEY_A,
    "b":  KEY_B,
    "c":  KEY_C,
    "d":  KEY_D,
    "e":  KEY_E,
    "f":  KEY_F,
    "g":  KEY_G,
    "h":  KEY_H,
    "i":  KEY_I,
    "j":  KEY_J,
    "k":  KEY_K,
    "l":  KEY_L,
    "m":  KEY_M,
    "n":  KEY_N,
    "o":  KEY_O,
    "p":  KEY_P,
    "q":  KEY_Q,
    "r":  KEY_R,
    "s":  KEY_S,
    "t":  KEY_T,
    "u":  KEY_U,
    "v":  KEY_V,
    "w":  KEY_W,
    "x":  KEY_X,
    "y":  KEY_Y,
    "z":  KEY_Z,
    "1":  KEY_1,
    "2":  KEY_2,
    "3":  KEY_3,
    "4":  KEY_4,
    "5":  KEY_5,
    "6":  KEY_6,
    "7":  KEY_7,
    "8":  KEY_8,
    "9":  KEY_9,
    "0":  KEY_0,
    "\t": KEY_TAB,
    "\n": KEY_ENTER,
    " ":  KEY_SPACE,
    ".":  KEY_DOT,
    ",":  KEY_COMMA,
    "/":  KEY_SLASH,
    "\\": KEY_BACKSLASH,
    }

def _chars_to_events(chars):
    events = []
    for char in chars:
        events.append(_CHAR_MAP.get(char))
    return events

class Device(object):

    """Device handle.

    `events`  - a sequence of event capability descriptors

    `name`    - name displayed in /proc/bus/input/devices

    `bustype` - bus type identifier, see linux/input.h

    `vendor`  - vendor identifier

    `product` - product identifier

    `version` - version identifier
    """

    def __init__(self, events, name="python-uinput",
                 bustype=0, vendor=0, product=0, version=0):
        self.__events = events
        self.__uinput_fd = -1
        self.__name = name.encode()

        user_dev = _struct_uinput_user_dev(self.__name)
        user_dev.id.bustype = bustype
        user_dev.id.vendor = vendor
        user_dev.id.product = product
        user_dev.id.version = version
        self.__uinput_fd = _libsuinput.suinput_open()
        for ev_spec in self.__events:
            ev_type, ev_code = ev_spec[:2]
            _libsuinput.suinput_enable_event(self.__uinput_fd, ev_type, ev_code)
            if len(ev_spec) > 2:
                absmin, absmax, absfuzz, absflat = ev_spec[2:]
                user_dev.absmin[ev_code] = absmin
                user_dev.absmax[ev_code] = absmax
                user_dev.absfuzz[ev_code] = absfuzz
                user_dev.absflat[ev_code] = absflat

        _libsuinput.suinput_create(self.__uinput_fd, ctypes.pointer(user_dev))

    def syn(self):
        """Fire all emitted events.

        All emitted events will be placed in a certain kind of event
        queue. Queued events will be fired when this method is
        called. This makes it possible to emit "atomic" events. For
        example sending REL_X and REL_Y atomically requires to emit
        first event without syn and the second with syn::

          d.emit(uinput.REL_X, 1, syn=False)
          d.emit(uinput.REL_Y, 1)

        The call above appears as a single (+1, +1) event.
        """

        _libsuinput.suinput_syn(self.__uinput_fd)

    def emit(self, event, value, syn=True):
        """Emit event.

        `event` - event identifier, for example uinput.REL_X

        `value` - value of the event
           KEY/BTN      : 1 (key-press) or 0 (key-release)
           REL          : integer value of the relative change
           ABS          : integer value in the range of min and max values

        `syn` - If True, Device.syn(self) will be called before return.
        """

        ev_type, ev_code = event
        _libsuinput.suinput_emit(self.__uinput_fd, ev_type, ev_code, value)
        if syn:
            self.syn()

    def emit_click(self, event, syn=True):
        """Emit click event. Only KEY and BTN events are accepted,
        otherwise ValueError is raised.

        `event` - event identifier, for example uinput.KEY_A

        `syn` - if True, Device.syn(self) is called before returning.
        """
        ev_type, ev_code = event
        if ev_type != 0x01:
            raise ValueError("event must be of type KEY or BTN")
        _libsuinput.suinput_emit_click(self.__uinput_fd, ev_code)
        if syn:
            self.syn()

    def emit_combo(self, events, syn=True):
        """Emit key combination. Only KEY and BTN events are accepted,
        otherwise ValueError is raised.

        `events` - a sequence of event identifiers, for example
        (uinput.KEY_LEFTCTRL, uinput.KEY_LEFTALT, uinput.KEY_DELETE).

        `syn` if True, Device.syn(self) is called before returning.
        """
        ev_types, ev_codes = zip(*events)
        if not all([ev_type == 0x01 for ev_type in ev_types]):
            raise ValueError("all events must be of type KEY or BTN")

        arrtype = ctypes.c_uint16 * len(events)
        _libsuinput.suinput_emit_combo(self.__uinput_fd, arrtype(*ev_codes), len(events))
        if syn:
            self.syn()

    def __del__(self):
        if self.__uinput_fd >= 0:
            _libsuinput.suinput_destroy(self.__uinput_fd)
