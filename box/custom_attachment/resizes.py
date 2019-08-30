# -*- coding:utf-8 -*-
from imagekit.processors import Resize


class Resize80x56(Resize):
    width = 80
    height = 56
    crop = True


class ResizeThumb(Resize):
    width = 172
    height = 172


class ResizeThumb300(Resize):
    height = 300


class ResizeThumb500(Resize):
    height = 500


class ResizeDisplay(Resize):
    width = 1200
    height = 900


class ResizeImg216x150(Resize):
    width = 216
    height = 150
    crop = True


class ResizeImg256x192(Resize):
    width = 256
    height = 192


class ResizeImg288x200(Resize):
    width = 288
    height = 200
    crop = True


class ResizeImg288x216(Resize):
    width = 288
    height = 216


class ResizeImg384x264(Resize):
    width = 384
    height = 264
    crop = True


class ResizeImg384x288(Resize):
    width = 384
    height = 288


class ResizeImgAutox408(Resize):
    height = 408
    