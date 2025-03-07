import taichi as ti

from src.dem.mainDEM import DEM

dem = DEM()

dem.system_init()

dem.set_configuration(domain=ti.Vector([10.,10.,10.]),
                      boundary=["Destroy", "Destroy", "Destroy"],
                      gravity=ti.Vector([0.,0.,-9.8]),
                      engine="SymplecticEuler",
                      search="LinkedCell")

dem.set_solver({
                "Timestep":         1e-4,
                "SimulationTime":   2.0,
                "SaveInterval":     0.01
               })

dem.memory_allocate(memory={
                            "max_material_number": 1,
                            "max_particle_number": 40000,
                            "max_sphere_number": 40000,
                            "max_clump_number": 0,
                            "max_plane_number": 6,
                            "verlet_distance_multiplier": 2.0
                            })

dem.add_region(region={
                       "Name": "region1",
                       "Type": "Rectangle",
                       "BoundingBoxPoint": ti.Vector([0.,0.,0.]),
                       "BoundingBoxSize": ti.Vector([7.0,7.0,7.0]),
                       "zdirection": ti.Vector([1.,1.,1.])
                       })                            

dem.add_attribute(materialID=0,
                  attribute={
                            "Density":            2650,
                            "ForceLocalDamping":  0.2,
                            "TorqueLocalDamping": 0.
                            })
                          

'''
dem.add_body(body={
                   "GenerateType": "Generate",
                   "RegionName": "region1",
                   "BodyType": "Sphere",
                   "PoissionSampling": False,
                   "TryNumber": 100,
                   "Template":{
                               "GroupID": 0,
                               "MaterialID": 0,
                               "InitialVelocity": ti.Vector([0.,0.,0.]),
                               "InitialAngularVelocity": ti.Vector([0.,0.,0.]),
                               "FixVelocity": ["Free","Free","Free"],
                               "FixAngularVelocity": ["Free","Free","Free"],
                               "MaxRadius": 0.15,
                               "MinRadius": 0.15,
                               "BodyNumber": 1000,
                               "BodyOrientation": "uniform"}})  
                         
dem.add_body(body={
                   "GenerateType": "Create",
                   "BodyType": "Sphere",
                   "Template":[{
                               "GroupID": 0,
                               "MaterialID": 0,
                               "InitialVelocity": ti.Vector([0.,0.,0.]),
                               "InitialAngularVelocity": ti.Vector([0.,0.,0.]),
                               "BodyPoint": ti.Vector([2.5,2.5,0.15]),
                               "FixVelocity": ["Free","Free","Free"],
                               "FixAngularVelocity": ["Free","Free","Free"],
                               "Radius": 0.15,
                               "BodyOrientation": "uniform"},
                               
                               {
                               "GroupID": 0,
                               "MaterialID": 0,
                               "InitialVelocity": ti.Vector([-0.,0.,0.]),
                               "InitialAngularVelocity": ti.Vector([0.,0.,0.]),
                               "BodyPoint": ti.Vector([2.5,2.5,0.5]),
                               "FixVelocity": ["Free","Free","Free"],
                               "FixAngularVelocity": ["Free","Free","Free"],
                               "Radius": 0.15,
                               "BodyOrientation": "uniform"},
                               
                               {
                               "GroupID": 0,
                               "MaterialID": 0,
                               "InitialVelocity": ti.Vector([0.,-0.,0.]),
                               "InitialAngularVelocity": ti.Vector([0.,0.,0.]),
                               "BodyPoint": ti.Vector([2.5,2.5,0.85]),
                               "FixVelocity": ["Free","Free","Free"],
                               "FixAngularVelocity": ["Free","Free","Free"],
                               "Radius": 0.15,
                               "BodyOrientation": "uniform"}]})
'''

dem.add_body(body={
                   "GenerateType": "Create",
                   "BodyType": "Sphere",
                   "Template":[{
                               "GroupID": 0,
                               "MaterialID": 0,
                               "InitialVelocity": ti.Vector([15.,0.,0.]),
                               "InitialAngularVelocity": ti.Vector([0.,0.,0.]),
                               "BodyPoint": ti.Vector([2.5,2.5,0.15]),
                               "FixVelocity": ["Free","Free","Free"],
                               "FixAngularVelocity": ["Free","Free","Free"],
                               "Radius": 0.15,
                               "BodyOrientation": "uniform"}]})

'''                           
dem.choose_contact_model(particle_particle_contact_model="Linear Model",
                         particle_wall_contact_model="Linear Model")
                            
dem.add_property(materialID1=0,
                 materialID2=0,
                 property={
                            "NormalStiffness":            1e6,
                            "TangentialStiffness":        1e6,
                            "Friction":                   0.5,
                            "NormalViscousDamping":       0.2,
                            "TangentialViscousDamping":   0.
                           })
'''
                           
dem.choose_contact_model(particle_particle_contact_model="Hertz Mindlin Model",
                         particle_wall_contact_model="Hertz Mindlin Model")
                            
dem.add_property(materialID1=0,
                 materialID2=0,
                 property={
                            "ShearModulus":            5e6,
                            "Poission":        0.3,
                            "Friction":                   0.5,
                            "Restitution":       0.9
                           })
                    
dem.add_wall(body={
                   "WallType":    "Plane",
                   "MaterialID":   0,
                   "WallCenter":   ti.Vector([5, 5, 0.]),
                   "OuterNormal":  ti.Vector([0., 0., 1.])
                  })
                  
dem.add_wall(body={
                   "WallType":    "Plane",
                   "MaterialID":   0,
                   "WallCenter":   ti.Vector([5, 5, 10.]),
                   "OuterNormal":  ti.Vector([0., 0., -1.])
                  })
                  
dem.add_wall(body={
                   "WallType":    "Plane",
                   "MaterialID":   0,
                   "WallCenter":   ti.Vector([10., 5, 5]),
                   "OuterNormal":  ti.Vector([-1., 0., 0.])
                  })
                  
dem.add_wall(body={
                   "WallType":    "Plane",
                   "MaterialID":   0,
                   "WallCenter":   ti.Vector([0., 5, 5]),
                   "OuterNormal":  ti.Vector([1., 0., 0.])
                  })
                  
dem.add_wall(body={
                   "WallType":    "Plane",
                   "MaterialID":   0,
                   "WallCenter":   ti.Vector([5, 0., 5]),
                   "OuterNormal":  ti.Vector([0., 1., 0.])
                  })
                  
dem.add_wall(body={
                   "WallType":    "Plane",
                   "MaterialID":   0,
                   "WallCenter":   ti.Vector([5, 10., 5]),
                   "OuterNormal":  ti.Vector([0., -1., 0.])
                  })

dem.select_save_data()

dem.add_solver()            

ti.profiler.print_kernel_profiler_info()
