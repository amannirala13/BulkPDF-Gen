#FROM ubuntu:latest

#ARG DEBIAN_FRONTEND=noninteractive
#ARG QT_GRAPHICSSYSTEM="native"

#ENV QT_DEBUG_PLUGINS=1
#ENV QT_QPA_PLATFORM=xcb
#ENV QT_QPA_PLATFORM_PLUGIN_PATH=/opt/Qt/${QT_VERSION}/gcc_64/plugins
#ENV QT_PLUGIN_PATH=/opt/Qt/${QT_VERSION}/gcc_64/plugins
#ENV DISPLAY=:1


#RUN apt-get -y update

#RUN apt-get install -y build-essential python3.8 python3.8-dev python3-pip python3.8-venv
#RUN apt-get install ffmpeg libsm6 libxext6  -y
#RUN apt-get install libx11-xcb1 -y
#RUN apt install libxkbcommon-x11-0 -y
#RUN apt-get install --reinstall libxcb-xinerama0 -y


#RUN apt-get install -y git

#RUN apt-get -y install firefox
#RUN apt-get -y install xauth


#RUN python3.8 -m pip install pip --upgrade
#RUN python3.8 -m pip install wheel

#COPY . .
#RUN ls -a
#RUN pip install -r requirements.txt
#RUN python3.8 app.py

#EXPOSE 8887
#CMD firefox
