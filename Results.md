# Initial Run

```
Registration took 0.0000 seconds.
Registration accuracy metrics:
  Fitness: 0.00 %
  Inlier RMSE: 0.0000
  Correspondences found: 0
  Visual Alignment: Way off
```

## Step 1:
### ICP (Iterative Closest Point)
Basic explanation: La kel source point bel pcd ble2e wahde aerab wahde ela, beaddir a transform that will make them match, I apply it and then I repeat la hadd ma yelte2o.

Limitations:
* Needs to have a close initial guess
* Can fail to align fully or only does minimal adjustments
* converge to wrong alignment

In this step we are mainly using: ``` TransformationEstimationPointToPoint() ```
It matches source points directly to target points and minimize the point-to-point distances.
This is the simplest ICP variant.

# Second Run 

```
Registration took 0.1661 seconds.
Registration accuracy metrics:
  Fitness: 0.00 %
  Inlier RMSE: 0.0000
  Correspondences found: 0
  Visual Alignment: Way off

```