* Wed Aug 31 2022 yangchenguang <yangchenguang@uniontech.com> - 32:9.16.23-9
- DESC: fix downgrade bind-utils conflict bind-dnssec-doc

* Mon Aug 01 2022 jiangheng<jiangheng14@huawei.com> - 32:9.16.23-8
- Type:bugfix
- CVE:
- SUG:NA
- DESC:update version number to maximum and keep it same as 22.03

* Mon Jul 25 2022 jiangheng<jiangheng14@huawei.com> - 32:9.16.23-6
- Type:bugfix
- CVE:
- SUG:NA
- DESC:add missing dependencies
remove geopip-directory in named.conf

* Mon Jun 13 2022 jiangheng<jiangheng14@huawei.com> - 9.16.23-5
- Type:bugfix
- CVE:
- SUG:NA
- DESC:fix test cases timeout

* Thu Mar 31 2022 jiangheng<jiangheng12@huawei.com> - 9.16.23-4
- Type:bugfix
- CVE:
- SUG:NA
- DESC:add bind.yaml to master branch

* Wed Mar 30 2022 jiangheng<jiangheng12@huawei.com> - 9.16.23-3
- Type:CVE
- CVE:CVE-2021-25220
- SUG:NA
- DESC:fix CVE-2021-25220

* Wed Mar 30 2022 jiangheng<jiangheng12@huawei.com> - 9.16.23-2
- Type:CVE
- CVE:CVE-2022-0396
- SUG:NA
- DESC:fix CVE-2022-0396

* Thu Dec 02 2021 jiangheng<jiangheng12@huawei.com> - 9.16.23-1
- DESC:update to 9.16.23

* Wed Nov 17 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h9
- Type:CVE
- CVE:CVE-2021-25219
- SUG:NA
- DESC:fix CVE-2021-25219

* Wed Nov 03 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h8
- Type:CVE
- CVE:CVE-2021-25219
- SUG:NA
- DESC:fix CVE-2021-25219

* Tue Aug 03 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h7
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:give zspill its own lock
fix tasan error
fix data race
Correctly encode LOC records with non integer negative
isc_ratelimiter needs to hold a reference to its task
dig +bufsize=0 failed to disable EDNS as a side effect
Lock access to ctx->blocked as it is updated by multiple threads
Only read dns_master_indent and dns_master_indentstr in named
Defer read of zl->server and zl->reconfig
Break lock order loop by sending TAT in an event
Handle DNS_R_NCACHENXRRSET in fetch_callback_{dnskey,validator}()
Unload a zone if a transfer breaks its SOA record
Address inconsistencies in checking added RRsets
dns_rdata_tostruct() should reject rdata with DNS_RDATA_UPDATE set

* Fri Jun 04 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h6
- Type:bugfix
- CVE:
- SUG:NA
- DESC:set print-time default to yes

* Wed May 19 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h5
- Type:CVE
- CVE:CVE-2021-25214 CVE-2021-25215
- SUG:NA
- DESC:fix CVE-2021-25214 CVE-2021-25215

* Mon Apr 26 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h4
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:fix no response when execute rndc addzone command

* Mon Apr 12 2021 zhujunhao<zhujunhao8@huawei.com> - 9.11.21-4.h3
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:remove GeoIP and libdb

* Mon Apr 12 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h2
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:fix the upgrade installtion failure

* Wed Apr 07 2021 jiangheng<jiangheng12@huawei.com> - 9.11.21-4.h1
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:update version to 9.11.21-4.h1

* Wed Mar 10 2021 zhouyihang<zhouyihang3@huawei.com> - 9.11.4-17.h11
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:set geoip-use-ecs default to no

