from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder


Builder.load_string('''
#:import Select2 Select2
<TheDropDown>:
    Select2:
        size_hint: None, None
        size: (165, 35)
        pos: 200, 400
        text: 'Select'
        options: root.get_options()
        on_select: root.my_call_back(self, self.text)
''')


class TheDropDown(FloatLayout):
    def __init__(self, **kwargs):
        super(TheDropDown, self).__init__(**kwargs)

    def my_call_back(self, instance, value):
        print('the value %s selected' % value)

    def get_options(self):
        options = []
        for i in range(0, 200):
            options.append('option %s' %i)
        return options


class ExampleApp(App):
    def build(self):
        widget = TheDropDown()
        return widget

    def callback(self, instance):
        print('The button <%s> is being pressed' % instance.text)


if __name__ == '__main__':
    ExampleApp().run()
