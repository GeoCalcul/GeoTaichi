import numpy as np

from src.consititutive_model.strain_rate.FluidStructureInteraction import *
from src.mpm.materials.ConstitutiveModelBase import ConstitutiveModelBase
from src.mpm.Simulation import Simulation
from src.utils.ObjectIO import DictIO


class FluidStructureInteraction(ConstitutiveModelBase):
    def __init__(self, sims: Simulation):
        super().__init__()
        self.add_material(sims.max_material_num, sims.material_type, FSIModel)
        self.stateVars = ULStateVariable.field(shape=sims.max_particle_num) 

    def add_material(self, max_material_num, material_type, material_struct):
        self.matProps = material_struct.field(shape=max_material_num)
        self.material_type = material_type

    def get_state_vars_dict(self, start_particle, end_particle):
        estress = np.ascontiguousarray(self.stateVars.estress.to_numpy()[start_particle:end_particle])
        rho = np.ascontiguousarray(self.stateVars.rho.to_numpy()[start_particle:end_particle])
        return {'estress': estress, 'rho': rho}
    
    def reload_state_variables(self, state_vars):
        estress = state_vars.item()['estress']
        rho = state_vars.item()['rho']
        kernel_reload_state_variables(estress, rho, self.stateVars)

    def model_initialize(self, material):
        materialID = DictIO.GetEssential(material, 'MaterialID')
        self.check_materialID(materialID, self.matProps.shape[0])
        
        if self.matProps[materialID].density > 0.:
            print("Previous Material Property will be overwritten!")
        is_structure = DictIO.GetEssential(material, 'IsStructure')
        if is_structure is False:
            density = DictIO.GetAlternative(material, 'Density', 1000)
            modulus = DictIO.GetAlternative(material, 'Modulus', 2e5)
            gamma = DictIO.GetAlternative(material, 'gamma', 7.)
            viscosity = DictIO.GetAlternative(material, 'Viscosity', 1e-3)
            atmospheric_pressure = DictIO.GetAlternative(material, 'atmospheric_pressure', 0.)
            self.matProps[materialID].add_fluid_material(density, modulus, viscosity, gamma, atmospheric_pressure)
        else:
            density = DictIO.GetAlternative(material, 'Density', 2650)
            young = DictIO.GetEssential(material, 'YoungModulus')
            possion = DictIO.GetAlternative(material, 'PossionRatio', 0.3)
            self.matProps[materialID].add_material(density, young, possion)
        self.contact_initialize(material)
        self.matProps[materialID].print_message(materialID)

    def get_lateral_coefficient(self, materialID):
        return 1.
