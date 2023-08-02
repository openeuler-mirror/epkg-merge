CONFIG_SET_FILES: list = [
    "kconfig",
]

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