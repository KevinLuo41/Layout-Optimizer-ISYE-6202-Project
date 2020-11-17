import numpy as np
import pandas as pd
from DataLoader import *
from gurobipy import *
from Model.generic_model import *

from gurobipy import *
from abc import ABC
from abc import abstractmethod


class SelectionModel:
    def __init__(self, model_input, Clayout, s=2, cr=2, N=None):

        self.model_input = model_input
        self.Clayout = Clayout
        self.s = s
        self.cr = 2
        self.N = N

        self.model = Model("")

        return

    @abstractmethod
    def get_all_sets_params(self):
        self.A = self.model_input["Artikelno"].to_numpy()
        self.pi = dict(zip(self.A, self.model_input["Picks"].to_numpy()))
        self.di = dict(zip(self.A, self.model_input["Full_pallet"].to_numpy()))
        self.li = dict(zip(self.A, self.model_input["Min_area"].to_numpy()))

        if self.N is None:
            self.N = np.count_nonzero(self.Clayout.to_numpy().flatten() != -1)

        return

    @abstractmethod
    def set_model_vars(self, model):
        print("Defining Variables")
        self.x_i = {}
        for i in self.A:
            self.x_i[i] = model.addVar(vtype=GRB.BINARY, name='x_i[%s]' % (i))

    @abstractmethod
    def set_model_constrs(self, model):
        print("Defining Constraints")
        C1 = model.addConstr((quicksum(self.x_i[i] * self.li[i] for i in self.A) <= self.N), "")

    @abstractmethod
    def set_objective(self, model):

        model.setObjective(quicksum((self.s * self.pi[i] - self.cr * self.di[i]) * self.x_i[i] for i in self.A),
                           GRB.MAXIMIZE)

    def construct_model(self):
        """
        It is recommended that this method is not overridden by descendant classes

        Output:
            Gurobi.model : gurobi model already has variables, constraints, and objective defined.
            Once returned, the user should run model.optimize() to retrieve results
        """
        self.get_all_sets_params()
        self.set_model_vars(self.model)
        self.set_model_constrs(self.model)
        self.set_objective(self.model)
        return self.model

    def output_result(self):
        solution = {}
        select = []
        for v in self.model.getVars():
            solution[v.VarName[4:-1]] = v.x
            if v.x == 1:
                select.append(int(v.VarName[4:-1]))
        print(select)

if __name__ == "__main__":
    data_path = "../../WHAI-provided_data/"
    p_path = data_path + "02_picking-activity_K1.csv"
    i_path = data_path + "04_Item-Master_K1.xlsx"
    clayout_path = data_path + "Current_layout.xlsx"

    picking = read_picking(p_path, i_path)
    Clayout = read_clayout(clayout_path)
    model_input = generate_input(picking, Clayout)

    Selection = SelectionModel(model_input, Clayout)

    model = Selection.construct_model()
    model.optimize()

    Selection.output_result()
