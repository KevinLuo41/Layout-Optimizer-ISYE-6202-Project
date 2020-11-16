import pandas as pd
from fbprophet import Prophet
from datetime import date, timedelta



# Generate holidays
def Sunday(years=(2018, 2025)):
    year_low, year_up = years

    def findsundays(year):
        d = date(year, 1, 1)  # January 1st
        d += timedelta(days=6 - d.weekday())  # First Sunday
        while d.year == year:
            yield d
            d += timedelta(days=7)

    sun = []
    for y in range(year_low, year_up):
        for d in findsundays(y):
            sun.append(d)

    sundays = pd.DataFrame({
        'holiday': 'Sunday',
        'ds': sun,
        'lower_window': 0,
        'upper_window': 0,
    })
    return sundays


# Picking simulator
def Simulator(artikelno=None, picking=None, freq="D", periods=365, years=(2018, 2025)):
    DateRange = pd.DataFrame({"Execution_time": pd.date_range('2018-08-31', periods=701, freq='D')})
    picking_artikel = picking[picking["Artikelno"] == artikelno]

    picking_sum = picking_artikel.groupby(["Execution_time"], as_index=0)["Amount"].sum()
    picking_ts = DateRange.merge(picking_sum, on="Execution_time", how="left")
    picking_ts["Amount"] = picking_ts["Amount"]

    if isinstance(years, tuple):
        sundays = Sunday(years)
    elif isinstance(years, int):
        sundays = Sunday((2018, years))
    else:
        raise KeyError("Parameter 'years' should be an int or tuple.")

    picking_ts.columns = ["ds", "y"]
    m = Prophet(holidays=sundays, yearly_seasonality=True, daily_seasonality=True)
    m.add_country_holidays(country_name='US')
    m.fit(picking_ts)
    future = m.make_future_dataframe(periods=365, freq='D')
    forecast = m.predict(future)

    # save forecast plot
    fig = m.plot(forecast)
    fig.savefig("forecast_%s.png" % artikelno)
    return m, forecast



