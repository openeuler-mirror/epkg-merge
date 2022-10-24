#!/usr/bash

post:audispd-plugins() {
if [ -d "/etc/audisp/" ];then
for file in audisp-remote.conf au-remote.conf syslog.conf
do
if [ "$file" == "audisp-remote.conf" ];then
if [ -s "/etc/audisp/$file" ];then
diffrence=`diff /etc/audisp/$file /etc/audit/$file`
if [ "X$diffrence" != "X" ];then
cp /etc/audisp/$file /etc/audit/$file
if [ "X`grep startup_failure_action /etc/audit/$file`" == "X" ];then
echo "startup_failure_action = warn_once_continue" >> /etc/audit/$file
fi
fi
fi
elif [ "$file" == "syslog.conf" ];then
if [ -s "/etc/audisp/plugins.d/$file" ];then
diffrence=`diff /etc/audisp/plugins.d/$file /etc/audit/plugins.d/$file`
if [ "X$diffrence" != "X" ];then
cp /etc/audisp/plugins.d/syslog.conf /etc/audit/plugins.d/syslog.conf
sed -i 's/path[ ]*=[ ]*builtin_syslog/path\ =\ \/sbin\/audisp-syslog/g' /etc/audit/plugins.d/syslog.conf
sed -i 's/type[ ]*=[ ]*builtin/type\ =\ always/g' /etc/audit/plugins.d/syslog.conf
fi
fi
else
if [ -s "/etc/audisp/plugins.d/$file" ];then
diffrence=`diff /etc/audisp/plugins.d/$file /etc/audit/plugins.d/$file`
if [ "X$diffrence" != "X" ];then
cp /etc/audisp/plugins.d/$file /etc/audit/plugins.d/$file
fi
fi
fi
done
fi
}

post:audispd-plugins-zos() {
if [ -d "/etc/audisp/" ];then
for file in audispd-zos-remote.conf zos-remote.conf
do
if [ "$file" == "zos-remote.conf" ];then
if [ -s "/etc/audisp/$file" ];then
diffrence=`diff /etc/audisp/$file /etc/audit/$file`
if [ "X$diffrence" != "X" ];then
cp /etc/audisp/$file /etc/audit/$file
fi
fi
elif [ "$file" == "audispd-zos-remote.conf" ];then
if [ -s "/etc/audisp/plugins.d/$file" ];then
diffrence=`diff /etc/audisp/plugins.d/$file /etc/audit/plugins.d/$file`
if [ "X$diffrence" != "X" ];then
cp /etc/audisp/plugins.d/$file /etc/audit/plugins.d/$file
sed -i 's/\/etc\/audisp\/zos-remote\.conf/\/etc\/audit\/zos-remote\.conf/g' /etc/audit/plugins.d/$file
fi
fi
fi
done
fi
}

pre() {
if [ -d "/etc/audisp/" ];then
self_config_files_285=(syslog.conf au-remote.conf audispd-zos-remote.conf af_unix.conf)
plugins_config_files=`ls /etc/audisp/plugins.d/*.conf 2>/dev/null | wc -w`
if [ $plugins_config_files -gt 0 ];then
if [ ! -d /etc/audit/plugins.d/ ];then
mkdir -p /etc/audit/plugins.d/
fi

for file in `/usr/bin/ls /etc/audisp/plugins.d/*.conf`
do
if [[ " ${self_config_files_285} " =~ " `/usr/bin/basename $file` " ]];then
continue
else
if [ ! -f /etc/audit/plugins.d/`/usr/bin/basename $file` ];then
cp $file /etc/audit/plugins.d/
fi
fi
done
fi
fi

}

post() {
/sbin/ldconfig
files=`ls /etc/audit/rules.d/ 2>/dev/null | wc -w`
if [ "$files" -eq 0 ] ; then
if [ -e /usr/share/doc/audit/rules/10-no-audit.rules ] ; then
cp /usr/share/doc/audit/rules/10-no-audit.rules /etc/audit/rules.d/audit.rules
else
touch /etc/audit/rules.d/audit.rules
fi
chmod 0600 /etc/audit/rules.d/audit.rules
fi
if [ -d "/etc/audisp/" ];then
if [ -s "/etc/audisp/plugins.d/af_unix.conf" ];then
diffrence=`diff /etc/audisp/plugins.d/af_unix.conf /etc/audit/plugins.d/af_unix.conf`
if [ "X$diffrence" != "X" ];then
cp /etc/audisp/plugins.d/af_unix.conf /etc/audit/plugins.d/af_unix.conf
fi
fi
fi
%systemd_post auditd.service

}

preun() {
if [ $1 -eq 0 ] && [ -x /usr/bin/systemctl ]; then
/usr/bin/systemctl --no-reload disable auditd.service || :
fi
if [ $1 -eq 0 ]; then
/sbin/service auditd stop > /dev/null 2>&1
fi

}

postun() {
/sbin/ldconfig
if [ $1 -ge 1 ]; then
/sbin/service auditd condrestart > /dev/null 2>&1 || :
fi

}

