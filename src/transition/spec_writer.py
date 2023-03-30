# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import copy
import os.path
import yaml
import re
from Cheetah.Template import Template
from src.transition.config import *
from src.transition.template import *
from src.log import log


class SpecWriter:
    def __init__(self, yaml_fpath, metadata):
        self.file_path = yaml_fpath
        self.metadata = metadata
        self.keywords_if_config = {}
        self.specfile = os.path.splitext(yaml_fpath)[0] + '.spec'

    def load_data_from_yaml(self):
        def _no_number(self, node):
            return str(self.construct_scalar(node))

        yaml.add_constructor('tag:yaml.org,2002:int', _no_number)
        yaml.add_constructor('tag:yaml.org,2002:float', _no_number)
        try:
            stream = open(self.file_path, 'r')
            self.metadata.update(yaml.load(stream, Loader=yaml.FullLoader))
        except IOError:
            log.error('Cannot read file: %s' % self.file_path)
        except ValueError:
            log.error('YAML format is wrong')
        except TypeError:
            # empty can lead here
            log.error('Empty yaml file: %s' % self.file_path)

    def process_use_native_commands(self):
        if 'use.nativeCommands' in self.metadata and isinstance(self.metadata['use.nativeCommands'], list):
            with open('nativeCommands.json', 'w') as f:
                for line in self.metadata['use.nativeCommands']:
                    f.write(line)

    def change_subpackage_to_list(self):
        """
        change struct of subpackage
        :return:
        """
        if "subpackage" in self.metadata and isinstance(self.metadata["subpackage"], dict):
            subpackage_list = []
            for sp_name, sp in self.metadata["subpackage"].items():
                if isinstance(sp, dict):
                    sp["name"] = sp_name
                    if "asWholeName" not in sp:
                        sp["asWholeName"] = True
                    subpackage_list.append(sp)
            self.metadata["subpackage"] = subpackage_list

    def parse_special_key(self):
        special_tmp_lines = []
        for some_key in LIST_KEYS:
            if some_key in self.metadata.keys() and some_key not in ["rpmMacros", "source", "patchset"]:
                if not self.metadata[some_key]:
                    self.metadata[some_key] = ""
                temp_some_key = copy.deepcopy(self.metadata[some_key])
                for index1, some_line in enumerate(self.metadata[some_key]):
                    temp_line = ""
                    temp_line_list = some_line.split("%if") if "%if" in some_line or "%else" in some_line else []
                    if "%if" in some_line or "%else" in some_line:
                        while len(temp_line_list):
                            if "%else" in temp_line_list[-1]:
                                if len(temp_line_list) > 1:
                                    temp_line += "%else" + os.linesep + "%if " + temp_line_list[-1].replace(
                                        "%else ", "") + os.linesep
                                    temp_line_list.pop()
                                else:
                                    temp_line += "%else" + os.linesep + some_key + ": " + temp_line_list[-1].replace(
                                        "%else ", "") + os.linesep
                                    temp_line_list.pop()
                            else:
                                if len(temp_line_list) > 1:
                                    temp_line += "%if" + temp_line_list[-1] + os.linesep
                                    temp_line_list.pop()
                                else:
                                    temp_line += some_key + ": " + temp_line_list[-1] + os.linesep
                                    temp_line_list.pop()
                        if_count = len(re.findall("%if", some_line))
                        for _ in range(if_count):
                            temp_line += "%endif" + os.linesep
                        temp_some_key.remove(some_line)
                        special_tmp_lines.append(temp_line)
                self.metadata[some_key] = temp_some_key
        final_paragra_key = os.linesep.join(special_tmp_lines)
        for requires_key, requires_new_key in REQUIRES_REPLACE.items():
            final_paragra_key = final_paragra_key.replace(requires_key, requires_new_key)
        final_paragra_key += os.linesep
        if "SpecialKey" in self.metadata:
            self.metadata["SpecialKey"] += final_paragra_key
        else:
            self.metadata["SpecialKey"] = final_paragra_key

    def trans_compile_args(self):
        """
        转换编译选项
        :return:
        """
        if "build" in self.metadata:
            # check is only make or not
            build_info_list = self.metadata["build"].split(os.linesep)
            only_make = False
            configure_make = False
            for line in build_info_list:
                if re.search("#.*make", line) is None and "make" in line and "cmake" not in line and not configure_make:
                    only_make = True
                if re.search("#.*configure", line) is None and ("/configure" in line or "%configure" in line):
                    only_make = False
                    configure_make = True
            if "compileExport" in self.metadata and isinstance(self.metadata["compileExport"], dict):
                export_list = []
                for export_name, export_value in self.metadata["compileExport"].items():
                    if isinstance(export_value, list):
                        export_value = ",".join(export_value)
                    export_list.append("export " + export_name + "=\"" + export_value + "\"")
                self.metadata["compileExport"] = export_list
            if "env.CC" in self.metadata:
                self.metadata["build"] = "export CC=\"" + self.metadata["env.CC"] + "\"" + os.linesep + self.metadata[
                    "build"]
            if "env.CFLAGS" in self.metadata:
                if only_make:
                    self.metadata["build"] = "export CFLAGS=\"" + self.metadata["env.CFLAGS"] + "\"" + os.linesep + \
                                             self.metadata["build"]
                else:
                    if "rpmMacros" in self.metadata:
                        self.metadata["rpmMacros"].append("%global optflags %optflags " + self.metadata["env.CFLAGS"])
                    else:
                        self.metadata["rpmMacros"] = ["%global optflags %optflags " + self.metadata["env.CFLAGS"]]
            if "env.LDFLAGS" in self.metadata:
                if only_make:
                    self.metadata["build"] = "export LDFLAGS=\"" + self.metadata["env.LDFLAGS"] + "\"" + os.linesep + \
                                             self.metadata["build"]
                else:
                    if "rpmMacros" in self.metadata:
                        self.metadata["rpmMacros"].append(
                            "%global build_optflags %build_optflags " + self.metadata["env.LDFLAGS"])
                    else:
                        self.metadata["rpmMacros"] = [
                            "%global build_optflags %build_optflags " + self.metadata["env.LDFLAGS"]]

    def parse_patchset(self):
        # handle patches with extra options
        if "patchset" in self.metadata:
            patches = self.metadata['patchset']

            self.metadata['patchset'] = []
            self.metadata['PatchOpts'] = []
            for patch in patches:
                if isinstance(patch, str):
                    if isinstance(patches, dict) and isinstance(patches[patch], str):
                        self.metadata['patchset'].append(patches[patch])
                    else:
                        self.metadata['patchset'].append(patch)
                    self.metadata['PatchOpts'].append('-p1')
                elif isinstance(patch, dict):
                    self.metadata['patchset'].append(list(patch.keys())[0])
                    self.metadata['PatchOpts'].append(list(patch.values())[0])
                elif isinstance(patch, list):
                    self.metadata['patchset'].append(patch[0])
                    self.metadata['PatchOpts'].append(' '.join(patch[1:]))

    def change_source_to_list(self):
        if 'source' in self.metadata and type(self.metadata['source']) is dict:
            source_list = []
            for item_key, item in self.metadata['source'].items():
                source_list.append(item)
            self.metadata['source'] = source_list

    def change_rpmmacros_linesep(self):
        if "rpmMacros" in self.metadata:
            for macros_index, macros_line in enumerate(self.metadata["rpmMacros"]):
                if "{os.linesep}" in macros_line:
                    self.metadata["rpmMacros"][macros_index] = macros_line.replace("{os.linesep}", os.linesep)

    def generate_necessary_keys(self):
        self.metadata["builder"] = ""
        necessary_keys = ["name", "version", "meta.summary", "meta.license", "release", "meta.description"]
        for necessary_key in necessary_keys:
            if necessary_key not in self.metadata.keys():
                self.metadata[necessary_key] = ""
                log.error("no such necessary key:" + necessary_key)

    def change_field(self):
        """
        在change_subpackage_to_list之前执行
        需要yaml中无数组嵌套字典
        :return:
        """

        def replace_dict_keywords(origin: dict, keywords):
            target_dict = copy.deepcopy(origin)
            for key in origin.keys():
                target_key = key
                if str(key).__contains__(keywords):
                    value = origin[key]
                    target_key = str(key).replace(keywords, "")
                    del target_dict[key]
                    target_dict[target_key] = value
                if type(origin[key]) is dict:
                    target_dict[target_key] = replace_dict_keywords(origin[key], keywords)
            return target_dict

        # replace rpmWhen
        self.metadata = replace_dict_keywords(self.metadata, "rpmWhen ")
        # replace runtimePhase.
        self.metadata = replace_dict_keywords(self.metadata, "runtimePhase.")
        # replace phase.
        self.metadata = replace_dict_keywords(self.metadata, "phase.")
        # replace meta.
        self.metadata = replace_dict_keywords(self.metadata, "meta.")

    def parse_subpackage_files_with_if(self):
        """
        在change_subpackage_to_list之后执行
        :return:
        """
        target_metadata = self.metadata.copy()
        for some_key in self.metadata:
            if some_key == "subpackage":
                for index0, sp in enumerate(self.metadata["subpackage"]):
                    if isinstance(sp, dict):
                        target_sp = sp.copy()
                        for sp_key in sp:
                            if sp_key.startswith("files") and "%if" in sp_key and "filesJudgement" not in sp:
                                judge_list = sp_key.split("%if")[1:]
                                this_value = sp[sp_key]
                                del target_sp[sp_key]
                                target_sp["files"] = this_value
                                target_sp["filesJudgement"] = map(lambda x: ("%if" + x).strip(), judge_list)
                        target_metadata["subpackage"][index0] = target_sp
        self.metadata = target_metadata

    def parse(self):
        """
        yaml字段解析
        :return:
        """
        self.process_use_native_commands()
        self.generate_necessary_keys()
        self.change_field()
        self.change_subpackage_to_list()
        self.change_source_to_list()
        self.parse_special_key()
        self.trans_compile_args()
        self.parse_patchset()
        self.change_rpmmacros_linesep()
        self.parse_subpackage_files_with_if()

    @staticmethod
    def arch_split(value):
        m = re.match(r'^(\w+):([^:]+)', value)
        if m:
            arch = m.group(1)
            left = m.group(2)
            if arch in ARCHS:
                return arch, ARCHS[arch], left
            else:
                return arch, arch, left
        else:
            return '', '', value

    def trans_data_to_spec(self):
        spec_content = Template(file=template_path + "/spec.tmpl",
                                searchList=[{
                                    'metadata': self.metadata,
                                    'arch_split': self.arch_split,
                                    'keywords_if_config': self.keywords_if_config,
                                }]).respond()

        def collation_spec_content(content):
            """
            整理模板引擎处理过后的spec数据
            :param content:
            :return:
            """
            while "\n\n\n\n" in content:
                content = content.replace("\n\n\n\n", "\n\n\n")
            if "\n%endif\n%endif\n" in content:
                temp_text = content.split("\n%endif\n%endif\n")[0]
                if re.search("\n%if.*\n%if.*\n", temp_text) is not None:
                    cutter1 = re.findall("\n%if.*\n%if.*\n", temp_text)[0]
                    temp_text = temp_text.split(cutter1)[1]
                    body_text = temp_text.replace("%endif\n", "")
                    content = content.replace(temp_text, body_text)
            if re.search(r"\n\s*\\b", content) is not None:
                some_texts = re.findall(r"\n\s*\\b", content)
                for some_text in some_texts:
                    content = content.replace(some_text, " ")
            # content = content.replace("\\\\\n", "\\\n")
            return content

        spec_content = collation_spec_content(spec_content)
        file = open(self.specfile, "w")
        file.write(spec_content)
        file.close()


def generate_spec(file_path):
    if not os.path.isfile(file_path):
        log.error("file_path is not a file")
        return
    if not file_path.endswith(".yaml") and not file_path.endswith(".yaml"):
        log.error("Cannot find valid yaml file")
        return
    # change to workspace directory
    directory = os.path.dirname(file_path)
    if file_path.find(os.path.sep) != -1 and directory != os.path.curdir:
        os.chdir(directory)
    file_name = os.path.basename(file_path)
    spec_writer = SpecWriter(yaml_fpath=file_name, metadata={})
    spec_writer.load_data_from_yaml()
    spec_writer.parse()
    spec_writer.trans_data_to_spec()
