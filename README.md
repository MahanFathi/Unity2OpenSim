# Unity2OpenSim

This repo aims to provide the user with a painless pipeline to perform Inverse Kinematics/Dynamics of OpenSim on Unity models. 

## Usage

#### OpenSim Installation

OpenSim is not friendly with Linux systems. There's a Dockerfile which aims to alleviate the cross-platform of usage of OpenSim. Make the image at the root of the project via:

```bash
docker build -t opensim:opensim .
```

_Note: Making the image takes a bit longer than expected._

You can always get a bash from the OpenSim docker container via:

```bash
docker run -it opensim:opensim
```

_Note: You'll have access to the OpenSim cli via `opensim-cmd` in the docker bash._

You should be able to mount directories outside the docker via this:

```bash
docker run -v "$PWD"/local/host/dir/:/container/tmp/ opensim:opensim command_to_run
```

#### Arm Sample 

To model movements of a human arm you could find a unity exported sample json at `./assents/samples/unity/arm.json`, which is generated using ML-Agents' reacher model. 
This sample file is generated using the `assets/samples/unity/scripts`. 
Plug these scripts into your Unity project and export the marker positions to file. 
Note that GameObject markers should have the right marker names and should be tagged as `OpenSimMarkers`.
Feel free to change modify the scripts, but the final exported format should be the same as `arm.json`, as the format is assumed in `util/json2trc/json2trc.py` script.

###### Portal Dir

The `./portal` directory is the directory that we are going to mount to the docker container. 
We will be copying everything we need to and from this directory. 
This is not usually a good practice but OpenSim uses a lame filesystem for I/O, this way we should be able to avoid the pain.

###### Convert JOSN to TRC

Use the `json2trc.py` to convert the Unity exported json to the trc format.
```bash
cp ./assets/samples/unity/arm.json ./portal
python3 ./util/json2trc/json2trc.py --json-file=./portal/arm.json --trc-file=./portal/arm.trc
```

###### OpenSim Static Scaling Tool

Here's where we make use of OpenSim models. 
You can find the scaling assets of the arm model under `assets/arm/ModelFiles/InputFiles_module5_scaleIK`. 
We also need the related OpenSim model of `MoBL_ARMS_module5_scaleIK.osim`. Let's put these files into the portal.

```bash
cp assets/arm/ModelFiles/InputFiles_module5_scaleIK/* portal/
cp assets/arm/ModelFiles/MoBL_ARMS_module5_scaleIK.osim portal/
```

OpenSim commands take in an .xml file and all the desired arguments are contained in this file. 
We need to add the .osim model and the trc motion reference file into `MoBL_ARMS_module5_Scale_Setup.xml`. 
So open up you favorite editor and change the `<model_file>` tag from `Unassigned` to `MoBL_ARMS_module5_scaleIK.osim`.

```xml
<!--model_file>unassigned</model_file-->
<model_file>/tmp/mobl_arms_module5_scaleik.osim</model_file> 
```

_Note: These files are mounted to the `/tmp/` directory of the docker._

Also change the reference motion.:

```xml
<!--marker_file>static.trc</marker_file-->
<marker_file>/tmp/arm.trc</marker_file>
```

_Note: There are two instances of the `marker_file` in the settings file._

We also need to output the new .osim model into a file. This should be also edited in the settings file.

```xml
<!--output_model_file>Unassigned</output_model_file-->
<output_model_file>/tmp/scaled.osim</output_model_file>
```

You might also want to edit the time rage of the motion:

```xml
<!--<time_range> 7.845 8.525</time_range>-->
<time_range> 0.5 8.525</time_range>
```

Now that we have everything sorted out, OpenSim should be able to scale the model. Using the docker env:
```bash
docker run -v "$PWD"/portal/:/tmp/ opensim:opensim opensim-cmd run-tool /tmp/MoBL_ARMS_module5_Scale_Setup.xml
```

###### OpenSim Inverse Kinematic Tool

Kinematic settings were already in the `assets/arm/ModelFiles/InputFiles_module5_scaleIK` directory, so no need to `cp` them again in the `portal`.
We should plug the `scaled.osim` model and `arm.trc` reference motion into the `MoBL_ARMS_module5_IK_Setup.xml` and to further infer the muscle activations we need to output the kinematic plausible motion into a file.
The following changes should occur in `MoBL_ARMS_module5_IK_Setup.xml`:

```xml
<!--<model_file>Unassigned</model_file>-->
<model_file>/tmp/sclaed.osim</model_file>

<!--<marker_file>Unassigned</marker_file>-->
<marker_file>/tmp/arm.trc</marker_file>

<!--<time_range> 0 4.995</time_range>-->
<time_range> 0 16.0</time_range>

<!--<output_motion_file>Unassigned</output_motion_file>-->
<output_motion_file>out.mot</output_motion_file>
```

Run the following command to get the `out.mot` output reference motion:

```bash
docker run -it -v "$PWD"/portal/:/tmp/ opensim:opensim opensim-cmd run-tool /tmp/MoBL_ARMS_module5_IK_Setup.xml
```

###### OpenSim Computed Muscle Control

CMC settings lay in the `assets/arm/ModelFiles/InputFiles_module6_CMC` directory. 
`cp` them in `portal` and change the setup file accordingly:

```xml
<!--<model_file />-->
<model_file>/tmp/sclaed.osim</model_file>

<!--<desired_kinematics_file>IKreachfiltered.mot</desired_kinematics_file>-->
<desired_kinematics_file>/tmp/out.mot</desired_kinematics_file>

<!--<task_set_file>CMC_Tasks.xml</task_set_file>-->
<task_set_file>/tmp/CMC_Tasks.xml</task_set_file>

<!--<constraints_file>/tmp/CMC_ControlConstraints.xml</constraints_file>-->
<constraints_file>/tmp/CMC_ControlConstraints.xml</constraints_file>
```

Results should be in `portal/Results-CMC` directory. 
