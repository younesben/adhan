FROM balenalib/raspberry-pi

RUN echo "deb-src http://archive.raspbian.org/raspbian buster main contrib non-free rpi firmware" >> /etc/apt/sources.list &&\
    apt update -y &&\
    apt upgrade -y &&\
    apt install apt-utils -y &&\
    apt install wget -y &&\
    apt install unzip -y &&\
    apt install -y dh-autoreconf libtool libtool-bin libasound2-dev libfftw3-dev build-essential devscripts autotools-dev fakeroot dpkg-dev debhelper autotools-dev dh-make quilt ccache libsamplerate0-dev libpulse-dev libaudio-dev lame libjack-jackd2-dev libasound2-dev libtwolame-dev libfaad-dev libflac-dev libmp4v2-dev libshout3-dev libmp3lame-dev libopus-dev
WORKDIR /tmp/build
RUN apt -b source libfaac0 faac &&\
    dpkg -i libfaac0_1.29.9.2-2_armhf.deb libfaac-dev_1.29.9.2-2_armhf.deb faac_1.29.9.2-2_armhf.deb


#RUN useradd -rm -d /home/darkice -s /bin/bash -u 1001 darkice
#USER darkice
WORKDIR /tmp/build/src
RUN wget http://tipok.org.ua/downloads/media/aacplus/libaacplus/libaacplus-2.0.2.tar.gz &&\
    tar -xzf libaacplus-2.0.2.tar.gz &&\
    sed -i 's/inline/static inline/g' libaacplus-2.0.2/frontend/au_channel.h &&\
    apt source darkice

WORKDIR libaacplus-2.0.2

RUN ./autogen.sh --host=arm-unknown-linux-gnueabi --enable-static --enable-shared &&\
    make  &&\
    make install &&\
    ldconfig 

#WORKDIR /tmp/build/src
#RUN apt source darkice

WORKDIR /tmp/build/src/darkice-1.3 
RUN ./configure --with-faac --with-faac-prefix=/usr/lib/arm-linux-gnueabihf --with-opus --with-opus-prefix=/usr/lib/arm-linux-gnueabihf --with-pulseaudio --with-pulseaudio-prefix=/usr/lib/arm-linux-gnueabihf --with-lame --with-lame-prefix=/usr/lib/arm-linux-gnueabihf --with-alsa --with-alsa-prefix=/usr/lib/arm-linux-gnueabihf --with-jack --with-jack-prefix=/usr/lib/arm-linux-gnueabihf --with-aacplus --with-aacplus-prefix=/usr/local --with-samplerate --with-samplerate-prefix=/usr/lib/arm-linux-gnueabihf --with-vorbis --with-vorbis-prefix=/usr/lib/arm-linux-gnueabihf &&\
make &&\
make install

WORKDIR /root
COPY conf/darkice.cfg /etc/darkice.cfg

CMD darkice
