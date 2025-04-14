### spec传统OS+yaml定制

#### 需求背景

对原有的构建方式不做改变的基础上，用户通过简单叠加yaml层来实现定制能力

specs -> group_spec

pkg_repo: git_url +
git_yaml: git_url +
git_yaml2: git_url



git_yaml1: git_url +
git_yaml2: git_url

1、get base layer
spec -> base layer
which specs?
=>
	layer's pkgs...  merge-configs

generate layer data

2、merge layers 

3、custumize_gits + left specs => snapshots
   custumize_gits (aarch64, x86)


4、use snapshots to generate task



#### user story

用户希望在软件包官方仓的基础上实现用户自定义改动，期望不需要fork官方仓库直接改动spec文件，而是通过编写定制化yaml文件实现spec文件的自定义改动，实现一次编写yaml文件多次复用。同时保留EulerMaker现有的正常的构建方式

e.g.

传统redis使用gcc编译，编译速度较慢，用户期望在redis官方仓库的spec文件基础上替换编译选项为musl-gcc，同时使用静态编译加快编译速度。

实现上列需求，原先的操作步骤是用户将src-openeuler下官方仓库fork到个人下，修改个人仓库里的spec文件，在EulerMaker上将package_repo配置成个人仓库的git_url，然后触发构建。该流程繁琐，同时需要有编写spec文件基础，同时改动无法在其他有相同需求的软件包下复用。

实际要实现快速配置，可以编写下列yaml文件

```yaml
env.CC: /usr/bin/musl-gcc -static
env.CFLAGS: -I/usr/musl/include
env.LDFLAGS: -L/usr/musl/lib
buildRequires:
    - musl-gcc
```

然后将yaml文件中的配置叠加在redis官方仓库spec文件上，就能快速实现编译选项替换，同时其他软件包能直接复用该yaml文件同时实现编译选项替换



input: packages repo;  yaml layer

output:  合并之后的packages repo, 其中的spec + yaml => 新的spec

for each packages:

​	(package repo => yaml) + 定制yaml => spec 

​    用新的spec+package repo 生成新的package repo (git)

下发构建任务



web显示：原始yaml + 原始spec + 合并后的spec文件

触发任务方式不变化，正常单包、增量和全量触发



#### 方案

方案1

package_overrides中添加custom_url、custom_branch

```python
package_overrides = {
    'pkg1': {
        'custom_url': 'https://gitee.com/xxx/xxx.git',
        'custom_branch': 'master' # default
    },
    ...
}
```

配置定制yaml文件要求命名为pkg.yaml





获取spec_commits时，若能在package_overrides中查询到某个包存在custom_url，执行特殊的软件仓初始化函数

首先正常fetch软件包仓库，fullcopy软件包仓库到new_repo = /srv/git/customization/origin_package_repo/${os_project}/{pkg_name}下

将copy后软件仓中的spec文件转换为yaml文件

clone custom_url至/srv/git/customization/custom_layer/目录下

使用合并工具将custom_url中的yaml合并叠加在软件仓原始spec转换的yaml上，生成新yaml文件

将yaml文件转换成spec文件并copy到new_repo下替换原始spec文件，将new_repo初始化成git仓库

参考正常创建快照获取commit信息，获取新生成的软件包repo仓的commit信息

```python
fetch_all()
for pkg in all_pkgs:
	if package_overrides.get(pkg).get('custom_url'):
        full_copy_repo_to_path(pkg, path1)
        transfer_spec_to_yaml(pkg)
        init_git_repo(pkg)
        clone_custom_layer(custom_url, path2)
        merge_custom_layer_to_pkg(custom_url, pkg)
        transfer_yaml_to_spec(pkg)
        submit_commit(pkg)
        get_spec_commit(new_pkg_repo)
        
```

方案2

project新增custom_layers记录所有定制层，每个层定义使能的软件包

```python
custom_layers = {
    'layer_1': {
        'custom_url': 'https://gitee.com/xxx/xxx.git',
        'custom_branch': 'master' # default,
    }
    ...
}
```

因同一定制yaml可能应用于多个软件包定制，定制的yaml文件命名不要求与软件包名相关





现有获取spec_commit逻辑，layer_urls => spec_groups => my_specs

在此基础上将custom_layers添加在队尾，即layer_urls => spec_groups => my_specs => custom_layers

实现用户定制layer叠加在spec上后生成的新spec的commit信息优先级最高

生成新pkg_git_repo同方案1

```python
get_spec_commits_from_layer_urls()
get_spec_commits_from_spec_groups()
get_spec_commits_from_my_specs()
get_spec_commits_from_custom_layers

def get_spec_commits_from_custom_layers(custom_layers):
    # no need fetch
    for custom_layer in custom_layers:
        clone_custom_layer(custom_url, path1)
        for pkg in custom_layer.get('enable_pkgs'):
            full_copy_repos_to_path(pkg, path1)
            transfer_spec_to_yaml(pkg)
       	    init_git_repo(pkg)
            merge_custom_layer_to_pkg(custom_url, pkg) merge-configs
            submit_commit(pkg)
            get_spec_commit(new_pkg_repo)
```



#### 方案选型

优缺点

|       | 优点                                   | 缺点                                             |
| ----- | -------------------------------------- | ------------------------------------------------ |
| 方案1 | 一对一定制软件包，可实现软件包细节定制 | 大颗粒的定制需要为每个软件包添加定制层，操作繁琐 |
| 方案2 | 可实现单yaml批量定制软件包             | 针对单包的细节性定制复用性不高                   |



#### 实现

openEuler-customization当前已有spec转yaml工具(openEulerTransition)，待确定合并yaml是沿用已有的merge-configs(base on layer)还是开发新合并策略实现