* Tue Mar 09 2021 yuboyun<yuboyun@huawei.com> - 9.11.4-17.h10
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:free rbuf
mempool didn t work for sizes less than sizeof void
Reset dig exit code after a TCP connection is establ
Prevent a race after zone load
Fix isc_buffer_copyregion for auto reallocated buffe
free tmpzonename and restart_master
errors initalizing badcaches were not caught or clea
set freed pointers to NULL
cleanup allocated memory on error
Fix a small memleak in delv
pass the correct object to cfg_obj_log
Try to fix crash at sigchase topdown
Do not fail on NULL passed to OpenSSL_free
error out if there are extra command line options
correct errno to result translation
properly detect period as last character in filename
fail if ctime output is truncted
Fix a race in fctx_cancelquery
add missing MAYBE_UNLOCK
Fix race in unix socket code when closing a socket t
fix Ed448 length values for precomputed ASN.1 prefix
don t overwrite the dns_master_loadfile result befor
address NULL pointer dereferences
address potential NULL pointer dereference
Prevent query loops for misbehaving servers
Lock di  manager buffer_lock before accessing b
Request exclusive access when crashing via fatal
Assign fctx client when fctx is created rather when
lock access to fctx nqueries
acquire task lock before calling push_readyq for tas
Call dns_dbiterator_destroy earlier to prevent poten
Handle catopen errors
Fixed crash when querying for non existing domain in
Fixed rebinding protection bug when using forwarder
initialize sockaddrdscp to prevent spurious output f
Lock access to answer to silence TSAN
Fix a data access race in resolver
Address race between zone_maintenance and dns_zone_s
rbtdb cleanup_dead_nodes should ignore alive nodes o
make sure new_zone_lock is locked before unlocking i
Prevent crash on dst initialization failure
IPSECKEY require non zero length public keys
NSEC3PARAM check that saltlen is consistent with the
A6 return FORMERR in fromwire if bits are non zero
Cast the original rcode to dns_ttl_t when setting ex
Lock on msg SELECT_POKE_CLOSE as it triggers a tsan
Lock access when updating reading manager epoll_even
Take complete ownership of aclp before calling destr
Take complete ownership of validatorp before calling
Address lock order inversion
It appears that you can t change what you are pollin
counter used was read without the lock being held
Missing locks in ns_lwresd_shutdown
Use atomics to update counters
Obtain a lock on the quota structure
The node lock was released too early
Address lock order inversion between the keytable an
Pause dbiterator to release rwlock to prevent lock o
Address lock order reversals when shutting down a vi
Hold qid lock when calling deref_portentry as
Lock zone before calling zone_namerd_tostr
Address TSAN error between dns_rbt_findnode and subt
Address data race in dns_stats_detach over reference
Lock check of DNS_ZONEFLG_EXITING flag

* Mon Feb 22 2021 zhouyihang<zhouyihang3@huawei.com> - 9.11.4-17.h9
- Type:CVE
- CVE:CVE-2020-8625
- SUG:NA
- DESC:fix CVE-2020-8625

* Mon Jan 4 2021 zhouyihang<zhouyihang3@huawei.com> - 9.11.4-17.h8
- Type:CVE
- CVE:CVE-2020-8619
- SUG:NA
- DESC:fix CVE-2020-8619

* Mon Dec 21 2020 xihaochen<xihaochen@huawei.com> - 9.11.4-17.h7
- Type:CVE
- CVE:CVE-2020-8624
- SUG:NA
- DESC:fix CVE-2020-8624

* Wed Dec 02 2020 yuboyun<yuboyun@huawei.com> - 9.11.4-17.h6
- Type:bugfix
- CVE:NA
- SUG:restart
- DESC:fix the difference at the macro definition using clock gettime instead of gettimeofday

* Wed Nov 18 2020 yuboyun<yuboyun@huawei.com> - 9.11.4-17.h5
- Type:CVE
- CVE:CVE-2020-8623
- SUG:restart
- DESC:fix CVE-2020-8623

* Tue Sep 22 2020 yuboyun<yuboyun@huawei.com> - 9.11.4-17.h4
- Type:CVE
- CVE:CVE-2020-8622
- SUG:NA
- DESC:add %patch6032 -p1 to fix CVE-2020-8622

* Wed Sep 16 2020 yuboyun<yuboyun@huawei.com> - 9.11.4-17.h3
- Type:CVE
- CVE:CVE-2020-8622
- SUG:restart
- DESC:fix CVE-2020-8622

* Tue Jun 09 2020 gaihuiying<gaihuiying1@huawei.com> - 9.11.4-17.h2
- Type:cves
- ID:CVE-2018-5744 CVE-2019-6467 CVE-2019-6471 CVE-2019-6477
- SUG:restart
- DESC:backport patch to fix CVE-2018-5744 CVE-2019-6467 CVE-2019-6471 CVE-2019-6477

* Thu May 28 2020 gaihuiying<gaihuiying1@huawei.com> - 9.11.4-17.h1
- Type:cves
- ID:CVE-2020-8616 CVE-2020-8617
- SUG:restart
- DESC:backport patch to fix CVE-2020-8616 CVE-2020-8617

* Tue Mar 31 2020 liaichun<liaichun@huawei.com> - 9.11.4-17
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: modify named.root.key permissions from 600 to 644

* Thu Mar 26 2020 liaichun<liaichun@huawei.com> - 9.11.4-16
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix  named service hangs and crashes

* Sat Mar 21 2020 liaichun<liaichun@huawei.com> - 9.11.4-15
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: modify key file permissions from 644 to 600

* Fri Mar 20 2020 wangli<wangli221@huawei.com> - 9.11.4-14
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:Reenable crypto rand for DHCP, disable just entropy check

* Thu Mar 19 2020 songnannan <songnannan2@huawei.com> - 9.11.4-13
- add gdb in buildrequires

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 9.11.4-12
- Package init
