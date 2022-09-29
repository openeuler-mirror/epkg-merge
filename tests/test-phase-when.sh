# test when condition schemes in phase.sh

build?+xxx() { echo ; }
build?-xxx() { echo ; }
build?xxx=yyy() { echo ; }
build?%%xxx=y() { echo ; }
build?arch=a,b,c() { echo ; }
build?@1.1:1.2() { echo ; }

build#+xxx() { echo ; }
build#-xxx() { echo ; }
build#xxx=yyy() { echo ; }
build#%%xxx!=y() { echo ; }
build#arch=a,b,c() { echo ; }
build#@1.1:1.2() { echo ; }
build#@1.1:1.2() { echo ; }
