docker network create radio
docker rm -f playlist
docker run -d  \
    --name playlist  \
    --user root \
    --device=/dev/snd:/dev/snd \
    --network=radio \
    --volume=$HOME/adhan/conf:/root/conf \
    --restart=always \
    mbenkhemis/darkice:0.0.3 \
    sudo /usr/local/bin/darkice -c /root/conf/darkice.cfg
