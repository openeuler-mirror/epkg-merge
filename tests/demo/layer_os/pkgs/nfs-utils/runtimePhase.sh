#!/usr/bash

pre() {
if [ -f /var/lock/subsys/rpc.gssd ]; then
mv /var/lock/subsys/rpc.gssd /var/lock/subsys/rpcgssd
fi

if [ -f /var/lock/subsys/rpc.idmapd ]; then
mv /var/lock/subsys/rpc.idmapd /var/lock/subsys/rpcidmapd
fi

cat /etc/group | cut -d':' -f 1 | grep rpcuser &> /dev/null
if [ "$?" -ne 0 ]; then
/usr/sbin/groupadd -g %{rpc_uid} rpcuser &> /dev/null || :
else
/usr/sbin/groupmod -g %{rpc_uid} rpcuser &> /dev/null || :
fi

cat /etc/passwd | cut -d':' -f 1 | grep rpcuser &> /dev/null
if [ "$?" -ne 0 ]; then
/usr/sbin/useradd -l -c "RPC Service User" -r -g %{rpc_uid} \
        -s /sbin/nologin -u %{rpc_uid} -d /var/lib/nfs rpcuser &> /dev/null || :
else
/usr/sbin/usermod -u %{rpc_uid} -g %{rpc_uid} rpcuser &> /dev/null || :
fi



cat /etc/group | cut -d':' -f 3 | grep %{nfsnobody_uid} &> /dev/null
if [ "$?" -ne 0 ]; then
/usr/sbin/groupadd -g %{nfsnobody_uid} nfsnobody &> /dev/null || :
fi

cat /etc/passwd | cut -d':' -f 3 | grep %{nfsnobody_uid} &> /dev/null
if [ $? -ne 0 ]; then
/usr/sbin/useradd -l -c "Anonymous NFS User" -r -g %{nfsnobody_uid} \
    -s /sbin/nologin -u %{nfsnobody_uid} -d /var/lib/nfs nfsnobody &> /dev/null || :
fi

}

post() {
if [ $1 -eq 1 ] ; then
/bin/systemctl enable nfs-client.target &> /dev/null  || :
/bin/systemctl start nfs-client.target  &> /dev/null  || :
fi

%systemd_post nfs-server
/bin/systemctl try-restart gssproxy  &> /dev/null || :

}

preun() {
if [ $1 -eq 0 ]; then
%systemd_preun nfs-client.target
%systemd_preun nfs-server.service
/bin/systemctl stop var-lib-nfs-rpc_pipefs.mount &> /dev/null || :
fi

}

postun() {
%systemd_postun_with_restart  nfs-client.target
%systemd_postun_with_restart  nfs-server

/bin/systemctl --system daemon-reload &> /dev/null  || :


}

