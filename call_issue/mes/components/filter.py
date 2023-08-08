from django_unicorn.components import UnicornView


class FilterView(UnicornView):
    search = ""

    def updated_search(self, query):
        self.parent.load_table()

        out_data = []
        if query != "":
            for item in self.parent.data:
                print(item, query)
                if query in item[2]:
                    out_data.append(item)

            self.parent.data = out_data
