FROM ubuntu:16.04

# INSTALL DEPENDENCIES
RUN apt-get update && apt-get install -y vim
RUN apt-get install -y git
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y build-essential
RUN apt-get install -y cmake
RUN apt-get install -y freeglut3-dev 
RUN apt-get install -y libxi-dev 
RUN apt-get install -y libxmu-dev 
RUN apt-get install -y liblapack-dev 
RUN apt-get install -y swig 
RUN apt-get install -y python-dev

WORKDIR ~

# ================================================================================ 
#					BUILD OPENSIM
# ================================================================================ 
RUN cd ~ && git clone https://github.com/opensim-org/opensim-core.git
RUN mkdir ~/opensim_dependencies_build
RUN cd ~/opensim_dependencies_build && cmake ~/opensim-core/dependencies/ \
	-DCMAKE_INSTALL_PREFIX='~/opensim_dependencies_install' \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo
RUN cd ~/opensim_dependencies_build && make -j4

RUN mkdir ~/opensim_build
RUN cd ~/opensim_build && cmake ~/opensim-core \
       -DCMAKE_INSTALL_PREFIX="~/opensim_install" \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DOPENSIM_DEPENDENCIES_DIR="~/opensim_dependencies_install" \
       -DBUILD_PYTHON_WRAPPING=ON \
       -DBUILD_JAVA_WRAPPING=OFF \
       -DWITH_BTK=ON
RUN cd ~/opensim_build && make -j4
RUN cd ~/opensim_build && make install
# ================================================================================ 
#				END BUILD OPENSIM
# ================================================================================ 

RUN echo 'export PATH=~/opensim_install/bin:$PATH' >> ~/.bashrc

# INSTALL PYOSIM
RUN cd ~/opensim_install/lib/python2.7/site-packages && python setup.py install
RUN pip install IPython==5.0

# INSTALL ezc3d
#RUN cd ~ && git clone https://github.com/pyomeca/ezc3d.git
#RUN cd ~/ezc3d && mkdir build && cd build && cmake .. && make && make install
#
## INSTALL pyomeca
#RUN cd ~ && pip install git+https://github.com/pyomeca/pyomeca/
#
## INSTALL BTKCore for BTKPython
#RUN apt-get install -y python-qt4
#RUN cd ~ && git clone https://github.com/Biomechanical-ToolKit/BTKCore.git
#RUN cd ~/BTKCore && mkdir build && cd build && cmake .. && make && make install
#RUN cd ~ && git clone https://github.com/Biomechanical-ToolKit/BTKPython.git
#RUN apt-get install -y qt4-dev-tools
#RUN apt-get install -y pyqt4-dev-tools
#RUN apt-get install -y qt4-qmake
#RUN apt-get install -y python-qt4-dev
#RUN cd ~ && git clone https://github.com/MeVisLab/pythonqt.git && cd pythonqt && qmake && make all
#RUN cd ~/BTKPython && mkdir build && cd build && cmake .. && make && make install
