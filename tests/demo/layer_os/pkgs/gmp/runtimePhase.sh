#!/usr/bash

post:gmp-c++() {
-p /sbin/ldconfig
}

postun:gmp-c++() {
-p /sbin/ldconfig
}

post() {
-p /sbin/ldconfig
}

postun() {
-p /sbin/ldconfig

}

