#!/usr/bash

post() {
%systemd_post selinux-autorelabel-mark.service restorecond.service

}

preun() {
%systemd_preun selinux-autorelabel-mark.service restorecond.service

}

postun() {
%systemd_postun_with_restart restorecond.service


}

