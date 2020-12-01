from Simulator.simulator import *
from ABC_Analysis.ABC import *

def dist_matrix(nx=12, ny=36, c=(-16, 2), unit_x=1.2, unit_y=0.8):
    x = np.linspace(0, nx - 1, nx)
    y = np.linspace(0, ny - 1, ny)

    coord = np.array(np.meshgrid(y, x)).transpose([2, 1, 0])
    dist = np.sum(abs(coord - c) * (unit_y, unit_x), axis=2)

    coord_x = coord[:, :, 0].astype(int)
    coord_y = coord[:, :, 1].astype(int)

    df = pd.DataFrame({"x": coord_x.flatten(),
                       "y": coord_y.flatten(),
                       "dist": dist.flatten()})
    #     df
    return df

def layout_matrix(distance_mat = None, Clayout=None):
    nx = max(distance_mat["x"])+1
    ny = max(distance_mat["y"])+1
    layout = np.zeros([nx,ny]).astype(int)
#     print(layout.shape)
    layout[0:6,0:11]= -1
    layout[:,[1,4,7,10]]= -1
    distance_mat["layout"] = layout.flatten()
    distance_mat["Clayout"] = Clayout.to_numpy().flatten()
    return distance_mat

def model_input(All = None,Clayout=None):
    unique, counts = np.unique(Clayout.to_numpy().flatten(), return_counts=True)
    model_in = All.merge(pd.DataFrame({"Artikelno":unique, "storage":counts}), on = "Artikelno",how="left").fillna(1)
    model_in["moves_p"] = model_in["count"]/model_in["storage"]
    model_in = model_in.sort_values(by = "moves_p",ascending = False).reset_index(drop = True)
    return model_in


def heurist_layout(layout = None, model_in= None):
    output = layout.sort_values(by="dist", ascending=True)
    #     print(len(output[output["layout"]!=-1])

    ava_cell = len(output[output["layout"] != -1])
    num_items = len(model_in["Artikelno"])
    if ava_cell < num_items:
        #         print(output.loc[output["layout"]!=-1,:])
        output.loc[output["layout"] != -1, "layout"] = model_in["Artikelno"][:ava_cell].to_numpy()
    #         print(output.loc[output["layout"]!=-1, "layout"])
    else:
        output.loc[output["layout"] != -1, "layout"][:num_items] = model_in["Artikelno"].to_numpy()

    output = output.sort_values(by=["x", "y"], ascending=True).reset_index(drop=True)
    return output


if __name__ == "__main__":
    data_path = "../../WHAI-provided_data/"
    p_path = data_path + "02_picking-activity_K1.csv"
    clayout_path = data_path+"Current_layout.xlsx"
    item_path = data_path+"04_Item-Master_K1.xlsx"

    picking = read_picking(p_path,item_path)
    clayout = read_clayout(clayout_path)

    # forecast
    model, forecast = Simulator(142, picking)

    # model
    dist = dist_matrix()
    layout_mat  =layout_matrix(dist,clayout)
    All_prod, A, B, C = ABC(data=picking, split_method="moves", time_scale=1)

    model_in = model_input(All_prod,clayout)
    output = heurist_layout(layout_mat,model_in)
    out_matrix = output.layout.astype(int).to_numpy().reshape(36,12)
    print(out_matrix)



