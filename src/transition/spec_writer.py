import os

import yaml
import re
from src.log import log
from Cheetah.Template import Template
from src.transition.template import *

# only these keys can be parsed
STR_KEYS = ('name',
            'version',
            'release',
            'epoch',
            'group',
            'prefix',
            'summary',
            'description',
            'license',
            'homepage',
            'buildArch',
            'autoReq',
            'autoProv',
            'autoReqProv',
            )

LIST_KEYS = ('exclusiveArch',
             'buildRoot',
             'recommends',
             'excludeArch',
             'buildRequires',
             'suggests',
             'requires',
             'requiresPre',
             'requiresPost',
             'requiresPreun',
             'requiresPostun',
             'requiresPretrans',
             'requiresPosttrans',
             'buildConflicts',
             'provides',
             'includeSource'
             )

DICT_KEYS = ('source',
             'patchset'
             )

PHASE_KEYS = ('prep',
              'build',
              'install',
              'check',
              'clean',
              )

RUNTIMEPHASE_KEYS = ('pre',
                     'preun',
                     'pretrans',
                     'preuntrans'
                     'post',
                     'postun',
                     'posttrans',
                     'postuntrans',
                     'verify',
                     'triggerprein',
                     'triggerin',
                     'triggerun',
                     'triggerpostun',
                     'filetriggerin',
                     'filetriggerun',
                     'filetriggerpostun',
                     'transfiletriggerin',
                     'transfiletriggerun',
                     'transfiletriggerpostun',
                     )

FILES_KEYS = ('files',)

