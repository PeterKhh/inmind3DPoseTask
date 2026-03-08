## Initial Run

```
Registration took 0.0000 seconds.
Fitness: 0.00 %
Inlier RMSE: 0.0000
Correspondences found: 0
Visual Alignment: Way off
```

# Step 1:
### ICP (Iterative Closest Point)
Basic explanation: La kel source point bel pcd ble2e wahde aerab wahde ela, beaddir a transform that will make them match, I apply it and then I repeat la hadd ma yelte2o.

Limitations:
* Needs to have a close initial guess
* Can fail to align fully or only does minimal adjustments
* converge to wrong alignment

In this step we are mainly using: ``` TransformationEstimationPointToPoint() ```
It matches source points directly to target points and minimize the point-to-point distances.
This is the simplest ICP variant.

## Run Results

```
Registration took 0.1661 seconds.
Fitness: 0.00 %
Inlier RMSE: 0.0000
Correspondences found: 0
Visual Alignment: Way off
```

As u may notice ICP didn't do much since it was a far first guess. This is why step 2 will include a better guess.

# Step 2
### Centroid Alignment
Before running ICP, I will first translate the source cloud so that its center matches the target cloud’s center.

Main line: ```initial_transformation[:3, 3] = target_center - source_center```

## Run Results
```
Registration took 6.4109 s        -----
Fitness: 8.57 %                   ++
Inlier RMSE: 0.0123             
Correspondences found: 17045
Visual Alignment: Bad
```


Registration took a lot of time. While still not really performing well. Next step will help reduce runtime, remove noise and might affect alignment.

# Step 3
### Downsampling
Before running ICP, we will downsample the clouds so that we have less points to deal with.
Helps with:
* runtime
* processing
* alignment

Main idea: reducing cubes of points to a point that represents. Most often using mean values...

## Run Results

```
Registration took 0.0612 s        +++++
Fitness: 8.98 %                   +
Inlier RMSE: 0.0117               -
Correspondences found: 17853      +
Visual alignment: Bad (same as step before)
```

# Step 4
### Normals and Point to Plane ICP
Main idea: Instead of focus on minimizing point to point distance, it minimizes the distance to the surface of the matched point. We will be using the normals.

While estimating normals:
* radius: neighborhood to consider for each normal (voxel size * 2 is standard).
* max_nn: max number of nearby points for each normal 

Main line: ``` TransformationEstimationPointToPlane() ```

## Run Results

```
Registration took 0.1258 s        -
Fitness: 9.35 %                   +
Inlier RMSE: 0.0121               -
Correspondences found: 18582      -
Visual alignment: Very Bad        -
```

# Step 5
### RANSAC and FPFH

FPFH describes the local shape around a point using: ```fpfh : Fast Point Feature Histogram```
* the point position
* neighboring points
* normals

RANSAC tries to align the clouds by:
* matching points using FPFH descriptors
* sampling candidate correspondences
* testing rigid transforms
* keeping the best one

## Run Results
```
Registration took 0.3063 s        -
Fitness: 47.78 %                  +++++
Inlier RMSE: 0.0105               ++
Correspondences found: 95005      +++++
Visual alignment: Good            ++
```

# Step 6
### Refine RANSAC result with ICP
Main idea: Use the RANSAC transform as the initial guess, then let ICP refine it for tighter alignment.
RANSAC gives a good coarse alignment. (rough pose)
ICP is best at fine alignment. (precision)

ICP is a local optimizer. We run RANSAC, throw it to ICP as initial guess in:
```
o3d.pipelines.registration.registration_icp(
        ...,
        ..,
        ...,
        init=ransac_result.transformation,
        ...,
    )
```

This way it starts from a much better guess and goes to find a better alignment

## Run Results
```
Registration took 1.3497 s        ---
Fitness: 62.11 %                  +++
Inlier RMSE: 0.0066               +++
Correspondences found: 123490     +++
Visual alignment: Very Good       ++
```
# Step 7
### Tuning parameters
### 7A: correspondence threshold:
* 0.02: 1.3497 s
* 0.015: 1.2398 s.
* 0.025: 0.9637 s <<< Chose to keep this one.