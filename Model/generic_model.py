from gurobipy import *
from abc import ABC
import numpy as np
from abc import abstractmethod


class GenericModel(ABC):

    def __init__(self):
        self.model = Model("")

        return

    @abstractmethod
    def get_all_sets_params(self):
        return

    @abstractmethod
    def set_model_vars(self):

        pass

    @abstractmethod
    def set_model_constrs(self):
        pass

    @abstractmethod
    def set_objective(self):
        pass

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
        return model

    @abstractmethod
    def output_result(self):
        pass