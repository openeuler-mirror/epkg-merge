#!/usr/bash

pre:openssh-server() {
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :
}

post:openssh-server() {
%systemd_post sshd.service sshd.socket
}

preun:openssh-server() {
%systemd_preun sshd.service sshd.socket
}

postun:openssh-server() {
%systemd_postun_with_restart sshd.service
}

pre() {
getent group ssh_keys >/dev/null || groupadd -r ssh_keys || :

}

