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
    def __init__(self, yaml_fpath, metadata):
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
                                      'condition2': 'value2'
                                     },
                         'package2': { 'condition1': 'value1', 'condition2': 'value2'}
                         }
         }
        """
        self.target_metadata['subpackage'] = {}
        for main_field in self.metadata:
            if main_field.startswith('subpackage.'):
                if main_field.__contains__(" when "):
                    condition = main_field[main_field.find(" when ") + 1:]
                    package_name = main_field[main_field.find('.') + 1:main_field.find(" when ")]
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
                    for meta_field in self.target_metadata['subpackage'][package_name][condition]['meta']:
                        target_meta.update({meta_field:
                                                self.target_metadata['subpackage'][package_name][condition]['meta'][
                                                    meta_field]})
                    del self.target_metadata['subpackage'][package_name][condition]['meta']
                    self.target_metadata['subpackage'][package_name][condition].update(target_meta)
                # 解析子包中所有字段
                values = {}
                for sub_filed in self.target_metadata['subpackage'][package_name][condition]:
                    sub_condition = ''
                    sub_values = self.target_metadata['subpackage'][package_name][condition][sub_filed]
                    if sub_filed.__contains__(' when '):
                        sub_condition = sub_filed[sub_filed.find(' when ') + 1:]
                        sub_filed = sub_filed[0:sub_filed.find(' when ')]
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
                    if main_filed.__contains__(' when '):
                        condition = main_filed[main_filed.find(' when ') + 1:]
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
                    if main_filed.__contains__(' when '):
                        condition = main_filed[main_filed.find(' when ') + 1:]
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
                    if main_filed.__contains__(' when '):
                        condition = main_filed[main_filed.find(' when ') + 1:]
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
        self.target_metadata['useFlags'] = {}
        if 'rpmMacros' in self.metadata:
            self.target_metadata['rpmMacros'] = self.metadata['rpmMacros']
        if 'rpmGlobal' in self.metadata:
            self.target_metadata['rpmGlobal'] = self.metadata['rpmGlobal']
        for field in self.metadata:
            if field.startswith('useFlags'):
                condition = ''
                if field.__contains__(' when '):
                    condition = field[field.find(' when ') + 1:]
                becond_values = self.metadata[field]
                target_values = []
                # todo useflags后的值添加为评论
                for value in becond_values:
                    if value.startswith('+'):
                        target_value = '%becond_without ' + value[1:]
                        target_values.append(target_value)
                    elif value.startswith('-'):
                        target_value = '%becond_with ' + value[1:]
                        target_values.append(target_value)
                self.target_metadata['useFlags'][condition] = target_values

    def parse_phase(self):
        # phase. prep build install check
        # move configure to build
        for main_field in list(self.metadata):
            if main_field.startswith('phase.configure'):
                if 'phase.build' in list(self.metadata):
                    self.metadata['phase.build'] = self.metadata[main_field] + self.metadata['phase.build']
                    self.metadata.pop(main_field)
        condition = ''
        param = ''
        value = ''
        target_field = ''
        # move phase. to self.target_metadata
        for main_field in self.metadata:
            if main_field.startswith('phase.'):
                if main_field.__contains__(" when "):
                    target_field = main_field[main_field.find('.') + 1:main_field.find(" when ")]
                    condition = main_field[main_field.find(" when ") + 1:]
                else:
                    target_field = main_field[main_field.find('.') + 1:]
                values = self.metadata[main_field]
                line_index = values.find('\n')
                first_line = values[0:line_index]
                if first_line.__contains__("rpm_macro_param: "):
                    param_index = first_line.find("rpm_macro_param: ") + len("rpm_macro_param: ")
                    param = first_line[param_index:]
                    value = values[line_index + 1:]
                else:
                    value = values
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
            if main_field.startswith('runtimePhase.'):
                if main_field.__contains__(" when "):
                    target_field = main_field[main_field.find('.') + 1:main_field.find(' when ')]
                    condition = main_field[main_field.find(' when ') + 1:]
                else:
                    target_field = main_field[main_field.find('.') + 1:]
                # parse param
                values = self.metadata[main_field]
                line_index = values.find('\n')
                first_line = values[0:line_index]
                if first_line.__contains__("rpm_macro_param: "):
                    param_index = first_line.find("rpm_macro_param: ") + len("rpm_macro_param: ")
                    param = first_line[param_index:]
                    value = values[line_index + 1:]
                else:
                    value = values
                if target_field in self.target_metadata:
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
                else:
                    self.target_metadata[target_field] = []
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
            if main_field.startswith('subpackage.'):
                if main_field.__contains__(' when '):
                    sub_name = main_field[main_field.find('.') + 1:main_field.find(' when ')]
                    condition = main_field[main_field.find(' when ') + 1:]
                else:
                    sub_name = main_field[main_field.find('.') + 1:]
                sub_values = self.metadata[main_field]
                for sub_field in sub_values:
                    if sub_field.startswith('runtimePhase.'):
                        if sub_field.__contains__(' when '):
                            target_field = sub_field[sub_field.find('.') + 1:sub_field.find(' when ')]
                            # 条件表达式直接连接
                            condition = sub_field[sub_field.find(' when ') + 1:] + ' and ' + condition
                        else:
                            target_field = sub_field[sub_field.find('.') + 1:]
                        values = sub_values[sub_field]
                        line_index = values.find('\n')
                        first_line = values[0:line_index]
                        if first_line.__contains__("rpm_macro_param: "):
                            param_index = first_line.find("rpm_macro_param: ") + len("rpm_macro_param: ")
                            param = first_line[param_index:] + " -n " + sub_name
                            value = values[line_index + 1:]
                        else:
                            param = " -n " + sub_name
                            value = values
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
        for main_field in self.metadata:
            condition = ''
            param = ''
            value = ''
            if main_field.startswith('files'):
                if main_field.__contains__(" when "):
                    condition = main_field[main_field.find(' when ') + 1:]
                # parse param
                values = self.metadata[main_field]
                line_index = values.find('\n')
                first_line = values[0:line_index]
                if first_line.__contains__("rpm_macro_param: "):
                    param_index = first_line.find("rpm_macro_param: ") + len("rpm_macro_param: ")
                    param = first_line[param_index:]
                    value = values[line_index + 1:]
                else:
                    value = values
                if target_field in self.target_metadata:
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
                else:
                    self.target_metadata[target_field] = []
                    self.target_metadata[target_field].append({'condition': condition, 'param': param, 'value': value})
            if main_field.startswith('subpackage.'):
                if main_field.__contains__(' when '):
                    sub_name = main_field[main_field.find('.') + 1:main_field.find(' when ')]
                    condition = main_field[main_field.find(' when ') + 1:]
                else:
                    sub_name = main_field[main_field.find('.') + 1:]
                sub_values = self.metadata[main_field]
                for sub_field in sub_values:
                    if sub_field.startswith('files'):
                        if sub_field.__contains__(' when '):
                            # 条件表达式直接连接
                            condition = sub_field[sub_field.find(' when ') + 1:] + ' ' + condition
                        values = sub_values[sub_field]
                        line_index = values.find('\n')
                        first_line = values[0:line_index]
                        if first_line.__contains__("rpm_macro_param: "):
                            param_index = first_line.find("rpm_macro_param: ") + len("rpm_macro_param: ")
                            param = first_line[param_index:] + " -n " + sub_name
                            value = values[line_index + 1:]
                        else:
                            param = " -n " + sub_name
                            value = values
                        if target_field in self.target_metadata:
                            self.target_metadata[target_field].append(
                                {'condition': condition, 'param': param, 'value': value})
                        else:
                            self.target_metadata[target_field] = []
                            self.target_metadata[target_field].append(
                                {'condition': condition, 'param': param, 'value': value})

    def parse_when(self, line):
        """
        根据条件表达式还原spec中的%if表达式
        :param line: 条件表达式
        :return:
        """
        judgement = ""
        # do(when +***=>%if %{with ***})
        if re.search("when\s+[+-][\w_]+", line) is not None:
            results = re.findall("when\s+[+-][\w_]+", line)
            for result in results:
                line = line.replace(result, "")
                if "+" in result:
                    condition = result.split("+")[1]
                    judgement += "%if %{with " + condition + "}" + "\n"
                elif "-" in result:
                    condition = result.split("-")[1]
                    judgement += "%if %{without " + condition + "}" + "\n"
        # do(when %%%{rpmGlobal.openEuler}=>%if 0%{?openEuler})
        if re.search("when\s+%+\{[\w|_.]+}", line) is not None:
            results = re.findall("when\s+%+\{[\w|_.]+}", line)
            for result in results:
                line = line.replace(result, "")
            conditions = list(map(lambda x: x.split("{")[1].rstrip("}").replace("rpmGlobal.", ""), results))
            for condition in conditions:
                judgement += "%if 0%{?" + condition + "}" + "\n"
        # do(when arch in=>%ifarch|%ifos|%ifnarch|%ifnos)
        if re.search("when arch|os in [\w|_.]+", line) is not None:
            results = re.findall("when arch in [\w|_.]+", line) + re.findall("when os in [\w|_.]+", line)
            for result in results:
                line = line.replace(result, "")
            conditions = list(
                map(lambda x: x.replace("when arch in", "%ifarch").replace("when os in", "%ifos"), results))
            for condition in conditions:
                judgement += condition + "\n"
        if re.search("when arch|os not in [\w|_.]+", line) is not None:
            results = re.findall("when arch not in [\w|_.]+", line) + re.findall("when os not in [\w|_.]+", line)
            for result in results:
                line = line.replace(result, "")
            conditions = list(map(lambda x: x.replace("when arch not in", "%ifnarch").replace(
                "when os not in", "%ifnos"), results))
            for condition in conditions:
                judgement += condition + "\n"
        if "when" in line:
            results = re.findall("when\s+.*", line)
            for result in results:
                judgement += result.replace("when not", "%if !").replace("when", "%if") + "\n"
        if judgement.endswith("\n"):
            judgement = judgement[0:-1]
        return judgement

    def print_endif(self, condition):
        """
        在spec中，一个%if条件对应一个%endif,
        condition存在多个条件嵌套，例如：when arch in x86 when +benchtests,
        所以根据when的个数确定%endif的个数
        :param conditon:
        :return:
        """
        end_str = ''
        results = re.findall("when", condition)
        for _ in results:
            end_str += "%endif\n"
        return end_str

    def parse(self):
        self.parse_macros()
        self.parse_str_keys()
        self.parse_list_keys()
        self.parse_dict_keys()
        self.parse_subpackage()

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
    yaml_file = 'template/glibc.yaml'
    spec_writer = SpecWriter(yaml_file, {})
    spec_writer.load_data_from_yaml()
    spec_writer.parse()
    spec_writer.trans_data_to_spec('spec.tmpl')
