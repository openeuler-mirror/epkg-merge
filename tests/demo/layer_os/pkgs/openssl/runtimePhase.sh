#!/usr/bash

post:openssl-libs() {
-p /sbin/ldconfig
}

postun:openssl-libs() {
-p /sbin/ldconfig
}

