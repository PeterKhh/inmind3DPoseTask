import open3d as o3d
import numpy as np


def register(pcd1: o3d.geometry.PointCloud, pcd2: o3d.geometry.PointCloud) -> np.ndarray:
    
    voxel_size = 0.05 #bigger voxel size = fewer points = faster = less detail
    #downsampling the pcds
    source_down = pcd1.voxel_down_sample(voxel_size) 
    target_down = pcd2.voxel_down_sample(voxel_size)

    #finding normals of the PCDs
    source_down.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2, max_nn=30)
    )
    target_down.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2, max_nn=30)
    )
    
    #computing centers of the 2 pcds
    source_center = source_down.get_center()
    target_center = target_down.get_center()
    
    initial_transformation = np.eye(4) #strating transf, baaden men aabbe fiya transl and rot 
    initial_transformation[:3, 3] = target_center - source_center #finding the transf lli target center -> src
    threshold = 0.2 #points match only eza baynetoun 0.2 units b3ad aan baaed 

    result = o3d.pipelines.registration.registration_icp(
        source_down,
        target_down,
        threshold,
        initial_transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(), #meth that estimates the rigid transf
    )

    return result.transformation