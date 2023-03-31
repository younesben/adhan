docker network create radio
docker rm -f live
docker run -d \
    --name live \
    --user root \
    --device=/dev/snd:/dev/snd \
    --network=radio \
    --volume=$HOME/adhan/conf:/root/conf \
    mbenkhemis/darkice:0.0.3 \
    sudo /usr/local/bin/darkice -c /root/conf/darkice-live.cfg