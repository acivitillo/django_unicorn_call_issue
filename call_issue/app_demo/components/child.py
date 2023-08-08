from django_unicorn.components import UnicornView


class ChildView(UnicornView):

    def mount(self):
            unicorn_var = "Unicorn component is mounted"
            self.call("unicornCall", unicorn_var)

    def calljs(self):
        unicorn_var = "call from Unicorn!"
        print("called")
        self.call("unicornCall", unicorn_var)
