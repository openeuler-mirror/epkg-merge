#!/usr/bash

pretrans:json-c-devel() {
-p <lua>
path = "%{_includedir}/%{name}"
st = posix.stat(path)
if st and st.type == "link" then
os.remove(path)
end

%ldconfig_scriptlets
}

