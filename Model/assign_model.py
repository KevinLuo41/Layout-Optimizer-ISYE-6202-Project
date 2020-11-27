from gurobipy import *
from DataLoader import *

from Model.generic_model import *


def get_selection():
    S = []
    with open("../output/selection.txt", "r") as f:
        for line in f:
            S.append(int(line))

    S = np.array(S)

    return S

class AssignmentModel(GenericModel):

    def __init__(self, model_input, Dist_mat, stack):
        super().__init__()
        self.Dist_mat = Dist_mat
        self.model_input = model_input
        self.stack = stack

        self.model = Model("")
        return

    def get_all_sets_params(self):
        self.C = self.Dist_mat[self.Dist_mat["clayout"] != -1][["x", "y"]].to_records(index=False)
        self.C = np.array(self.C).astype(tuple)

        self.D_c = dict(zip(self.C, np.array(self.Dist_mat["dist"])))

        try:
            self.S = get_selection()
        except:
            raise FileExistsError("Please run selection model first!!!")

        input_S = self.model_input[self.model_input["Artikelno"].isin(self.S)]
        self.D_s = dict(zip(input_S["Artikelno"], input_S["Total"]))
        self.P_s = dict(zip(input_S["Artikelno"], input_S["Picks"]))
        self.T_s = dict(zip(self.stack["Artikelno"], self.stack["Easiness"]))



        return

    def set_model_vars(self):
        print("Defining Variables")
        self.x_sc = {}

        for s in self.S:
            for c in self.C:
                self.x_sc[(s,c)] = self.model.addVar(vtype=GRB.BINARY, name='x_sc[%s+%s]' % (s,c))


    def set_model_constrs(self):
        print("Defining Constraints")
        C2 = self.model.addConstrs((quicksum(self.x_sc[(s,c)]  for c in self.C) ==1
                             for s in self.S), "")
        C1 = self.model.addConstrs((quicksum(self.x_sc[(s,c)]  for s in self.S) ==1
                             for c in self.C), "")





    def set_objective(self):
        self.model.setObjective(quicksum(((self.P_s[s]+self.T_s[s]) * self.D_c[c] * self.x_sc[(s,c)]
                                     for c in self.C for s in self.S)),
                           GRB.MINIMIZE)

    def construct_model(self):
        """
        It is recommended that this method is not overridden by descendant classes

        Output:
            Gurobi.model : gurobi model already has variables, constraints, and objective defined.
            Once returned, the user should run model.optimize() to retrieve results
        """
        self.get_all_sets_params()

        model_vars = self.set_model_vars()
        self.set_model_constrs()
        self.set_objective()
        return


    def output_result(self):
        solution = {"SKU":[],"Cx":[],"Cy":[]}
        layout = np.full([36,12],-1)

        for v in self.model.getVars():

            if v.x == 1:
                s, c = v.VarName[5:-1].split("+")
                x,y = c[1:-1].split(",")
                solution["SKU"].append(int(s))
                solution["Cx"].append(int(x))
                solution["Cy"].append(int(y))
                layout[(int(x),int(y))]=int(s)

        print(layout)

        return solution

if __name__ == "__main__":
    data_path = "../../WHAI-provided_data/"
    p_path = data_path + "02_picking-activity_K1.csv"
    i_path = data_path + "04_Item-Master_K1.xlsx"
    clayout_path = data_path + "Current_layout.xlsx"
    stack_path = data_path + "stack.csv"

    picking = read_picking(p_path, i_path)
    Clayout = read_clayout(clayout_path)
    model_input = generate_input(picking, Clayout)
    Dist_mat = dist_matrix(Clayout)
    selection =get_selection()
    stack = read_stack(stack_path,selection)


    Assignment = AssignmentModel(model_input, Dist_mat, stack)

    Assignment.construct_model()
    Assignment.model.optimize()
    Assignment.output_result()

    # Assignment.output_result()