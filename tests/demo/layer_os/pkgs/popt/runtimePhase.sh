#!/usr/bash

pre() {

}

preun() {

}

post() {
-p /sbin/ldconfig

}

postun() {
-p /sbin/ldconfig

}

