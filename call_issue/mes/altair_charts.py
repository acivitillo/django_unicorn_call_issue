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
