import numpy as np
import pandas as pd
from DataLoader import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def ABC(split_method="quantile", time_scale=None, ratio=(0.2, 0.3, 0.5), value=(0.7, 0.25, 0.05),data=None):
    r'''
    ABC analysis: Split the artikels to 3 different critical type based on chosen method.

    Parameters:
    -------------
    data: pd.DataFrame, default=picking
        file path of picking/retrieval data
    split_method: str: {"quantile", "value", "moves"}, default= "quantile"
        file path of CLSLAB_path
    time_scale: int, default=None
        # of past months of ABC analysis, None: all history data
    ratio: split ratio, split by quantile of the data
    value: split value, split by values of the data
    '''

    if data is None:
        data_path = "../../WHAI-provided_data/"
        p_path = data_path + "02_picking-activity_K1.csv"
        data = pd.read_csv(p_path)
        data["Execution_time"] = pd.to_datetime(data["Execution_time"])

    if time_scale:
        latest_date = data['Execution_time'].iloc[-1]
        start_date = latest_date - pd.DateOffset(months=time_scale) - pd.offsets.MonthBegin(1)
        data = data[data['Execution_time'] >= start_date]
    #     return data, None,None,None
    picking_sum = data.groupby(["Artikelno"], as_index=0)["Amount"].sum()
    picking_sort = picking_sum.sort_values(by="Amount", ascending=False).reset_index(drop=True)

    N = len(picking_sort)
    All = picking_sort.copy()
    rA, rB, rC = ratio
    vA, vB, vC = value

    if split_method == "quantile":
        A, B, C = np.split(picking_sort, [int(rA * N), int((rA + rB) * N)])

    elif split_method == "value":
        picking_value = picking_sort.copy()
        Total = picking_value.sum()["Amount"]

        picking_value["Cumsum"] = picking_value["Amount"].cumsum()
        A = picking_value[picking_value["Cumsum"] <= Total * vA]
        B = picking_value[(picking_value["Cumsum"] > Total * vA) & (picking_value["Cumsum"] <= Total * vB + Total * vA)]
        C = picking_value[picking_value["Cumsum"] > Total * vB + Total * vA]

        A =A[["Artikelno","Amount"]]
        B =B[["Artikelno","Amount"]]
        C =C[["Artikelno","Amount"]]
        All = All[["Artikelno","Amount"]]

    elif split_method == "moves":
        moves = data.groupby(["Artikelno"], as_index=0)["Amount"].agg(['count']).reset_index()
        moves_sort = moves.sort_values(by="count", ascending=False).reset_index(drop=True)
        A, B, C = np.split(moves_sort, [int(rA * N), int((rA + rB) * N)])
        All = moves_sort.copy()

    else:
        raise ValueError("split_method needs to be chosen from [quantile, value, moves]")

    return All, A, B, C


def HistBox(df,name = None):
    # setup the figure and axes
    fig = plt.figure(figsize=(6, 4))
    bpAx = fig.add_axes([0.1, 0.5, 0.8, 0.4])  # left, bottom, width, height:
    # (adjust as necessary)
    histAx = fig.add_axes([0.1, 0.1, 0.8, 0.5])  # left specs should match and
    # bottom + height on this line should
    # equal bottom on bpAx line
    # plot stuff
    bp = bpAx.boxplot(df["Amount"], notch=True, vert=False)
    h = histAx.hist(df["Amount"], bins=7)

    # confirm that the axes line up
    xlims = np.array([bpAx.get_xlim(), histAx.get_xlim()])
    for ax in [bpAx, histAx]:
        ax.set_xlim([xlims.min(), xlims.max()])

    bpAx.set_xticklabels([])  # clear out overlapping xlabels
    bpAx.set_yticks([])  # don't need that 1 tick mark

    fig_name = "HistBox_%s.png" % name
    fig.savefig("../output/ABC_output/" + fig_name)
    fig.savefig("../web_app/static/imgs/ABC_output/" + fig_name)

def Pie(A,B,C):
    labels = ['A', 'B', 'C']
    sizes = [A["Amount"].sum(), B["Amount"].sum(), C["Amount"].sum()]
    explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig_name = "Pie.png"
    fig.savefig("../output/ABC_output/" + fig_name)
    fig.savefig("../web_app/static/imgs/ABC_output/" + fig_name)
    plt.close()


