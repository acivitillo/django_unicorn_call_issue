from django_unicorn.components import UnicornView
import sqlite3
import pandas


class PageView(UnicornView):
    status = ""
    updated_status = False
    data = {}

    def get_data(self, reel_code: str = ""):
        signal_name = "ttd"
        con = sqlite3.connect("signals_lamination.sqlite")
        df = pandas.read_sql(
            f"""select * from signals_lamination 
                where signal_name='{signal_name}' 
                      and stack_id <> '#N/D' and reelcode_anode='{reel_code}'
            """,
            con=con,
        )
        self.data = df

        for child in self.children:
            if hasattr(child, "chart_data"):
                child.create_chart()
                child.component_key = 123
                child.render(init_js=True)
                with open("calls.json", "w") as f:
                    f.write(str(child.calls))
