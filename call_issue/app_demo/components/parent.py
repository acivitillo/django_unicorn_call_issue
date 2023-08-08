from django_unicorn.components import UnicornView


class ParentView(UnicornView):
    counter = 0

    def add(self):
        self.counter += 1
