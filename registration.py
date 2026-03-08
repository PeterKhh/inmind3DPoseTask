import open3d as o3d
import numpy as np


# Separated prepocessing from register function
def preprocess_point_cloud(pcd: o3d.geometry.PointCloud, voxel_size: float):
    pcd_down = pcd.voxel_down_sample(voxel_size)     #downsampling the pcds

    #finding normals of the PCDs
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(
            radius=voxel_size * 2,
            max_nn=30,
        )
    )
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(
            radius=voxel_size * 5,
            max_nn=100,
        )
    )

    return pcd_down, fpfh

def register(pcd1: o3d.geometry.PointCloud, pcd2: o3d.geometry.PointCloud) -> np.ndarray:
    
    voxel_size = 0.05 #bigger voxel size = fewer points = faster = less detail

    #Preprocessing the PCDs
    source_down, source_fpfh = preprocess_point_cloud(pcd1, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(pcd2, voxel_size)

    distance_threshold = voxel_size * 2

    ransac_result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down,
        target_down,
        source_fpfh,
        target_fpfh,
        mutual_filter=True, #only mutual nearest-neighbor feature matches.
        max_correspondence_distance=distance_threshold,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        ransac_n=4, #Every trial picks 4 correspondences 
        checkers=[
            # byorfoud feature matches that are locally inconsistent. 
            # eza aande 2 src points fi fare2 byanoun distance x
            # lezim l matching target points tabaaouun ykoun fi baynoun x            
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            
            #byorfoud transforms that fit the sampled points but not the cloud overall, 
            # eza ma keno domn l dist_threshold
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold),
        ],
        #max iterations, confidence target
        criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999),
    )

    #est normals again laenno ho full res holik downsample w b3ouz lal PtoPlane
    pcd1.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2, max_nn=30)
    )
    pcd2.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2, max_nn=30)
    )

    icp_result = o3d.pipelines.registration.registration_icp(
        pcd1,
        pcd2,
        max_correspondence_distance=0.03,
        init=ransac_result.transformation,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPlane(),
    )

    return icp_result.transformation
