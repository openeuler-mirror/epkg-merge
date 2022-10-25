#!/usr/bash

post() {
%systemd_post quota_nld.service rpc-rquotad.service

}

preun() {
%systemd_preun quota_nld.service rpc-rquotad.service

}

postun() {
%systemd_postun_with_restart quota_nld.service rpc-rquotad.service



}

