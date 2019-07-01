# Generic CMakeLists.txt for making a Simbody-using executable.
# This shows how to use the provided SimbodyConfig.cmake to locate a Simbody
# installation on your machine so you can use it from your own code.
# You will most likely want to copy some of these lines into your own
# CMakeLists.txt rather than use this one verbatim.
cmake_minimum_required(VERSION 2.8)
project(opensim_test)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_HOME_DIRECTORY}/assets)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_HOME_DIRECTORY}/assets)

# Set OpenSim Installation directory path, containing OpenSimConfig.cmake file here
set(OpenSim_DIR /home/mahan/Libraries/opensim_install/lib64/cmake/OpenSim)

# List your source and header files here.
set(src main.cpp)
#set(inc myexe.h)

# This depends on SimbodyConfig.cmake being located somewhere predictable
# on your machine. If you have installed it somewhere that CMake won't be
# able to guess, you'll need to tell find_package where to look.
find_package(OpenSim REQUIRED)

# This is only necessary if Simbody was built using CMake older than 3.0.2.
include_directories(${OpenSim_INCLUDE_DIR} /home/mahan/Libraries/opensim-models-install/Geometry)

add_executable(main ${src})
target_link_libraries(main ${OpenSim_LIBRARIES})