class SpecWriter:
    def __init__(self, yaml_fpath, metadata=None):
        if metadata is None:
            metadata = {}
        self.file_path = yaml_fpath
        self.metadata = metadata
        self.target_metadata = {}
        self.spec_file = ""

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

    def parse_subpackage(self):
        """
         {'subpackage': {'package1': { 'condition1': {'field1': {
                                                               'field1_condition1': 'field1_values',
                                                               'field1_condition2': 'field1_values'
                                                               }
                                                     },
                                      'condition2': {}
                                     },
                         'package2': { 'condition1': {}, 'condition2': {}}
                         }
         }
        """
        self.target_metadata['subpackage'] = {}
        for main_field in self.metadata:
            if main_field.startswith('subpackage.'):
                if main_field.__contains__(" rpmWhen "):
                    condition = main_field[main_field.find(" rpmWhen ") + 1:]
                    package_name = main_field[main_field.find('.') + 1:main_field.find(" rpmWhen ")]
                else:
                    condition = ''
                    package_name = main_field[main_field.find('.') + 1:]
                self.target_metadata['subpackage'].setdefault(package_name, {}).\
                    update({condition: self.metadata[main_field]})

                # 解析子包中所有字段
                values = {}
                for sub_filed in self.target_metadata['subpackage'][package_name][condition]:
                    sub_condition = ''
                    sub_values = self.target_metadata['subpackage'][package_name][condition][sub_filed]
                    if sub_filed.__contains__(' rpmWhen '):
                        sub_condition = sub_filed[sub_filed.find(' rpmWhen ') + 1:]
                        sub_filed = sub_filed[0:sub_filed.find(' rpmWhen ')]
                    values.setdefault(sub_filed, {}).update({sub_condition: sub_values})
                del self.target_metadata['subpackage'][package_name][condition]
                self.target_metadata['subpackage'][package_name][condition] = values

    def parse_simple_keys(self):
        """
        {'simple_key': {'condition1': 'value1', 'condition2': 'value2'}}
        :return:
        """
        KEYS = STR_KEYS + LIST_KEYS + DICT_KEYS
        for main_filed in self.metadata:
            for key in KEYS:
                if main_filed.startswith(key):
                    condition = ''
                    if main_filed.__contains__(' rpmWhen '):
                        condition = main_filed[main_filed.find(' rpmWhen ') + 1:]
                    self.target_metadata.setdefault(key, {}).\
                        update({condition: self.metadata[main_filed]})
                    break

    def format_meta(self):
        """
        trans metadata{'meta': {'file1': 'value1','file2': 'value2'}}
        to metadata{'file1': 'value1','file2': 'value2'}
        :return:
        """
        if 'meta' in self.metadata:
            for key in self.metadata['meta']:
                self.metadata[key] = self.metadata['meta'][key]
            del self.metadata['meta']
        for key in self.metadata:
            if key.startswith("subpackage"):
                value = self.metadata[key]
                if 'meta' in value:
                    for sub_key in value['meta']:
                        self.metadata[key][sub_key] = value[sub_key]
                    del self.metadata[key]['meta']

    def format_runtimePhase(self):
        for key in list(self.metadata.keys()):
            if key.startswith("runtimePhase."):
                value = self.metadata[key]
                del self.metadata[key]
                new_key = key.replace('runtimePhase.', "", 1)
                self.metadata[new_key] = value
            if key.startswith("subpackage."):
                sub_value = self.metadata[key]
                for sub_key in list(sub_value.keys()):
                    if sub_key.startswith("runtimePhase."):
                        value = sub_value[sub_key]
                        del self.metadata[key][sub_key]
                        new_key = sub_key.replace('runtimePhase.', "", 1)
                        self.metadata[key][new_key] = value

    def parse_macros(self):
        self.target_metadata['defineFlags'] = {}
        if 'rpmMacros' in self.metadata:
            self.target_metadata['rpmMacros'] = self.metadata['rpmMacros']
        if 'rpmGlobal' in self.metadata:
            self.target_metadata['rpmGlobal'] = self.metadata['rpmGlobal']
        for field in self.metadata:
            if field.startswith('defineFlags'):
                condition = ''
                if field.__contains__(' rpmWhen '):
                    condition = field[field.find(' rpmWhen ') + 1:]
                becond_dict = self.metadata[field]
                target_dict = {}
                for k in becond_dict:
                    if k.startswith("+"):
                        target_k = "%bcond_without " + k[1:]
                    elif k.startswith("-"):
                        target_k = "%bcond_with " + k[1:]
                    else:
                        target_k = k
                    target_dict[target_k] = becond_dict[k]
                # todo defineFlags后的值添加为评论
                self.target_metadata['defineFlags'][condition] = target_dict
                break

    def parse_phase(self):
        # phase. prep build install check clean
        # move configure to build
        for main_field in self.metadata:
            if main_field.startswith('phase.configure'):
                configure_name = main_field.split(".")[-1]
                if 'phase.build' in list(self.metadata):
                    lines = self.metadata['phase.build'].split("\n")
                    target_lines = []
                    for line in lines:
                        _line = line.strip()
                        if _line == configure_name:
                            target_lines.append(self.metadata[main_field])
                        else:
                            target_lines.append(line)
                    self.metadata['phase.build'] = "\n".join(target_lines)
        # move phase. to self.target_metadata
        for main_field in self.metadata:
            if main_field.startswith('phase.') and 'rpm_macro_param' not in main_field and 'configure' not in main_field:
                condition = ''
                param = ''
                if main_field.__contains__(" rpmWhen "):
                    condition = main_field[main_field.find(" rpmWhen ") + 1:]
                    target_field = main_field[main_field.find('.') + 1:main_field.find(" rpmWhen ")]
                    target_param_filed = 'phase.' + target_field + ':rpm_macro_param ' + condition
                else:
                    target_field = main_field[main_field.find('.') + 1:]
                    target_param_filed = 'phase.' + target_field + ':rpm_macro_param'
                if target_param_filed in self.metadata:
                    param = self.metadata[target_param_filed]
                value = self.metadata[main_field]
                self.target_metadata.setdefault(target_field, []).\
                    append({'condition': condition, 'param': param, 'value': value})

    def parse_shell(self):
        """
        trans matadata{'pre': 'values1', 'subpackage.package1': {'pre': 'values_sub1'}}
        to target_metadata{'pre': [{'condition': '', 'param': '', 'values': 'values1'},
        {'condition': '', 'parm': '-n package1', 'values': 'values_sub1'}]
        """
        KEYS = RUNTIMEPHASE_KEYS + FILES_KEYS
        for spec_key in KEYS:
            param = ''
            condition = ''
            self.trans_shell(self.metadata, spec_key, condition, param)
            for key in self.metadata:
                if key.startswith('subpackage.'):
                    if key.__contains__(' rpmWhen '):
                        sub_name = key[key.find(".") + 1:key.find(' rpmWhen ')]
                        condition = key[key.find(' rpmWhen ') + 1:]
                    else:
                        sub_name = key[key.find(".") + 1:]
                    sub_values = self.metadata[key]
                    param = "-n " + sub_name
                    self.trans_shell(sub_values, spec_key, condition, param)

    def trans_shell(self, meta_json, spec_key, condition, param):
        key_param = spec_key + ":rpm_macro_param"
        for key in meta_json:
            # 避免相同前缀, 如：pre, preun
            pattern = '^' + spec_key + '\\w+.*$'
            if re.match(pattern, key):
                continue
            if key.startswith(spec_key) and not key.startswith(key_param):
                value = meta_json[key]
                param_key = key.replace(spec_key, key_param, 1)
                if param_key in meta_json:
                    param += ' ' + meta_json[param_key]
                if key.__contains__(' rpmwhen '):
                    if condition:
                        condition += ' and ' + key[key.find(' rpmwhen ') + len(' rpmwhen '):]
                    else:
                        condition = key[key.find(' rpmwhen '):]
                self.target_metadata.setdefault(spec_key, []).append(
                    {'condition': condition, 'param': param, 'value': value})
            # 只有参数
            if key.startswith(key_param):
                target_key = key.replace(key_param, spec_key, 1)
                if target_key not in meta_json:
                    value = ""
                    param += ' ' + meta_json[key]
                    if key.__contains__(' rpmwhen '):
                        if condition:
                            condition += ' and ' + key[key.find(' rpmwhen ') + len(' rpmwhen '):]
                        else:
                            condition = key[key.find(' rpmwhen '):]
                    self.target_metadata.setdefault(spec_key, []).append(
                        {'condition': condition, 'param': param, 'value': value})

    def trans_compile_args(self):
        """
        转换编译选项

        :return:
        """
        if "build" in self.metadata:
            # check is only make or not
            build_info_list = self.metadata["phase.build"].split(os.linesep)
            only_make = False
            configure_make = False
            for line in build_info_list:
                if re.search("#.*make", line) is None and "make" in line and "cmake" not in line and not configure_make:
                    only_make = True
                if re.search("#.*configure", line) is None and ("/configure" in line or "%configure" in line):
                    only_make = False
                    configure_make = True
            # compileExport 是列表，在%build字段中
            if "compileExport" in self.metadata and isinstance(self.metadata["compileExport"], dict):
                export_list = []
                for export_name, export_value in self.metadata["compileExport"].items():
                    if isinstance(export_value, list):
                        export_value = ",".join(export_value)
                    export_list.append("export " + export_name + "=\"" + export_value + "\"")
                self.metadata["compileExport"] = export_list
            # env.CC, env.LDFLAGS, env.CFLAGS都是字符串
            if "env.CC" in self.metadata:
                self.metadata["phase.build"] = "export CC=\"" + self.metadata["env.CC"] + "\"" + os.linesep + self.metadata[
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

    def parse_when(self, line):
        """
        根据条件表达式还原spec中的%if表达式
        :param line: 条件表达式
        :return:
        """
        judgement = ""
        # do(when +***=>%if %{with ***})
        if re.search("rpmWhen\s+[+-][\w_]+", line) is not None:
            results = re.findall("rpmWhen\s+[+-][\w_]+", line)
            for result in results:
                line = line.replace(result, "")
                if "+" in result:
                    condition = result.split("+")[1]
                    judgement += "%if %{with " + condition + "}" + "\n"
                elif "-" in result:
                    condition = result.split("-")[1]
                    judgement += "%if %{without " + condition + "}" + "\n"
        # do(rpmWhen %%%{rpmGlobal.openEuler}=>%if 0%{?openEuler})
        if re.search("rpmWhen\s+%+\{[\w|_.]+}", line) is not None:
            results = re.findall("rpmWhen\s+%+\{[\w|_.]+}", line)
            for result in results:
                line = line.replace(result, "")
            conditions = list(map(lambda x: x.split("{")[1].rstrip("}").replace("rpmGlobal.", ""), results))
            for condition in conditions:
                judgement += "%if 0%{?" + condition + "}" + "\n"
        # do(rpmWhen arch in=>%ifarch|%ifos|%ifnarch|%ifnos)
        if re.search("rpmWhen arch|os in [\w|_.]+", line) is not None:
            results = re.findall("rpmWhen arch in [\w|_.]+", line) + re.findall("rpmWhen os in [\w|_.]+", line)
            for result in results:
                line = line.replace(result, "")
            conditions = list(
                map(lambda x: x.replace("rpmWhen arch in", "%ifarch").replace("rpmWhen os in", "%ifos"), results))
            for condition in conditions:
                judgement += condition + "\n"
        if re.search("rpmWhen arch|os not in [\w|_.]+", line) is not None:
            results = re.findall("rpmWhen arch not in [\w|_.]+", line) + re.findall("rpmWhen os not in [\w|_.]+", line)
            for result in results:
                line = line.replace(result, "")
            conditions = list(map(lambda x: x.replace("rpmWhen arch not in", "%ifnarch").replace(
                "rpmWhen os not in", "%ifnos"), results))
            for condition in conditions:
                judgement += condition + "\n"
        if "rpmWhen" in line:
            results = re.findall("rpmWhen\s+.*", line)
            for result in results:
                judgement += result.replace("rpmWhen not", "%if !").replace("rpmWhen", "%if") + "\n"
        if judgement.endswith("\n"):
            judgement = judgement[0:-1]
        return judgement

    def print_endif(self, condition):
        """
        在spec中，一个%if条件对应一个%endif,
        condition存在多个条件嵌套，例如：rpmWhen arch in x86 rpmrpmWhen +benchtests,
        所以根据rpmWhen的个数确定%endif的个数
        :param conditon:
        :return:
        """
        end_str = ''
        results = re.findall("rpmWhen", condition)
        for _ in results:
            end_str += "%endif\n"
        return end_str

    def convert_double_percent_sign(self):
        for k, v in self.metadata.items():
            if type(v) is str:
                self.metadata[k] = v.replace("\%\%", "%%")
            if k.startswith("subpackage"):
                for sub_k, sub_v in self.metadata[k].items():
                    if type(sub_v) is str:
                        self.metadata[k][sub_k] = sub_v.replace("\%\%", "%%")

    def parse(self):
        self.format_meta()
        self.format_runtimePhase()
        self.convert_double_percent_sign()
        self.parse_macros()
        self.parse_simple_keys()
        self.parse_subpackage()
        self.parse_phase()
        self.parse_shell()

    def trans_data_to_spec(self):
        spec_content = Template(file=template_path + "/spec.tmpl",
                                searchList=[{
                                    'metadata': self.target_metadata,
                                    'parse_when': self.parse_when,
                                    'print_endif': self.print_endif
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
        file = open(self.spec_file, "w")
        file.write(spec_content)
        file.close()


def generate_spec(file_path):
    if not os.path.isfile(file_path):
        log.error("file_path is not a file")
        return
    if not file_path.endswith(".yaml") and not file_path.endswith(".yaml"):
        log.error("Cannot find valid yaml file")
        return
    directory = os.path.dirname(file_path)
    if file_path.find(os.path.sep) != -1 and directory != os.path.curdir:
        os.chdir(directory)
    file_name = os.path.basename(file_path)
    spec_writer = SpecWriter(yaml_fpath=file_name, metadata={})
    spec_writer.load_data_from_yaml()
    spec_writer.parse()
    spec_writer.spec_file = os.path.splitext(spec_writer.file_path)[0] + '.spec'
    spec_writer.trans_data_to_spec()
