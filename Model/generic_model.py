from gurobipy import *
from abc import ABC
from abc import abstractmethod


class GenericModel(ABC):

    def __init__(self):
        return

    @abstractmethod
    def get_all_sets_params(self):
        return

    @abstractmethod
    def set_model_vars(self, model):
        pass

    @abstractmethod
    def set_model_constrs(self, model):
        pass

    @abstractmethod
    def set_objective(self, model):
        pass

    def construct_model(self):
        """
        It is recommended that this method is not overridden by descendant classes

        Output:
            Gurobi.model : gurobi model already has variables, constraints, and objective defined.
            Once returned, the user should run model.optimize() to retrieve results
        """
        self.get_all_sets_params()
        model = Model("")
        model_vars = self.set_model_vars(model)
        self.set_model_constrs(model)
        self.set_objective(model)
        return model

    @abstractmethod
    def output_result(self):
        pass