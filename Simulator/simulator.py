import pandas as pd
from fbprophet import Prophet
from datetime import date, timedelta
from DataLoader import *
from dateutil.relativedelta import relativedelta


# Generate holidays
def Sunday(years=(2018, 2025)):
    year_low, year_up = years
    year_up+=1
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
def Simulator(artikelno=None, hist_periods=None, freq="D", fore_periods=365):
    data_path = "../../WHAI-provided_data/"
    p_path = data_path + "02_picking-activity_K1.csv"
    i_path = data_path + "04_Item-Master_K1.xlsx"
    picking = read_picking(p_path, i_path)
    first_day = picking["Execution_time"].min()
    last_day = picking["Execution_time"].max()

    if hist_periods:
        hist = hist_periods
    else:
        hist = (picking["Execution_time"].max() - picking["Execution_time"].min()).days + 1

    DateRange = pd.DataFrame({"Execution_time": pd.date_range(end=last_day, periods=hist, freq="D")})
    picking_artikel = picking[picking["Artikelno"] == artikelno]

    picking_sum = picking_artikel.groupby(["Execution_time"], as_index=0)["Amount"].sum()
    picking_ts = DateRange.merge(picking_sum, on="Execution_time", how="left")
    # picking_ts["Amount"] = picking_ts["Amount"]


    if freq == "D":
        sundays = Sunday((first_day.year, (last_day+relativedelta(days=fore_periods)).year))
    elif freq == "M":
        sundays = Sunday((first_day.year, (last_day + relativedelta(months=fore_periods)).year))
    elif freq == "Y":
        sundays = Sunday((first_day.year, (last_day + relativedelta(years=fore_periods)).year))
    # print(sundays)

    picking_ts.columns = ["ds", "y"]
    m = Prophet(holidays=sundays, yearly_seasonality=True, daily_seasonality=True)
    m.add_country_holidays(country_name='US')
    m.fit(picking_ts)
    future = m.make_future_dataframe(periods=fore_periods, freq=freq)
    forecast = m.predict(future)

    # save forecast plot
    fig = m.plot(forecast)
    fig_name = "forecast_%s.png" % artikelno
    fig.savefig("../output/forecast_imgs/"+fig_name)
    fig.savefig("../web-app/static/imgs/forecast_ouput/" + fig_name)
    return fig_name, m, forecast


if __name__ == '__main__':
    Simulator(55)
