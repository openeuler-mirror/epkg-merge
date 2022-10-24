#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
autoreconf -ifv
%configure %%{env.configureFlags} LT_SYS_LIBRARY_PATH=%_libdir
%disable_rpath

%make_build

}

install() {
%make_install
%delete_la

replace ()
{
filename=$1
file=`basename "$filename"`
binary=${file%%.*}
pattern=${binary##bsd}

awk "
/^.Dt ${pattern^^} 1/ {
print \".Dt ${binary^^} 1\";
next;
}
!stop && /^.Nm $pattern/ {
print \".Nm $binary\" ;
stop = 1 ;
next;
}
1;
" "$filename" > "$filename.new"
mv "$filename".new "$filename"
}

for manpage in bsdtar.1 bsdcpio.1
do
installed_manpage=`find "$RPM_BUILD_ROOT" -name "$manpage"`
replace "$installed_manpage"
done

}

check() {
%if %{with check}
logfiles ()
{
find -name '*_test.log' -or -name test-suite.log
}

tempdirs ()
{
cat `logfiles` \
        | awk "match(\$0, /[^[:space:]]*`date -I`[^[:space:]]*/) { print substr(\$0, RSTART, RLENGTH); }" \
        | sort | uniq
}

cat_logs ()
{
for i in `logfiles`
do
echo "=== $i ==="
cat "$i"
done
}

run_testsuite ()
{
rc=0
%make_build check -j1 || {
# error happened - try to extract in koji as much info as possible
cat_logs

for i in `tempdirs`; do
if test -d "$i" ; then
find $i -printf "%p\n    ~> a: %a\n    ~> c: %c\n    ~> t: %t\n    ~> %s B\n"
cat $i/*.log
fi
done
return 1
}
cat_logs
}

run_testsuite

%endif

}

