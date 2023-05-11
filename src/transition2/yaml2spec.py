import os

import yaml
import re
from src.log import log
from Cheetah.Template import Template

# 单独处理的字段
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


class SpecWriter:
    def __init__(self, yaml_fpath, metadata={}):
        self.file_path = yaml_fpath
        self.metadata = metadata
        self.target_metadata = {}

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
                if package_name in self.target_metadata['subpackage']:
                    self.target_metadata['subpackage'][package_name].update({condition: self.metadata[main_field]})
                else:
                    self.target_metadata['subpackage'][package_name] = {}
                    self.target_metadata['subpackage'][package_name].update({condition: self.metadata[main_field]})
                # 将meta字段分解成单独字段
                if 'meta' in self.target_metadata['subpackage'][package_name][condition]:
                    target_meta = {}
                    for meta_field, meta_value in self.target_metadata['subpackage'][package_name][condition]['meta'].items():
                        target_meta.update({meta_field: meta_value})
                    del self.target_metadata['subpackage'][package_name][condition]['meta']
                    self.target_metadata['subpackage'][package_name][condition].update(target_meta)
                # 解析子包中所有字段
                values = {}
                for sub_filed in self.target_metadata['subpackage'][package_name][condition]:
                    sub_condition = ''
                    sub_values = self.target_metadata['subpackage'][package_name][condition][sub_filed]
                    if sub_filed.__contains__(' rpmWhen '):
                        sub_condition = sub_filed[sub_filed.find(' rpmWhen ') + 1:]
                        sub_filed = sub_filed[0:sub_filed.find(' rpmWhen ')]
                    if sub_filed in values:
                        values[sub_filed].update({sub_condition: sub_values})
                    else:
                        values.update({sub_filed: {sub_condition: sub_values}})
                del self.target_metadata['subpackage'][package_name][condition]
                self.target_metadata['subpackage'][package_name][condition] = values

    def parse_dict_keys(self):
        """
        {'dict_key': {'condition1': 'value1', 'condition2': 'value2'}
        :return:
        """
        for main_filed in self.metadata:
            for key in DICT_KEYS:
                if main_filed.startswith(key):
                    condition = ''
                    if main_filed.__contains__(' rpmWhen '):
                        condition = main_filed[main_filed.find(' rpmWhen ') + 1:]
                    if key in self.target_metadata:
                        self.target_metadata[key].update({condition: self.metadata[main_filed]})
                    else:
                        self.target_metadata[key] = {condition: self.metadata[main_filed]}
                    break

    def parse_str_keys(self):
        for main_filed in self.metadata:
            for key in STR_KEYS:
                if main_filed.startswith(key):
                    condition = ''
                    if main_filed.__contains__(' rpmWhen '):
                        condition = main_filed[main_filed.find(' rpmWhen ') + 1:]
                    if key in self.target_metadata:
                        self.target_metadata[key].update({condition: self.metadata[main_filed]})
                    else:
                        self.target_metadata[key] = {condition: self.metadata[main_filed]}
                    break

    def parse_list_keys(self):
        for main_filed in self.metadata:
            for key in LIST_KEYS:
                if main_filed.startswith(key):
                    condition = ''
                    if main_filed.__contains__(' rpmWhen '):
                        condition = main_filed[main_filed.find(' rpmWhen ') + 1:]
                    if key in self.target_metadata:
                        self.target_metadata[key].update({condition: self.metadata[main_filed]})
                    else:
                        self.target_metadata[key] = {condition: self.metadata[main_filed]}
                    break

    def parse_meta(self):
        """
        trans metadata{'meta': {'file1': 'value1','file2': 'value2'}}
        to metadata{'file1': 'value1','file2': 'value2'}
        :return:
        """
        if 'meta' in self.metadata:
            for main_field in self.metadata['meta']:
                self.metadata[main_field] = self.metadata['meta'][main_field]

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
                becond_values = self.metadata[field]
                target_values = []
                # todo defineFlags后的值添加为评论
                for value in becond_values:
                    if value.startswith('+'):
                        target_value = '%becond_without ' + value[1:]
                        target_values.append(target_value)
                    elif value.startswith('-'):
                        target_value = '%becond_with ' + value[1:]
                        target_values.append(target_value)
                self.target_metadata['defineFlags'][condition] = target_values

    def parse_phase(self):
        # phase. prep build install check clean
        # move configure to build
        for main_field in list(self.metadata):
            if main_field.startswith('phase.configure'):
                if 'phase.build' in list(self.metadata):
                    self.metadata['phase.build'] = self.metadata[main_field] + self.metadata['phase.build']
                    self.metadata.pop(main_field)
        # move phase. to self.target_metadata
        for main_field in self.metadata:
            if main_field.startswith('phase.') and not main_field.__contains__(':'):
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
                if target_field in self.target_metadata:
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
                else:
                    self.target_metadata[target_field] = []
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})

    def parse_runtimePhase(self):
        """
        trans matadata{'runtimePhase.pre': 'values1', 'subpackage.package1': {'runtimePhase.pre': 'values_sub1'}}
        to target_metadata{'pre': [{'condition': '', 'param': '', 'values': 'values1'},
        {'condition': '', 'parm': '-n package1', 'values': 'values_sub1'}]
        """
        # parse condition
        for main_field in self.metadata:
            condition = ''
            param = ''
            value = ''
            target_field = ''
            if main_field.startswith('runtimePhase.') and not main_field.__contains__('rpm_macro_param'):
                if main_field.__contains__(" rpmWhen "):
                    condition = main_field[main_field.find(' rpmWhen ') + 1:]
                    target_field = main_field[main_field.find('.') + 1:main_field.find(' rpmWhen ')]
                    target_param_field = 'runtimePhase.' + target_field + ":rpm_macro_param " + condition
                else:
                    target_field = main_field[main_field.find('.') + 1:]
                    target_param_field = 'runtimePhase.' + target_field + ":rpm_macro_param"
                # parse param
                value = self.metadata[main_field]
                if target_param_field in self.metadata:
                    param = self.metadata[target_param_field]
                if target_field in self.target_metadata:
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
                else:
                    self.target_metadata[target_field] = []
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
            if main_field.startswith('subpackage.'):
                if main_field.__contains__(' rpmWhen '):
                    sub_name = main_field[main_field.find('.') + 1:main_field.find(' rpmWhen ')]
                    condition = main_field[main_field.find(' rpmWhen ') + 1:]
                else:
                    sub_name = main_field[main_field.find('.') + 1:]
                sub_values = self.metadata[main_field]
                for sub_field in sub_values:
                    if sub_field.startswith('runtimePhase.') and not sub_field.__contains__("rpm_macro_param"):
                        if sub_field.__contains__(' rpmWhen '):
                            target_field = sub_field[sub_field.find('.') + 1:sub_field.find(' rpmWhen ')]
                            # 嵌套表达式用’and'连接
                            condition = condition + ' and ' + sub_field[sub_field.find(' rpmWhen ') + len(' rpmWhen '):]
                        else:
                            target_field = sub_field[sub_field.find('.') + 1:]
                        value = sub_values[sub_field]
                        param = '-n ' + sub_name
                        for k in sub_values:
                            if k.__contains__('rpm_macro_param'):
                                param = param + ' ' + sub_values[k]
                                break
                        if target_field in self.target_metadata:
                            self.target_metadata[target_field].append(
                                {'condition': condition, 'param': param, 'value': value})
                        else:
                            self.target_metadata[target_field] = []
                            self.target_metadata[target_field].append(
                                {'condition': condition, 'param': param, 'value': value})

    def parse_files(self):
        """
        trans metadata{'files': 'values', 'subpackage.package1': {'files': 'values'} }
        to
        target_metadata{'files': [{'condition':'', 'param':'', 'values': 'values'},
        {'condition':'', 'param': '-n package1', 'values': 'values'}]
        :return:
        """
        target_field = 'files'
        self.target_metadata[target_field] = []
        for main_field in self.metadata:
            condition = ''
            param = ''
            value = ''
            if main_field.startswith('files') and not main_field.__contains__(':'):
                if main_field.__contains__(" rpmWhen "):
                    condition = main_field[main_field.find(' rpmWhen ') + 1:]
                    target_param_filed = 'files:rpm_macro_param' + ' ' + condition
                else:
                    target_param_filed = 'files:rpm_macro_param'
                if target_param_filed in self.metadata:
                    param = self.metadata[target_param_filed]
                value = self.metadata[main_field]
                self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
            if main_field.startswith('subpackage.'):
                if main_field.__contains__(' rpmWhen '):
                    sub_name = main_field[main_field.find('.') + 1:main_field.find(' rpmWhen ')]
                    condition = main_field[main_field.find(' rpmWhen ') + 1:]
                else:
                    sub_name = main_field[main_field.find('.') + 1:]
                sub_values = self.metadata[main_field]
                for sub_field in sub_values:
                    if sub_field.startswith('files') and not sub_field.__contains__(":"):
                        if sub_field.__contains__(' rpmWhen '):
                            # 嵌套的条件表达式用‘and'连接
                            condition = condition + ' and ' + sub_field[sub_field.find(' rpmWhen ') + len(' rpmWhen '):]
                        value = sub_values[sub_field]
                        param = '-n ' + sub_name
                        for k in sub_values:
                            if k.__contains__('rpm_macro_param'):
                                param = param + ' ' + sub_values[k]
                                break
                        self.target_metadata[target_field].append(
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

    def parse(self):
        self.parse_macros()
        self.parse_meta()
        self.parse_str_keys()
        self.parse_list_keys()
        self.parse_dict_keys()
        self.parse_subpackage()
        self.parse_phase()
        self.parse_runtimePhase()
        self.parse_files()


    def trans_data_to_spec(self, temp_name):
        spec_content = Template(file='template/' + temp_name,
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
        print(spec_content)


if __name__ == '__main__':
    yaml_file = 'template/bind.yaml'
    spec_writer = SpecWriter(yaml_file, {})
    spec_writer.load_data_from_yaml()
    spec_writer.parse()
    spec_writer.trans_data_to_spec('spec.tmpl')
