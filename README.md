# Unity2OpenSim

This repo aims to provide the user with a painless pipeline to perform Inverse Kinematics/Dynamics of OpenSim on Unity models. 

### File Dependency Diagram (Sample: gait2354)
Files mentioned are located in the assets folder.
                                        
#### *Scaling:* `subject01_Setup_Scale.xml`

depends on: 
* `gait2354_simbody.osim`:
    - OpenSim original unscaled model
* `gait2354_Scale_MarkerSet.xml`:
    - original model marker definitions
* `subject01_static.trc`:
    - subject's marker point positions in stance? 

generates:
* `subject01_scaledOnly.osim`:
    - some useless osim model
* `subject01_scaleSet_applied.xml`:
    - weights applied for scaling
* `subject01_static_output.mot`:
    - new stance mode?
* `subject01_simbody.osim`*:
    - new scaled osim model

#### *Inverse Kinematics:* `subject01_Setup_IK.xml`

depends on:
* *`subject01_simbody.osim`*:
    - new scaled osim model
* `subject01_walk1.trc`:
    - kinematics of markers trajectory in the task

generates:
* `subject01_walk1_ik.mot`*:
    - new kinematics results
* `subject01_ik_marker_errors.sto`:
    - new kinematics errors

#### *Inverse Dynamics:* `subject01_Setup_InverseDynamics.xml`

depends on:
* *`subject01_simbody.osim`*:
    - new scaled osim model
* *`subject01_walk1_ik.mot`*:
    - new kinematics results for the task
* `subject01_walk1_grf.xml`*:
    - dynamic ground reaction forces of the task
    - depends on:
        - `subject01_walk1_grf.mot`
            - no idea
        
generates:
* `ResultsInverseDynamics/inverse_dynamics.sto`:

#### So what files do you need?
* Motion Captured or Unity Generated files:
	- `subject01_static.trc`
	- `subject01_walk1.trc`
	- `subject01_walk1_grf.xml`
	- `subject01_walk1_grf.mot`
