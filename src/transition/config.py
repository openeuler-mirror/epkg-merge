# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

LIST_KEYS = ('source',
             'requires',
             'buildRequires',
             'suggests',
             'requiresPre',
             'requiresPreUn',
             'requiresPreTrans',
             'requiresPost',
             'requiresPostUn',
             'requiresPostTrans',
             'provides',
             'conflicts',
             'buildConflicts',
             'obsoletes',
             'exclusiveArch',
             'files',
             'rpmMacros',
             'buildArch',
             )

REQUIRES_REPLACE = {"requiresPost:": "requires(post):", "requiresPostUn:": "requires(postun):",
                    "requiresPre:": "requires(pre):", "requiresPreUn:": "requires(preun):",
                    "requiresPretrans:": "requires(pretrans):", "requiresPosttrans:": "requires(posttrans):"}

# Available architecture qualifiers
ARCHS = {'ix86': '%{ix86}',
         'arm': '%{arm}',
         'armv5': 'armv5el armv5tel armv5tejl',
         'armv6': 'armv6l armv6hl',
         'armv7': 'armv7el armv7tel armv7l armv7hl armv7nhl armv7thl armv7tnhl',
         }