from django_unicorn.components import UnicornView
from django import forms
from django.utils.timezone import now
from django import forms
import altair as alt
from vega_datasets import data
import json
import sqlite3
import pandas

from .altair_charts import cpk_chart


class SimpletestView(UnicornView):
    counter = 0

    def update_status(self):
        print("1333")
        self.counter += 1
        self.parent.parent_status = "Clicked!"
