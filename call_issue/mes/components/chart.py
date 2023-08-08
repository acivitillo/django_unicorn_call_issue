from django_unicorn.components import UnicornView
from django import forms
from django.utils.timezone import now
from django import forms
import altair as alt
from vega_datasets import data
import json
import sqlite3
import pandas
from django.utils.timezone import now

import altair as alt
import pandas


def cpk_chart(
    df: pandas.DataFrame, measurement_name: str, lsl: float, tg: float, usl: float
):
    base = (
        alt.Chart(df)
        .encode(alt.X(f"{measurement_name}:Q"))
        .properties(width=500, height=300)
    )

    density = (
        base.transform_density(
            measurement_name,
            as_=[measurement_name, "density"],
        )
        .mark_area(opacity=0.3)
        .encode(
            alt.Y("density:Q"),
        )
    )

    measurement_avg = df[measurement_name].mean()

    line_avg = (
        alt.Chart(pandas.DataFrame({"x": [measurement_avg]}))
        .mark_rule(color="brown")
        .encode(x="x")
    )
    line_lsl = (
        alt.Chart(pandas.DataFrame({"x": [lsl]})).mark_rule(color="brown").encode(x="x")
    )
    line_usl = alt.Chart(pandas.DataFrame({"x": [usl]})).mark_rule().encode(x="x")

    line_tg = (
        alt.Chart(pandas.DataFrame({"x": [usl]}))
        .mark_rule(strokeDash=[1, 1], color="orange")
        .encode(x="x")
    )

    return alt.layer(
        density, line_lsl, line_usl, line_avg, line_tg
    )  # , line_avg, line_usl, line_tg)


def get_df():
    con = sqlite3.connect("signals_lamination.sqlite")
    sql = """select reelcode_anode, signal_name, avg(signal_value) 
            from signals_lamination
            group by reelcode_anode, signal_name
            """
    df = pandas.read_sql(
        sql,
        con=con,
    )
    return df


class ChartView(UnicornView):
    chart_data = {}
    encoded_chart = None
    table_data = {}
    table_columns = []
    chart = None
    chart_clicked = False
    search = ""

    def mount(self):
        print("testing chartview")
        if isinstance(self.chart_data, pandas.DataFrame):
            self.create_chart()
        self.load_table()

    def load_table(self):
        df = get_df()
        if self.table_columns == []:
            for col in df.columns:
                self.table_columns.append(col)
        self.table_data = df.values.tolist()[1:20]

    def get_data(self, reel_code: str = ""):
        signal_name = "ttd"
        con = sqlite3.connect("signals_lamination.sqlite")
        df = pandas.read_sql(
            f"""select reelcode_anode, signal_value from signals_lamination 
                where signal_name='{signal_name}' 
                      and stack_id <> '#N/D' and reelcode_anode='{reel_code}'
            """,
            con=con,
        )
        self.chart_data = df
        self.create_chart()

    def create_chart(self):
        chart = cpk_chart(
            self.chart_data,
            measurement_name="signal_value",
            lsl=104.45,
            tg=105,
            usl=105.7,
        )
        chart.save("chart.json")

        with open("chart.json", "r") as f:
            chart = json.load(f)
        self.chart_clicked = True
        self.call("createChart", chart)

    def updated_search(self, query):
        if self.table_data == []:
            self.load_table()

        new_table_data = []
        if query != "":
            for item in self.table_data:
                if query in item[1]:
                    new_table_data.append(item)

            self.table_data = new_table_data
