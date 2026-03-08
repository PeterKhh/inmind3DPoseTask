import open3d as o3d
import numpy as np


def register(pcd1: o3d.geometry.PointCloud, pcd2: o3d.geometry.PointCloud) -> np.ndarray:
    #computing centers of the 2 pcds
    source_center = pcd1.get_center()
    target_center = pcd2.get_center()

    initial_transformation = np.eye(4) #strating transf, baaden men aabbe fiya transl and rot 
    initial_transformation[:3, 3] = target_center - source_center #finding the transf lli target center -> src
    threshold = 0.2 #points match only eza baynetoun 0.2 units b3ad aan baaed 

    result = o3d.pipelines.registration.registration_icp(
        pcd1,
        pcd2,
        threshold,
        initial_transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(), #meth that estimates the rigid transf
    )

    return result.transformation