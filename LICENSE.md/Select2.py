#!/usr/bin/env python

"""
Python kivy dropdown searchable Module.
=======================================
Inspired By Javascript Select2 library, this meant to offer the same behaviour but for Python Kivy apps.

tested with kivy 1.10.1
"""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty, ColorProperty, DictProperty

__author__ = "Jafar Jabr"
__copyright__ = "Copyright 2018, Jafar Jabr"
__credits__ = ["Jafar Jabr"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jafar Jabr"
__email__ = "Jafaronly@yahoo.com"
__status__ = "Production"


class Select2(BoxLayout):
    text = StringProperty()
    options = ListProperty()
    hint_text = StringProperty('Search')
    background_color = ColorProperty((1, .3, .4, .85))
    active_background_color = ColorProperty((0, .3, .4, .85))
    color = ColorProperty((0, 0, 0, 0))
    active_color = ColorProperty((1, 1, 1, 1))
    is_select2 = BooleanProperty(True)
    dropdown = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        if 'size_hint' in kwargs:
            self.size_hint = kwargs['size_hint']
        else:
            self.size_hint = (None, None)

        if 'size' in kwargs:
            self.size = kwargs['size']
        else:
            self.size = (165, 35)
        super(Select2, self).__init__(**kwargs)
        self._prev_dd = None
        self._textinput = ti = TextInput(multiline=False, hint_text=self.hint_text, size_hint=self.size_hint, size=self.size)
        ti.bind(text=self._apply_filter)
        ti.bind(on_text_validate=self._on_enter)
        self._button = btn =Button(text=self.text, background_normal='', background_color=self.background_color,
                                size_hint=self.size_hint, size=self.size)
        btn.bind(on_release=self._on_release)
        self.add_widget(btn)
        self.register_event_type('on_select')
        if 'on_select' in kwargs:
            self.bind(on_select=kwargs.get("on_select"))

    def on_select(self, *args):
        pass

    def on_text(self, instance, value):
        self._button.text = value

    def on_dropdown(self, instance, value):
        _prev_dd = self._prev_dd
        if value is _prev_dd:
            return
        if _prev_dd:
            _prev_dd.unbind(on_dismiss=self._on_dismiss)
            _prev_dd.unbind(on_select=self._on_select)
        if value:
            value.bind(on_dismiss=self._on_dismiss)
            value.bind(on_select=self._on_select)
        self._prev_dd = value

    def _apply_filter(self, instance, text):
        if self.dropdown:
            self.dropdown.apply_filter(text)

    def _on_release(self, *largs):
        if not self.dropdown:
            return
        if self.is_select2:
            self.remove_widget(self._button)
            self.add_widget(self._textinput)
            self._textinput.focus = True
        self.dropdown.open(self)

    def _on_dismiss(self, *largs):
        if self.is_select2:
            self.remove_widget(self._textinput)
            self.add_widget(self._button)
            self._textinput.text = ''

    def _on_select(self, instance, value):
        self.text = value
        for wg in self.dropdown._widgets.keys():
            if wg == value:
                self.dropdown._widgets[wg].background_color = self.active_background_color
                self.dropdown._widgets[wg].color = self.active_color
            else:
                self.dropdown._widgets[wg].background_color = self.background_color
                self.dropdown._widgets[wg].color = self.color
        self.dispatch('on_select', value)

    def _on_enter(self, *largs):
        container = self.dropdown.container
        if container.children:
            self.dropdown.select(container.children[-1].text)
        else:
            self.dropdown.dismiss()


Builder.load_string("""
<DDButton>:
  size_hint: root.size_hint
  size: root.size
  canvas.before:
    Color:
      rgba:  .5, .5, .5, 1
    Line:
      width: 1
      rectangle: self.x, self.y, self.width, self.height
""")


class DDButton(Button):
    def __init__(self, custom_properties, **kwargs):
        self.background_normal = ''
        self.size_hint = custom_properties['size_hint']
        self.size = custom_properties['size']
        self.background_color = custom_properties['background_color']
        self.color = custom_properties['color']
        super(DDButton, self).__init__(**kwargs)


Builder.load_string('''
#:import F kivy.factory.Factory
<Select2>:
    options: root.options
    dropdown:
        F.FilteredDropDown(options=self.options, custom_properties={'size_hint': self.size_hint, 'size': self.size, 'background_color': self.background_color, 'active_background_color': self.active_background_color, 'color': self.color, 'active_color': self.active_color})
    canvas.before:
        Color:
            rgb: (0.93, 0.93, 1)
        Rectangle:
            pos: self.pos
            size: self.size
''')


class FilteredDropDown(DropDown):
    ignore_case = BooleanProperty(True)
    options = ListProperty()
    custom_properties = DictProperty()

    def __init__(self, **kwargs):
        self._needle = None
        self._order = []
        self._widgets = {}
        self.background_normal = ''
        self.custom_properties = kwargs['custom_properties']
        self.size_hint = self.custom_properties['size_hint']
        self.size = self.custom_properties['size']
        self.background_color = self.custom_properties['background_color']
        self.active_background_color = self.custom_properties['active_background_color']
        self.color = self.custom_properties['color']
        self.active_color = self.custom_properties['active_color']
        super(FilteredDropDown, self).__init__(**kwargs)

    def on_options(self, instance, values):
        _order = self._order
        _widgets = self._widgets
        changed = False
        for txt in values:
            if txt not in _widgets:
                _widgets[txt] = btn = DDButton(self.custom_properties, text=txt, background_normal = '', background_color=self.background_color, color=self.color, size_hint= self.size_hint, size=self.size)
                btn.bind(on_release=self.select_option)
                _order.append(txt)
                changed = True
        for txt in _order[:]:
            if txt not in values:
                _order.remove(txt)
                del _widgets[txt]
                changed = True
        if changed:
            self.apply_filter(self._needle)

    def select_option(self, instance):
        self.select(instance.text)

    def apply_filter(self, needle):
        self._needle = needle
        self.clear_widgets()
        _widgets = self._widgets
        add_widget = self.add_widget
        ign = self.ignore_case
        _lcn = needle and needle.lower()
        for haystack in self._order:
            _lch = haystack.lower()
            if not needle or ((ign and _lcn in _lch) or
                         (not ign and needle in haystack)):
                add_widget(_widgets[haystack])
