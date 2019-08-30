# -*- coding:utf-8 -*-
from imagekit.specs import ImageSpec
from .resizes import *


class Thumb(ImageSpec):
    processors = [ResizeThumb]


class Thumb300(Resize):
    processors = [ResizeThumb300]


class Thumb500(Resize):
    processors = [ResizeThumb500]


class Display(ImageSpec):
    processors = [ResizeDisplay]


class Img80x56(ImageSpec):
    processors = [Resize80x56]


class Img216x150(ImageSpec):
    processors = [ResizeImg216x150]


class Img256x192(ImageSpec):
    processors = [ResizeImg256x192]


class Img288x200(ImageSpec):
    processors = [ResizeImg288x200]


class Img288x216(ImageSpec):
    processors = [ResizeImg288x216]


class Img384x264(ImageSpec):
    processors = [ResizeImg384x264]


class Img384x288(ImageSpec):
    processors = [ResizeImg384x288]


class ImgAutox408(ImageSpec):
    processors = [ResizeImgAutox408]

