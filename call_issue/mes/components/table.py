from django_unicorn.components import UnicornView
from django import forms
from django.utils.timezone import now
from django import forms
import altair as alt
from vega_datasets import data
import json
import sqlite3
import pandas
import sqlite3


def get_df():
    con = sqlite3.connect("signals_lamination.sqlite")
    sql = """select stack_id, reelcode_anode, signal_name, signal_value 
            from signals_lamination"""
    df = pandas.read_sql(
        sql,
        con=con,
    )
    return df


class TableView(UnicornView):
    columns = []
    data = []

    def get_data(self, reel_code: str):
        self.parent.get_data(reel_code)

    def mount(self):
        if self.columns != []:
            self.columns = []
        self.load_table()

    def load_table(self):
        df = get_df()
        for col in df.columns:
            self.columns.append(col)
        self.data = df.values.tolist()[1:20]

    def update_status(self):
        print("1333")
        self.counter += 1
        self.parent.parent_status = "Clicked!"
