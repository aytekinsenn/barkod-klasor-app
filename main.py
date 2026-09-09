# -*- coding: utf-8 -*-
"""
Barkod -> Klasor Foto Uygulamasi
"""

import os
import re
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.utils import platform

from camera4kivy import Preview

try:
    from PIL import Image as PILImage
    from pyzbar.pyzbar import decode as zbar_decode
except Exception:
    PILImage = None
    zbar_decode = None


KV = """
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: '46dp'
            padding: '10dp', '4dp'

            Label:
                text: 'Klasor: ' + root.current_folder_name
                color: (0.25, 0.85, 1, 1) if root.has_folder else (1, 0.4, 0.4, 1)
                bold: True
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                shorten: True

        RelativeLayout:
            ScannerPreview:
                id: preview
                aspect_ratio: '16:9'

            Label:
                id: toast
                text: ''
                opacity: 0
                font_size: '20sp'
                bold: True
                color: 0, 1, 0.4, 1
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.55
                    Rectangle:
                        pos: self.x - 10, self.y - 6
                        size: self.width + 20, self.height + 12
                size_hint: None, None
                size: self.texture_size
                pos_hint: {'center_x': 0.5, 'top': 0.95}

        BoxLayout:
            size_hint_y: None
            height: '100dp'
            padding: '20dp'

            Widget:

            Button:
                id: shutter
                size_hint: None, None
                size: '72dp', '72dp'
                pos_hint: {'center_y': 0.5}
                background_normal: ''
                background_down: ''
                background_color: (1, 1, 1, 1) if root.has_folder else (0.4, 0.4, 0.4, 1)
                on_release: root.take_photo()
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0
                Label:
                    text: ''

            Widget:

            Label:
                text: root.photo_count_text
                size_hint_x: None
                width: '90dp'
                color: 1, 1, 1, 0.85
                halign: 'right'
                valign: 'middle'
                text_size: self.size
"""


def safe_folder_name(text):
    text = (text or "").strip()
    text = re.sub(r'[\\/:*?"<>|]+', '_', text)
    text = re.sub(r'\s+', '_', text)
    text = text.strip('._ ')
    if not text:
        text = "barkod_" + str(int(time.time()))
    return text[:80]


class ScannerPreview(Preview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_barcode = None

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        if zbar_decode is None or PILImage is None:
            return
        try:
