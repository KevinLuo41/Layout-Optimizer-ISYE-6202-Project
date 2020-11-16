import pandas as pd

# Read Data
def read_picking(picking_path=None):
    picking = pd.read_csv(picking_path)
    picking["Execution_time"] = pd.to_datetime(picking["Execution_time"])
    return picking

def read_clayout(clayout_path=None):
    Clayout = pd.read_excel(clayout_path, header=None).astype(int)
    return Clayout
