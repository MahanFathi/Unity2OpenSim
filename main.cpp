#include <iostream>
#include <OpenSim/OpenSim.h>
#include <OpenSim/Tools/ScaleTool.h>
#include <OpenSim/Tools/InverseKinematicsTool.h>
#include <OpenSim/Tools/InverseDynamicsTool.h>

int main() {
    // get the assets path
    std::string assetsPath = "/home/mahan/Mahan/Projects/Unity2OpenSim/assets/";

    // Scale to subject 1
    {
        // this outputs a new .osim file in the parent directory representing
        // the new scaled up body geometry, here: "subject01_simbody.osim".

        std::cout << "Scaling to subject in process ..." << std::endl;

        // Note: 'gait2354_simbody.osim', path to original model, is hardcoded in the .xml
        std::string scaleSetupFilePath(assetsPath + "subject01_Setup_Scale.xml");
        std::unique_ptr<OpenSim::ScaleTool> subjectScaleSetup(new OpenSim::ScaleTool(scaleSetupFilePath));
        subjectScaleSetup->run();
        std::cout << "Scaling done." << std::endl;
    }

    // Inverse Kinematics
    {
        // this outputs a new .mot file in the parent directory, here specified 
        // as "subject01_walk1_ik.mot", hardcoded in the IK .xlm file.

        std::cout << "Inverse Kinematics in process ..." << std::endl;

        OpenSim::InverseKinematicsTool::registerTypes();

        // Note: 'subject01_simbody.osim', path to subject model, is hardcoded in the .xml
        std::string iKSetupFilePath(assetsPath + "subject01_Setup_IK.xml");
        std::unique_ptr<OpenSim::InverseKinematicsTool> subjectIKSetup(new OpenSim::InverseKinematicsTool(iKSetupFilePath, false));
        subjectIKSetup->run();
        std::cout << "Inverse Kinematics done." << std::endl;
    }

    // Inverse Dynamics
    {

        std::cout << "Inverse Dynamics in process ..." << std::endl;

        // NOTE: 'subject01_walk1_grf.xml', path to external loads file, is hardcoded in the .xml file.
        // NOTE: 'subject01_walk1_ik.mot', path to originall mocap file, is hardcoded in the .xml file.
        std::string iDSetupFilePath(assetsPath + "subject01_Setup_InverseDynamics.xml");
        std::unique_ptr<OpenSim::InverseDynamicsTool> subjectIDSetup(new OpenSim::InverseDynamicsTool(iDSetupFilePath, false));
        subjectIDSetup->run();
        std::cout << "Inverse Dynamics done." << std::endl;
    }

    // Load the model readily
    OpenSim::Model *model = new OpenSim::Model(assetsPath + "subject01_simbody.osim");
    std::cout << model->getJointSet() << std::endl;

    model->setUseVisualizer(true);

    // Configure the model.
    SimTK::State& state = model->initSystem();
    model->equilibrateMuscles(state);

    // Configure the visualizer.
//    model.updMatterSubsystem().setShowDefaultGeometry(true);
    SimTK::Visualizer& viz = model->updVisualizer().updSimbodyVisualizer();
    viz.setBackgroundType(viz.SolidColor);
    viz.setBackgroundColor(SimTK::White);

    std::cout << model->getAbsolutePath().toString() << std::endl;

    // Simulate.
    OpenSim::simulate(*model, state, 10.0);

    return 0;
};
