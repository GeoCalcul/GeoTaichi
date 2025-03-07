import taichi as ti

from src.dem.Simulation import Simulation as DEMSimulation
from src.dem.SceneManager import myScene as DEMScene
from src.dem.contact.ContactKernel import *
from src.mpdem.contact.ContactModelBase import ContactModelBase
from src.mpdem.contact.MultiLinkedCell import MultiLinkedCell
from src.mpdem.Simulation import Simulation
from src.mpm.SceneManager import myScene as MPMScene
from src.utils.ObjectIO import DictIO


class ParticleFluid(ContactModelBase):
    def __init__(self, max_material_num) -> None:
        super().__init__()
        self.surfaceProps = LiquidSurfaceProperty.field(shape=max_material_num * max_material_num)
        self.null_model = False
        self.model_type = 3

    def calcu_critical_timestep(self, mscene: MPMScene, dsims: DEMSimulation, dscene: DEMScene, max_material_num):
        mass = min(mscene.find_particle_min_mass(), dscene.find_particle_min_mass(dsims.scheme))
        stiffness = self.find_max_stiffness(max_material_num)
        return ti.sqrt(mass / stiffness)

    def find_max_stiffness(self, max_material_num):
        maxstiff = 0.
        for materialID1 in range(max_material_num):
            for materialID2 in range(max_material_num):
                componousID = self.get_componousID(max_material_num, materialID1, materialID2)
                if self.surfaceProps[componousID].kn > 0.:
                    maxstiff = ti.max(maxstiff, self.surfaceProps[componousID].kn)
        return maxstiff
    
    def add_surface_property(self, max_material_num, materialID1, materialID2, property):
        kn = DictIO.GetEssential(property, 'NormalStiffness')
        ndratio = DictIO.GetEssential(property, 'NormalViscousDamping')

        componousID = 0
        if materialID1 == materialID2:
            componousID = self.get_componousID(max_material_num, materialID1, materialID2)
            self.surfaceProps[componousID].add_surface_property(kn, ndratio)
        else:
            componousID = self.get_componousID(max_material_num, materialID1, materialID2)
            self.surfaceProps[componousID].add_surface_property(kn, ndratio)
            componousID = self.get_componousID(max_material_num, materialID2, materialID1)
            self.surfaceProps[componousID].add_surface_property(kn, ndratio)
        return componousID


    # ========================================================= #
    #              Particle Contact Matrix Resolve              #
    # ========================================================= # 
    def update_particle_particle_contact_table(self, sims: Simulation, mscene: MPMScene, dscene: DEMScene, pcontact: MultiLinkedCell):
        update_contact_table_(sims.potential_particle_num, int(mscene.particleNum[0]), pcontact.particle_particle, pcontact.potential_list_particle_particle, self.cplist)

    def update_particle_wall_contact_table(self, sims: Simulation, mscene: MPMScene, dscene: DEMScene, pcontact: MultiLinkedCell):
        update_contact_table_(sims.wall_coordination_number, int(mscene.particleNum[0]), pcontact.particle_wall, pcontact.potential_list_particle_wall, self.cplist)
        

@ti.dataclass
class LiquidSurfaceProperty:
    kn: float
    ndratio: float
    ncut: float

    def add_surface_property(self, kn, ndratio):
        self.kn = kn
        self.ndratio = ndratio
        self.ncut = 0.

    def print_surface_info(self, matID1, matID2):
        print(" Surface Properties Information ".center(71, '-'))
        print('Contact model: Fluid-Particle Model')
        print(f'MaterialID{matID1} < --- > MaterialID{matID2}')
        print('Contact normal stiffness: = ', self.kn)
        print('Viscous damping coefficient = ', self.ndratio)
        print('\n')

    @ti.func
    def _fluid_force_assemble(self, m_eff, gapn, coeff, norm, v_rel, dt):
        kn, ndratio = self.kn, self.ndratio
        vn = v_rel.dot(norm) 
        vs = v_rel - v_rel.dot(norm) * norm

        normal_contact_force = -kn * coeff * gapn 
        normal_damping_force = -2 * ndratio * ti.sqrt(m_eff * kn * coeff) * vn
        normal_force = (normal_contact_force + normal_damping_force) * norm
        tangential_force = -vs / dt[None] * m_eff
        return normal_force, tangential_force


