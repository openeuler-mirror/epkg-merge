CONFIG_SET_FILES: dict = {
    "kconfig": "arch/{0}/configs/openeuler_defconfig",
}

ARCH_SYS: dict = {
    "aarch64": "arm64",
    "x86_64": "x86",
    "armv8l": "arm",
    "alpha": "alpha",
}

INDEX_CONF = {
    "configFilesPattern": r"(?P<_pkgname>[-0-9a-zA-Z_.]+)(/|\\)(package\.yaml)",
    "registerConfigSpaceForEachFile": {
        "pkgs.${{pkg._basename}}:fspath": "${{pkg._filepath}}",
        "files.\"${{pkg._filepath}}\"": {
            "name": "${{pkg._basename}}", # can catch spell error if conflict with the name defined in yaml
            "docType": "base",
            "includePhase": "phase.sh",
            "includeRuntimePhase": "runtimePhase.sh runtimePhase.lua",
            "include": "versions.yaml files.yaml defineFlags.yaml",
            ":referAttrs": "types.package",
            "meta:referAttrs": "types.package.meta",
            "phase:referAttrs": "types.package.phase",
            "runtimePhase:referAttrs": "types.package.runtimePhase"
        }
    }
}

BASE_FLAGS = {
    "optflags": "optflags",
    "cflags": "build_cflags",
    "cxxflags": "build_cxxflags",
    "fflags": "build_fflags",
    "ldflags": "build_ldflags",
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

MERGE_SCRIPTS = {
    "merge_config": "/opt/merge_configs/merge_config.sh"
}
