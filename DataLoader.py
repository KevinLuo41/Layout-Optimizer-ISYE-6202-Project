import pandas as pd
import numpy as np

# Read Data
def read_picking(picking_path=None, i_path = None):
    picking = pd.read_csv(picking_path)
    picking["Execution_time"] = pd.to_datetime(picking["Execution_time"])
    Item = pd.read_excel(i_path)
    Item = Item[~Item["Article number"].isna()]
    Item["Article number"] = Item["Article number"].astype(int)

    picking = picking.merge(Item[["Article number", "number per load carrier"]],
                            left_on="Artikelno", right_on="Article number", how="left")
    del picking['Article number']
    picking = picking.rename(columns={"number per load carrier": "Unit_load"})
    return picking

def read_clayout(clayout_path=None):
    Clayout = pd.read_excel(clayout_path, header=None).astype(int)
    return Clayout


def generate_input(picking = None, Clayout = None):
    model_input = picking[["Execution_time","Artikelno","Amount","Unit_load"]].groupby(
        ["Artikelno","Unit_load"],as_index = 0)["Amount"].agg({"Total":'sum',"Picks":'count'}).reset_index(drop=True)
    model_input["Full_pallet"] = np.ceil(model_input["Total"]/model_input["Unit_load"]).astype(int)

    unique, counts = np.unique(Clayout.to_numpy().flatten(), return_counts=True)
    li = pd.DataFrame({"Artikelno": unique[2:], "Min_area": counts[2:], "Assigned": np.zeros_like(counts[2:])})
    model_input = model_input.merge(li, on="Artikelno", how="left")
    model_input["Min_area"] = 1
    model_input["Assigned"] = model_input["Assigned"].fillna(0).astype(int)

    return model_input

def read_stack(stack_path=None,selection = None):
    stack_data = pd.read_csv(stack_path)
    selection = pd.DataFrame({"Artikelno":selection,"Stack_Easiness":np.ones_like(selection)})
    selection = selection.merge(stack_data,on="Artikelno",how="left")
    selection["Easiness"] = selection["Easiness"].fillna(selection["Stack_Easiness"])
    selection = selection[["Artikelno","Easiness"]].astype(int)
    return selection


def dist_matrix(Clayout=None, c=(-16, 2), unit_h=1.2, unit_v=0.8):
    # x:row, y:col
    # horizontal 1.2, vertical 0.8
    nx, ny = Clayout.shape
    x = np.linspace(0, nx - 1, nx)
    y = np.linspace(0, ny - 1, ny)

    coord = np.array(np.meshgrid(x, y)).transpose([2, 1, 0])
    dist = np.sum(abs(coord - c) * (unit_v, unit_h), axis=2)

    coord_x = coord[:, :, 0].astype(int)
    coord_y = coord[:, :, 1].astype(int)

    df = pd.DataFrame({"x": coord_x.flatten(),
                       "y": coord_y.flatten(),
                       "dist": dist.flatten(),
                       "clayout": Clayout.to_numpy().flatten()})
    df = df[df["clayout"] != -1]

    return df




