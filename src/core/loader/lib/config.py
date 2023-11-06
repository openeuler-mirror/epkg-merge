CONFIG_SET_FILES: dict = {
    "kconfig": "arch/{0}/configs/openeuler_defconfig",
}

ARCH_SYS: dict = {
    "aarch64": "arm64",
    "x86_64": "x86",
    "armv8l": "arm",
    "alpha": "alpha",
}

BASE_FLAGS_CANTACT = {
    "optflags": "optflags",
    "cflags": "build_cflags",
    "cxxflags": "build_cxxflags",
    "fflags": "build_fflags",
    "ldflags": "build_ldflags",
}

BASE_FLAGS_REPLACE = {
    "cc": "__cc",
    "cpp": "__cpp",
    "cxx": "__cxx",
    "ld": "__ld",
    "ar": "__ar",
    "as": "__as",
    "nm": "__nm",
    "objcopy": "__objcopy",
    "objdump": "__objdump",
    "ranlib": "__ranlib",
    "readelf": "__readelf",
    "strings": "__strings",
    "strip": "__strip",
}

