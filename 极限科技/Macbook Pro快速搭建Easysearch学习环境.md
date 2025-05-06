---
title: Macbook Pro快速搭建Easysearch学习环境
date: 2025-03-25 20:46:04
tags: []
categories: [极限科技]
---
# 极限科技

在学习过程中，我们有时身边没有可用的服务器，这时就需要借助自己的 Mac 来安装和学习 Easysearch。然而，Easysearch 官网并未提供 Mac 版本的安装教程，下面我将详细整理我在 Mac 上安装和使用 Easysearch 的折腾经历。![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e549bc7f2a41481e8c7a49817bf9d76d.png)

### Easysearch

Easysearch 的运行依赖于 Java，程序启动时会自动从当前目录的 JDK 中查找 Java 环境。因此，即便环境变量中已经配置了 Java，程序也可能无法找到。针对这个问题，有两种解决办法：
下载 JDK 的二进制文件，将其重命名为 “jdk”，并放置在 Easysearch 的根目录下。
下载 Easysearch 的 bundle 包，该包会自带一个 JDK。下载链接为：https://release.infinilabs.com/Easysearch/stable/bundle/
安装步骤如下：首先执行初始化脚本，此脚本会设置 TLS 证书和集群密码。在执行脚本之前，log 目录为空。

```bash
bin/initialize.sh

                                 @@@@@@@@@@@
                                @@@@@@@@@@@@
                                @@@@@@@@@@@@
                               @@@@@@@@@&@@@
                              #@@@@@@@@@@@@@
        @@@                   @@@@@@@@@@@@@
       &@@@@@@@              &@@@@@@@@@@@@@
       @&@@@@@@@&@           @@@&@@@@@@@&@
      @@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@@&   @@@@@@@@@@@@@
        %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@&@@@@@@@@@@@@@@@
    @@         ,@@@@@@@@@@@@@@@@@@@@@@@&
    @@@@@.         @@@@@&@@@@@@@@@@@@@@
   @@@@@@@@@@          @@@@@@@@@@@@@@@#
   @&@@@&@@@&@@@          &@&@@@&@@@&@
  @@@@@@@@@@@@@.              @@@@@@@*
  @@@@@@@@@@@@@                  %@@@
 @@@@@@@@@@@@@
/@@@@@@@&@@@@@
@@@@@@@@@@@@@
@@@@@@@@@@@@@
@@@@@@@@@@@@        Welcome to INFINI Labs!


Now attempting the initializing...

RISK WARNING: The initialization script will overwrite certificates and passwords. If this is not the first run, please acknowledge the risks before proceeding. This is a dangerous operation. Do you want to proceed? [y/N]:y

NOTICE: Do you want to log credentials to /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/logs/initialize.log? Default is no logging. Press Enter to skip. [y/N]:y
Using bundled JDK at /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/jdk

Certificate request self-signature ok
subject=C = IN, ST = FI, L = NI, O = ORG, OU = UNIT, CN = infini.cloud
Certificate request self-signature ok
subject=C = IN, ST = FI, L = NI, O = ORG, OU = UNIT, CN = admin.infini.cloud
                DNS:infini.cloud, DNS:*.infini.cloud
                DNS:infini.cloud, DNS:*.infini.cloud

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    NOTICE: Please remember the bootstrap credential for further usage    @
@                        admin:db3e19a8c1c9f7755763                        @
@    Usage:  curl -ku admin:db3e19a8c1c9f7755763 https://localhost:9200    @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Your plugins directory is not empty. Please install the plugin manually.


Initialization successful! [Easysearch] is ready to use!


----------------------------------------------------------------
cd /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle && bin/Easysearch
----------------------------------------------------------------


   __ _  __ ____ __ _  __ __
  / // |/ // __// // |/ // /
 / // || // _/ / // || // /
/_//_/|_//_/  /_//_/|_//_/

©INFINI.LTD, All Rights Reserved.
```

这里打印了集群的密码和连接信息：

```bash
curl -ku admin:db3e19a8c1c9f7755763 https://localhost:9200
```

然后启动集群，默认监听在 9200 端口：

```bash
❰xu❙~/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle❱✔≻ bin/Easysearch        (base) 13:50:14
[2025-02-11T13:50:28,686][WARN ][o.e.b.Natives            ] [xudeMacBook-Pro.local] unable to load JNA native support library, native methods will be disabled.
java.lang.UnsatisfiedLinkError: /Users/xu/Library/Caches/JNA/temp/jna114104068097844929.tmp: dlopen(/Users/xu/Library/Caches/JNA/temp/jna114104068097844929.tmp, 0x0001): tried: '/Users/xu/Library/Caches/JNA/temp/jna114104068097844929.tmp' (fat file, but missing compatible architecture (have 'i386,x86_64', need 'arm64e' or 'arm64')), '/System/Volumes/Preboot/Cryptexes/OS/Users/xu/Library/Caches/JNA/temp/jna114104068097844929.tmp' (no such file), '/Users/xu/Library/Caches/JNA/temp/jna114104068097844929.tmp' (fat file, but missing compatible architecture (have 'i386,x86_64', need 'arm64e' or 'arm64'))
	at jdk.internal.loader.NativeLibraries.load(Native Method) ~[?:?]
	at jdk.internal.loader.NativeLibraries$NativeLibraryImpl.open(Unknown Source) ~[?:?]
	at jdk.internal.loader.NativeLibraries.loadLibrary(Unknown Source) ~[?:?]
	at jdk.internal.loader.NativeLibraries.loadLibrary(Unknown Source) ~[?:?]
	at java.lang.ClassLoader.loadLibrary(Unknown Source) ~[?:?]
	at java.lang.Runtime.load0(Unknown Source) ~[?:?]
	at java.lang.System.load(Unknown Source) ~[?:?]
	at com.sun.jna.Native.loadNativeDispatchLibraryFromClasspath(Native.java:1018) ~[jna-5.5.0.jar:5.5.0 (b0)]
	at com.sun.jna.Native.loadNativeDispatchLibrary(Native.java:988) ~[jna-5.5.0.jar:5.5.0 (b0)]
	at com.sun.jna.Native.<clinit>(Native.java:195) ~[jna-5.5.0.jar:5.5.0 (b0)]
	at java.lang.Class.forName0(Native Method) ~[?:?]
	at java.lang.Class.forName(Unknown Source) ~[?:?]
	at org.Easysearch.bootstrap.Natives.<clinit>(Natives.java:30) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.bootstrap.Bootstrap.initializeNatives(Bootstrap.java:95) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.bootstrap.Bootstrap.setup(Bootstrap.java:163) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.bootstrap.Bootstrap.init(Bootstrap.java:378) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.bootstrap.Easysearch.init(Easysearch.java:169) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.bootstrap.Easysearch.execute(Easysearch.java:160) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:71) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.cli.Command.mainWithoutErrorHandling(Command.java:112) ~[Easysearch-cli-1.10.1.jar:1.10.1]
	at org.Easysearch.cli.Command.main(Command.java:75) ~[Easysearch-cli-1.10.1.jar:1.10.1]
	at org.Easysearch.bootstrap.Easysearch.main(Easysearch.java:125) ~[Easysearch-1.10.1.jar:1.10.1]
	at org.Easysearch.bootstrap.Easysearch.main(Easysearch.java:67) ~[Easysearch-1.10.1.jar:1.10.1]
[2025-02-11T13:50:28,689][WARN ][o.e.b.Natives            ] [xudeMacBook-Pro.local] cannot check if running as root because JNA is not available
[2025-02-11T13:50:28,689][WARN ][o.e.b.Natives            ] [xudeMacBook-Pro.local] cannot install system call filter because JNA is not available
[2025-02-11T13:50:28,689][WARN ][o.e.b.Natives            ] [xudeMacBook-Pro.local] cannot register console handler because JNA is not available
[2025-02-11T13:50:28,690][WARN ][o.e.b.Natives            ] [xudeMacBook-Pro.local] cannot getrlimit RLIMIT_NPROC because JNA is not available
[2025-02-11T13:50:28,690][WARN ][o.e.b.Natives            ] [xudeMacBook-Pro.local] cannot getrlimit RLIMIT_AS because JNA is not available
[2025-02-11T13:50:28,690][WARN ][o.e.b.Natives            ] [xudeMacBook-Pro.local] cannot getrlimit RLIMIT_FSIZE because JNA is not available
[2025-02-11T13:50:28,757][INFO ][o.e.n.Node               ] [xudeMacBook-Pro.local] version[1.10.1], pid[18338], build[default/tar/1505f74d355bb2bac84162077fe66e9a32fc1be2/2025-01-24T21:02:00.632579Z], OS[Mac OS X/15.3/aarch64], JVM[Azul Systems, Inc./OpenJDK 64-Bit Server VM/17.0.13/17.0.13+11-LTS]
[2025-02-11T13:50:28,757][INFO ][o.e.n.Node               ] [xudeMacBook-Pro.local] JVM home [/Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/jdk]
[2025-02-11T13:50:28,758][INFO ][o.e.n.Node               ] [xudeMacBook-Pro.local] JVM arguments [-Xshare:auto, -Des.networkaddress.cache.ttl=60, -Des.networkaddress.cache.negative.ttl=10, -XX:+AlwaysPreTouch, -Xss1m, -Djava.awt.headless=true, -Dfile.encoding=UTF-8, -Djna.nosys=true, -XX:-OmitStackTraceInFastThrow, -XX:+ShowCodeDetailsInExceptionMessages, -Dio.netty.noUnsafe=true, -Dio.netty.noKeySetOptimization=true, -Dio.netty.recycler.maxCapacityPerThread=0, -Dio.netty.allocator.numDirectArenas=0, -Dlog4j.shutdownHookEnabled=false, -Dlog4j2.disable.jmx=true, -Xms1g, -Xmx1g, -XX:+UseG1GC, -XX:G1ReservePercent=25, -XX:InitiatingHeapOccupancyPercent=30, -Djava.io.tmpdir=/var/folders/ft/rfbtvz_n5l9dg007x5lsk7jw0000gn/T/Easysearch-134350959148498936, -Djava.security.manager=allow, -Djava.locale.providers=SPI,COMPAT, -XX:+HeapDumpOnOutOfMemoryError, -XX:HeapDumpPath=data, -XX:ErrorFile=logs/hs_err_pid%p.log, -Xlog:gc*,gc+age=trace,safepoint:file=logs/gc.log:utctime,pid,tags:filecount=32,filesize=64m, -XX:MaxDirectMemorySize=536870912, -Des.path.home=/Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle, -Des.path.conf=/Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config, -Des.distribution.flavor=oss, -Des.distribution.type=tar, -Des.bundled_jdk=false]
[2025-02-11T13:50:29,116][INFO ][c.i.s.s.t.SSLConfig      ] [xudeMacBook-Pro.local] SSL dual mode is disabled
[2025-02-11T13:50:29,117][INFO ][c.i.s.SecurityPlugin     ] [xudeMacBook-Pro.local] ES Config path is /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config
[2025-02-11T13:50:29,184][INFO ][c.i.s.s.DefaultSecurityKeyStore] [xudeMacBook-Pro.local] JVM supports TLSv1.3
[2025-02-11T13:50:29,185][INFO ][c.i.s.s.DefaultSecurityKeyStore] [xudeMacBook-Pro.local] Config directory is /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config/, from there the key- and truststore files are resolved relatively
[2025-02-11T13:50:29,389][INFO ][c.i.s.s.DefaultSecurityKeyStore] [xudeMacBook-Pro.local] TLS Transport Client Provider : JDK
[2025-02-11T13:50:29,389][INFO ][c.i.s.s.DefaultSecurityKeyStore] [xudeMacBook-Pro.local] TLS Transport Server Provider : JDK
[2025-02-11T13:50:29,389][INFO ][c.i.s.s.DefaultSecurityKeyStore] [xudeMacBook-Pro.local] TLS HTTP Provider             : JDK
[2025-02-11T13:50:29,389][INFO ][c.i.s.s.DefaultSecurityKeyStore] [xudeMacBook-Pro.local] Enabled TLS protocols for transport layer : [TLSv1.3, TLSv1.2]
[2025-02-11T13:50:29,389][INFO ][c.i.s.s.DefaultSecurityKeyStore] [xudeMacBook-Pro.local] Enabled TLS protocols for HTTP layer      : [TLSv1.3, TLSv1.2]
[2025-02-11T13:50:29,391][INFO ][c.i.s.SecurityPlugin     ] [xudeMacBook-Pro.local] Clustername: Easysearch
[2025-02-11T13:50:29,745][INFO ][o.e.j.JobSchedulerPlugin ] [xudeMacBook-Pro.local] Loaded scheduler extension: Easysearch-index-management, index: .Easysearch-ilm-config
[2025-02-11T13:50:29,748][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [aggs-matrix-stats]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [analysis-common]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [custom-codecs]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [geo]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [job-scheduler]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [lang-expression]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [lang-mustache]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [lang-painless]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [mapper-extras]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [parent-join]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [percolator]
[2025-02-11T13:50:29,749][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [rank-eval]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [reindex]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [repository-s3]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [repository-url]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [security]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded module [transport-netty4]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [analysis-icu]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [analysis-ik]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [analysis-pinyin]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [analysis-stconvert]
[2025-02-11T13:50:29,750][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [cross-cluster-replication]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [index-management]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [ingest-common]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [ingest-geoip]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [ingest-user-agent]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [knn]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [mapper-annotated-text]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [mapper-murmur3]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [mapper-size]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [sql]
[2025-02-11T13:50:29,751][INFO ][o.e.p.PluginsService     ] [xudeMacBook-Pro.local] loaded plugin [transport-nio]
[2025-02-11T13:50:29,759][INFO ][c.i.s.SecurityPlugin     ] [xudeMacBook-Pro.local] Disabled https compression by default to mitigate BREACH attacks. You can enable it by setting 'http.compression: true' in Easysearch.yml
[2025-02-11T13:50:29,767][INFO ][o.e.e.NodeEnvironment    ] [xudeMacBook-Pro.local] using [1] data paths, mounts [[/System/Volumes/Data (/dev/disk3s5)]], net usable_space [57gb], net total_space [926.3gb], types [apfs]
[2025-02-11T13:50:29,767][INFO ][o.e.e.NodeEnvironment    ] [xudeMacBook-Pro.local] heap size [1gb], compressed ordinary object pointers [true]
[2025-02-11T13:50:29,784][INFO ][o.e.n.Node               ] [xudeMacBook-Pro.local] node name [xudeMacBook-Pro.local], node ID [w5zzEDPfTDSE30HWYkUNcw], cluster name [Easysearch], roles [master, remote_cluster_client, data, ingest]
[2025-02-11T13:50:30,915][WARN ][c.i.s.c.Salt             ] [xudeMacBook-Pro.local] If you plan to use field masking pls configure compliance salt e1ukloTxxxOgPquJ to be a random string of 16 chars length identical on all nodes
[2025-02-11T13:50:30,921][INFO ][c.i.s.a.i.AuditLogging   ] [xudeMacBook-Pro.local] Message routing enabled: true
[2025-02-11T13:50:30,945][INFO ][c.i.s.f.SecurityFilter   ] [xudeMacBook-Pro.local] <NONE> indices are made immutable.
[2025-02-11T13:50:31,104][INFO ][o.e.t.NettyAllocator     ] [xudeMacBook-Pro.local] creating NettyAllocator with the following configs: [name=unpooled, suggested_max_allocation_size=256kb, factors={es.unsafe.use_unpooled_allocator=null, g1gc_enabled=true, g1gc_region_size=1mb, heap_size=1gb}]
[2025-02-11T13:50:31,132][INFO ][o.e.d.DiscoveryModule    ] [xudeMacBook-Pro.local] using discovery type [zen] and seed hosts providers [settings]
[2025-02-11T13:50:31,250][WARN ][o.e.g.DanglingIndicesState] [xudeMacBook-Pro.local] gateway.auto_import_dangling_indices is disabled, dangling indices will not be automatically detected or imported and must be managed manually
[2025-02-11T13:50:31,335][WARN ][o.e.r.MethodHandlers     ] [xudeMacBook-Pro.local] replace existing handler for [/{index}/_search] for method: GET existing:com.infinilabs.security.filter.SecurityRestFilter$1@41fbe8c0 to com.infinilabs.security.filter.SecurityRestFilter$1@1e8fd198
[2025-02-11T13:50:31,335][WARN ][o.e.r.MethodHandlers     ] [xudeMacBook-Pro.local] replace existing handler for [/{index}/_search] for method: POST existing:com.infinilabs.security.filter.SecurityRestFilter$1@4f75c627 to com.infinilabs.security.filter.SecurityRestFilter$1@1631a614
[2025-02-11T13:50:31,344][INFO ][o.e.n.Node               ] [xudeMacBook-Pro.local] initialized
[2025-02-11T13:50:31,344][INFO ][o.e.n.Node               ] [xudeMacBook-Pro.local] starting ...
[2025-02-11T13:50:31,345][INFO ][o.e.i.r.a.s.RollupListener] [xudeMacBook-Pro.local] Rollup listener start
[2025-02-11T13:50:31,391][INFO ][o.e.t.TransportService   ] [xudeMacBook-Pro.local] publish_address {127.0.0.1:9300}, bound_addresses {[::1]:9300}, {127.0.0.1:9300}
[2025-02-11T13:50:31,473][WARN ][o.e.b.BootstrapChecks    ] [xudeMacBook-Pro.local] system call filters failed to install; check the logs and fix your configuration or disable system call filters at your own risk
[2025-02-11T13:50:31,473][WARN ][o.e.b.BootstrapChecks    ] [xudeMacBook-Pro.local] the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
[2025-02-11T13:50:31,477][INFO ][o.e.c.c.ClusterBootstrapService] [xudeMacBook-Pro.local] no discovery configuration found, will perform best-effort cluster bootstrapping after [3s] unless existing master is discovered
[2025-02-11T13:50:34,481][INFO ][o.e.c.c.Coordinator      ] [xudeMacBook-Pro.local] setting initial configuration to VotingConfiguration{w5zzEDPfTDSE30HWYkUNcw}
[2025-02-11T13:50:34,576][INFO ][o.e.c.s.MasterService    ] [xudeMacBook-Pro.local] elected-as-master ([1] nodes joined)[{xudeMacBook-Pro.local}{w5zzEDPfTDSE30HWYkUNcw}{KMu1pbs-RB2vaWucEO8dmg}{127.0.0.1}{127.0.0.1:9300}{dimr} elect leader, _BECOME_MASTER_TASK_, _FINISH_ELECTION_], term: 1, version: 1, delta: master node changed {previous [], current [{xudeMacBook-Pro.local}{w5zzEDPfTDSE30HWYkUNcw}{KMu1pbs-RB2vaWucEO8dmg}{127.0.0.1}{127.0.0.1:9300}{dimr}]}
[2025-02-11T13:50:34,601][INFO ][o.e.c.c.CoordinationState] [xudeMacBook-Pro.local] cluster UUID set to [kJHbUT_zT2ionNVL9f3raQ]
[2025-02-11T13:50:34,623][INFO ][o.e.c.s.ClusterApplierService] [xudeMacBook-Pro.local] master node changed {previous [], current [{xudeMacBook-Pro.local}{w5zzEDPfTDSE30HWYkUNcw}{KMu1pbs-RB2vaWucEO8dmg}{127.0.0.1}{127.0.0.1:9300}{dimr}]}, term: 1, version: 1, reason: Publication{term=1, version=1}
[2025-02-11T13:50:34,627][INFO ][o.e.i.i.ManagedIndexCoordinator] [xudeMacBook-Pro.local] Cache cluster manager node onClusterManager time: 1739253034627
[2025-02-11T13:50:34,637][INFO ][o.e.h.AbstractHttpServerTransport] [xudeMacBook-Pro.local] publish_address {127.0.0.1:9200}, bound_addresses {[::1]:9200}, {127.0.0.1:9200}
[2025-02-11T13:50:34,640][INFO ][o.e.n.Node               ] [xudeMacBook-Pro.local] started
[2025-02-11T13:50:34,640][INFO ][c.i.s.SecurityPlugin     ] [xudeMacBook-Pro.local] Node started
[2025-02-11T13:50:34,640][INFO ][c.i.s.c.ConfigurationRepository] [xudeMacBook-Pro.local] Will attempt to create index .security and default configs if they are absent
[2025-02-11T13:50:34,641][INFO ][c.i.s.SecurityPlugin     ] [xudeMacBook-Pro.local] 3 Security modules loaded so far: [Module [type=REST_MANAGEMENT_API, implementing class=com.infinilabs.security.dlic.rest.api.SecurityRestApiActions], Module [type=MULTITENANCY, implementing class=com.infinilabs.security.configuration.PrivilegesInterceptorImpl], Module [type=AUDITLOG, implementing class=com.infinilabs.security.auditlog.impl.AuditLogging]]
[2025-02-11T13:50:34,641][INFO ][c.i.s.c.ConfigurationRepository] [xudeMacBook-Pro.local] Background init thread started. Install default config?: true
[2025-02-11T13:50:34,645][INFO ][c.i.s.c.ConfigurationRepository] [xudeMacBook-Pro.local] Wait for cluster to be available ...
[2025-02-11T13:50:34,670][INFO ][o.e.g.GatewayService     ] [xudeMacBook-Pro.local] recovered [0] indices into cluster_state
[2025-02-11T13:50:36,676][INFO ][o.w.a.d.Dictionary       ] [xudeMacBook-Pro.local] try load config from /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config/analysis-ik/IKAnalyzer.cfg.xml
[2025-02-11T13:50:37,465][INFO ][o.e.c.m.MetadataCreateIndexService] [xudeMacBook-Pro.local] [.security] creating index, cause [api], templates [], shards [1]/[1]
[2025-02-11T13:50:37,470][INFO ][o.e.c.r.a.AllocationService] [xudeMacBook-Pro.local] updating number_of_replicas to [0] for indices [.security]
[2025-02-11T13:50:37,657][INFO ][o.e.c.r.a.AllocationService] [xudeMacBook-Pro.local] Cluster health status changed from [YELLOW] to [GREEN] (reason: [shards started [[.security][0]]]).
[2025-02-11T13:50:37,679][INFO ][c.i.s.c.ConfigurationRepository] [xudeMacBook-Pro.local] Index .security created?: true
[2025-02-11T13:50:37,685][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Will update 'config' with /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config/security/config.yml and populate it with empty doc if file missing and populateEmptyIfFileMissing=false
[2025-02-11T13:50:37,720][INFO ][o.e.c.m.MetadataMappingService] [xudeMacBook-Pro.local] [.security/ADtiL1q3TUiUghNCrlfrHQ] create_mapping [_doc]
[2025-02-11T13:50:37,779][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Doc with id 'config' and version 2 is updated in .security index.
[2025-02-11T13:50:37,780][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Will update 'role' with /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config/security/role.yml and populate it with empty doc if file missing and populateEmptyIfFileMissing=false
[2025-02-11T13:50:37,786][INFO ][o.e.c.m.MetadataMappingService] [xudeMacBook-Pro.local] [.security/ADtiL1q3TUiUghNCrlfrHQ] update_mapping [_doc]
[2025-02-11T13:50:37,830][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Doc with id 'role' and version 2 is updated in .security index.
[2025-02-11T13:50:37,831][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Will update 'role_mapping' with /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config/security/role_mapping.yml and populate it with empty doc if file missing and populateEmptyIfFileMissing=false
[2025-02-11T13:50:37,838][INFO ][o.e.c.m.MetadataMappingService] [xudeMacBook-Pro.local] [.security/ADtiL1q3TUiUghNCrlfrHQ] update_mapping [_doc]
[2025-02-11T13:50:37,885][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Doc with id 'role_mapping' and version 2 is updated in .security index.
[2025-02-11T13:50:37,886][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Will update 'user' with /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config/security/user.yml and populate it with empty doc if file missing and populateEmptyIfFileMissing=false
[2025-02-11T13:50:37,898][INFO ][o.e.c.m.MetadataMappingService] [xudeMacBook-Pro.local] [.security/ADtiL1q3TUiUghNCrlfrHQ] update_mapping [_doc]
[2025-02-11T13:50:37,937][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Doc with id 'user' and version 2 is updated in .security index.
[2025-02-11T13:50:37,937][INFO ][c.i.s.s.ConfigHelper     ] [xudeMacBook-Pro.local] Will update 'privilege' with /Users/xu/Desktop/es/Easysearch-1.10.1-1978-mac-arm64-bundle/config/security/privilege.yml and populate it with empty doc if file missing and populateEmptyIfFileMissing=false

```

使用 Postman 尝试连接，可以正常返回 HTTP 的响应：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/59507653bfb74e90bab4f21b2b0adc73.png)

这里就需要用到上次的那个密码，默认存放在 log/initialize.log 下。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/32a54c5760464860858e5ada2c08c98b.png)

### Console

下载二进制文件并且运行，服务监听在 9000 端口，通过这个页面连接 Easysearch，用来替代 kibana，个人觉得比 kibana 和 OpenSearch Dashboard 要好用，除了 Easysearch 之外，还可以连接 ES 和 OpenSearch。

```bash
./console-mac-arm64             (base) 14:25:43

   ___  ___    __  __    ___  __   __
  / __\/___\/\ \ \/ _\  /___\/ /  /__\
 / /  //  //  \/ /\ \  //  // /  /_\
/ /__/ \_// /\  / _\ \/ \_// /__//__
\____|___/\_\ \/  \__/\___/\____|__/

HOME: https://github.com/infinilabs/console/

[CONSOLE] The easiest way to operate your own search platform, open-sourced under the GNU AGPLv3.
[CONSOLE] 1.28.1#1978, 2025-01-25 11:40:24, 2025-12-31 10:10:10, b189b72c11a9, 8ecefd18d9eb, c511f8f4cab9
[02-11 14:25:47] [INF] [env.go:216] configuration auto reload enabled
[02-11 14:25:47] [INF] [env.go:222] watching config: /Users/xu/Desktop/es/console-1.28.1-1978-mac-arm64/config
[02-11 14:25:47] [INF] [app.go:311] initializing console, pid: 20341
[02-11 14:25:47] [INF] [app.go:312] using config: /Users/xu/Desktop/es/console-1.28.1-1978-mac-arm64/console.yml
[02-11 14:25:47] [INF] [instance.go:100] workspace: /Users/xu/Desktop/es/console-1.28.1-1978-mac-arm64/data/console/nodes/culeqqr55o14utfde2a0
[02-11 14:25:47] [INF] [module.go:159] started module: badger
[02-11 14:25:47] [INF] [module.go:159] started module: kafka_queue
[02-11 14:25:47] [INF] [module.go:159] started module: setup
[02-11 14:25:47] [INF] [module.go:159] started module: setup
[02-11 14:25:47] [INF] [web.go:226] web server listen at: http://0.0.0.0:9000
[02-11 14:25:47] [INF] [module.go:159] started module: web
[02-11 14:25:47] [INF] [module.go:184] all modules are started
[02-11 14:25:47] [INF] [app.go:537] console is up and running now.
[02-11 14:28:03] [WRN] [schema.go:101] duplicated schema rbac-role, infini.sh/console/core/security-role
[02-11 14:28:03] [WRN] [schema.go:101] duplicated schema rbac-user, infini.sh/console/core/security-user
[02-11 14:28:03] [WRN] [schema.go:101] duplicated schema credential, infini.sh/framework/core/credential-credential
[02-11 14:28:04] [INF] [module.go:187] loading [0] remote configs
[02-11 14:28:04] [INF] [pipeline.go:418] creating pipeline: merge_metrics
[02-11 14:28:04] [INF] [pipeline.go:418] creating pipeline: metadata_ingest
[02-11 14:28:04] [INF] [pipeline.go:418] creating pipeline: activity_ingest
[02-11 14:28:04] [INF] [pipeline.go:418] creating pipeline: merge_logging
[02-11 14:28:04] [INF] [pipeline.go:418] creating pipeline: merge_audit_log
[02-11 14:28:04] [INF] [pipeline.go:418] creating pipeline: ingest_merged_requests
[02-11 14:28:04] [INF] [load.go:69] loading permission file from /Users/xu/Desktop/es/console-1.28.1-1978-mac-arm64/config/permission.json
[02-11 14:28:06] [INF] [pipeline.go:227] config changed, checking for new pipeline configs, CREATE, config/system_config.yml
[02-11 14:54:38] [ERR] [v0.go:521] invalid response: https://localhost:9200/.infini_metrics%2A/_search,{"aggs":{"culf8bj55o14utfdf1u0":{"aggs":{"culf8bj55o14utfdf1ug":{"aggs":{"culf8bj55o14utfdf1v0":{"aggs":{},"terms":{"field":"payload.elasticsearch.cluster_health.status","missing":"","size":2}}},"date_range":{"field":"timestamp","format":"yyyy-MM-dd","ranges":[{"from":"now-13d/d","to":"now-12d/d"},{"from":"now-12d/d","to":"now-11d/d"},{"from":"now-11d/d","to":"now-10d/d"},{"from":"now-10d/d","to":"now-9d/d"},{"from":"now-9d/d","to":"now-8d/d"},{"from":"now-8d/d","to":"now-7d/d"},{"from":"now-7d/d","to":"now-6d/d"},{"from":"now-6d/d","to":"now-5d/d"},{"from":"now-5d/d","to":"now-4d/d"},{"from":"now-4d/d","to":"now-3d/d"},{"from":"now-3d/d","to":"now-2d/d"},{"from":"now-2d/d","to":"now-1d/d"},{"from":"now-1d/d","to":"now/d"},{"from":"now/d","to":"now"}],"time_zone":"+08:00"}}},"terms":{"field":"metadata.labels.cluster_id","size":2}}},"query":{"bool":{"filter":[{"range":{"timestamp":{"gte":"now-15d","lte":"now"}}}],"must":[{"terms":{"metadata.labels.cluster_id":["infini_default_system_cluster"]}},{"term":{"metadata.category":{"value":"elasticsearch"}}},{"term":{"metadata.name":{"value":"cluster_health"}}}]}},"size":0},{"error":{"root_cause":[{"type":"runtime_exception","reason":"Unable to unroll aggregation tree.  Aggregation [culf8bj55o14utfdf1u0] is of type [UnmappedTerms] which is currently unsupported."}],"type":"runtime_exception","reason":"Unable to unroll aggregation tree.  Aggregation [culf8bj55o14utfdf1u0] is of type [UnmappedTerms] which is currently unsupported."},"status":500}
[02-11 14:59:18] [ERR] [config.go:46] agent config not found: missing field accessing 'agent'
[02-11 14:59:18] [INF] [certs.go:49] auto generating cert files

```

![](https://i-blog.csdnimg.cn/direct/f5c1ef6500b24949b22c7aaff8c317b6.png)

查看集群信息，可以看指标，也可以看索引，kibana 有的功能这边基本都有：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/31e40aee35944b6fa7e6920ae065cd39.png)

同时提供 DSL 查询：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a8cf7751f52b4ea0a9ef59c769a27f58.png)

### Gateway

INFINI Gateway 是一个面向搜索场景的高性能数据网关，所有请求都经过网关处理后再转发到后端的搜索业务集群。基于 INFINI Gateway，可以实现索引级别的限速限流、常见查询的缓存加速、查询请求的审计、查询结果的动态修改等等。

Macbook 下有奇怪的安全规则，除了二进制文件之外，yml 文件经验也报错不安全。打开 “系统偏好设置”，进入 “安全性与隐私”，点击 “通用”，有 “仍然允许” 按钮，点击它即可。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/24aacd91ee854915acae12662b75f853.png)

然后按照 Easysearch 的配置进行修改，否则会连不上集群。就是这个报错：

```bash
./gateway-mac-arm64                 (base) 14:51:14

   ___   _   _____  __  __    __  _
  / _ \ /_\ /__   \/__\/ / /\ \ \/_\ /\_/\
 / /_\///_\\  / /\/_\  \ \/  \/ //_\\\_ _/
/ /_\\/  _  \/ / //__   \  /\  /  _  \/ \
\____/\_/ \_/\/  \__/    \/  \/\_/ \_/\_/

HOME: https://github.com/infinilabs/gateway/

[GATEWAY] A light-weight, powerful and high-performance search gateway, open-sourced under the GNU AGPLv3.
[GATEWAY] 1.28.1#1978, 2025-01-24 18:34:08, 2025-12-31 10:10:10, 93fd9e32500a, 8ecefd18d9eb, c511f8f4cab9
[02-11 14:51:17] [INF] [app.go:311] initializing gateway, pid: 22456
[02-11 14:51:17] [INF] [app.go:312] using config: /Users/xu/Desktop/es/gateway-1.28.1-1978-mac-arm64/gateway.yml
[02-11 14:51:17] [INF] [instance.go:100] workspace: /Users/xu/Desktop/es/gateway-1.28.1-1978-mac-arm64/data/gateway/nodes/culf6pb55o15fe01mtvg
panic: Get "http://localhost:9200": EOF

goroutine 433 [running]:
infini.sh/framework/modules/elastic/common.InitClientWithConfig({{{0x14000810630, 0x4}, 0x0, 0x0}, {0x103466e7c, 0x4}, {0x14000810630, 0x4}, {0x0, 0x0}, ...})
	/root/go/src/infini.sh/framework/modules/elastic/common/config.go:89 +0x880
infini.sh/framework/modules/elastic/common.InitElasticInstanceWithoutMetadata({{{0x14000810630, 0x4}, 0x0, 0x0}, {0x103466e7c, 0x4}, {0x14000810630, 0x4}, {0x0, 0x0}, ...})
	/root/go/src/infini.sh/framework/modules/elastic/common/config.go:199 +0x64
infini.sh/framework/modules/elastic.initElasticInstances({0x14000826008?, 0x1e?, 0x103670600?}, {0x103466e7c, 0x4})
	/root/go/src/infini.sh/framework/modules/elastic/module.go:194 +0x7c
infini.sh/framework/modules/elastic.(*ElasticModule).Setup(0x140006fa120?)
	/root/go/src/infini.sh/framework/modules/elastic/module.go:215 +0x124
infini.sh/framework/core/module.Start()
	/root/go/src/infini.sh/framework/core/module/module.go:123 +0x238
main.start()
	/root/go/src/infini.sh/gateway/main.go:72 +0x1c
infini.sh/framework.(*App).run(0x14000332500)
	/root/go/src/infini.sh/framework/app.go:493 +0x160
created by infini.sh/framework.(*App).Start in goroutine 1
	/root/go/src/infini.sh/framework/app.go:429 +0xb4
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ebcac27064884421860bbc6e60d2155b.png)
修改配置文件之后，启动日志如下：

```bash
./gateway-mac-arm64                 (base) 14:53:07

   ___   _   _____  __  __    __  _
  / _ \ /_\ /__   \/__\/ / /\ \ \/_\ /\_/\
 / /_\///_\\  / /\/_\  \ \/  \/ //_\\\_ _/
/ /_\\/  _  \/ / //__   \  /\  /  _  \/ \
\____/\_/ \_/\/  \__/    \/  \/\_/ \_/\_/

HOME: https://github.com/infinilabs/gateway/

[GATEWAY] A light-weight, powerful and high-performance search gateway, open-sourced under the GNU AGPLv3.
[GATEWAY] 1.28.1#1978, 2025-01-24 18:34:08, 2025-12-31 10:10:10, 93fd9e32500a, 8ecefd18d9eb, c511f8f4cab9
[02-11 14:53:16] [INF] [app.go:311] initializing gateway, pid: 22599
[02-11 14:53:16] [INF] [app.go:312] using config: /Users/xu/Desktop/es/gateway-1.28.1-1978-mac-arm64/gateway.yml
[02-11 14:53:16] [INF] [instance.go:100] workspace: /Users/xu/Desktop/es/gateway-1.28.1-1978-mac-arm64/data/gateway/nodes/culf6pb55o15fe01mtvg
[02-11 14:53:16] [INF] [module.go:159] started module: badger
[02-11 14:53:16] [INF] [api.go:214] local ips: 192.168.5.53
[02-11 14:53:16] [INF] [api.go:312] api server listen at: http://0.0.0.0:2900
[02-11 14:53:16] [INF] [module.go:159] started module: api
[02-11 14:53:16] [INF] [module.go:159] started module: disk_queue
[02-11 14:53:16] [INF] [actions.go:420] elasticsearch [logging-server] is available
[02-11 14:53:16] [INF] [module.go:159] started module: elasticsearch
[02-11 14:53:16] [INF] [module.go:159] started module: kafka_queue
[02-11 14:53:16] [INF] [module.go:159] started module: queue
[02-11 14:53:16] [INF] [module.go:159] started module: redis
[02-11 14:53:16] [INF] [module.go:159] started module: s3
[02-11 14:53:16] [INF] [module.go:159] started module: simple_stats
[02-11 14:53:16] [INF] [module.go:159] started module: task
[02-11 14:53:16] [INF] [actions.go:420] elasticsearch [prod] is available
[02-11 14:53:16] [INF] [pipeline.go:418] creating pipeline: pipeline_logging_merge
[02-11 14:53:16] [INF] [pipeline.go:418] creating pipeline: ingest_pipeline_logging
[02-11 14:53:16] [INF] [pipeline.go:418] creating pipeline: async_messages_merge
[02-11 14:53:16] [INF] [pipeline.go:418] creating pipeline: metrics_merge
[02-11 14:53:16] [INF] [pipeline.go:418] creating pipeline: request_logging_merge
[02-11 14:53:16] [INF] [pipeline.go:418] creating pipeline: ingest_merged_requests
[02-11 14:53:16] [INF] [pipeline.go:418] creating pipeline: async_ingest_bulk_requests
[02-11 14:53:16] [INF] [module.go:159] started module: pipeline
[02-11 14:53:16] [INF] [module.go:178] started plugin: floating_ip
[02-11 14:53:16] [INF] [module.go:178] started plugin: force_merge
[02-11 14:53:16] [INF] [module.go:178] started plugin: metrics
[02-11 14:53:16] [INF] [module.go:178] started plugin: statsd
[02-11 14:53:17] [INF] [reverseproxy.go:299] elasticsearch [prod] hosts: [] => [127.0.0.1:9200]
[02-11 14:53:17] [INF] [entry.go:420] entry [my_es_entry] listen at: http://0.0.0.0:8000
[02-11 14:53:17] [INF] [module.go:178] started plugin: gateway
[02-11 14:53:17] [INF] [module.go:184] all modules are started
[02-11 14:53:17] [INF] [app.go:537] gateway is up and running now.


```

认证之后，可以从 Gateway 代理到 Easysearch：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b30d52d702d34054a51c0717e0c8ba8a.png)

#### Gateway 注册到 Console

注册时候用的是 2900 端口，如果注册到 8000 是无法连接的。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2811c9077e0c497f9d3717b6778a27f6.png)

注册完成就会显示 Gateway 的信息：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6f80928712d7410b842013aaa825aa94.png)

本文围绕在 Mac 系统上安装、配置和使用 Easysearch 展开，详细介绍了各组件的安装过程、遇到的问题及解决办法，以下是详细总结：

### 1. 安装背景与前期准备

在学习阶段缺少服务器时，可使用 Mac 进行 Easysearch 的安装学习，但官网未提供 Mac 版安装教程。Easysearch 运行依赖 Java，程序启动时会从当前目录的 JDK 查找 Java，即便环境变量已配置也可能无法找到，解决办法有：一是下载 JDK 二进制文件，重命名为“jdk”放在 Easysearch 根目录；二是下载自带 JDK 的 Easysearch bundle 包。

### 2. Easysearch 安装与启动

- **初始化**：执行`bin/initialize.sh`脚本设置 TLS 证书和集群密码，初始化过程会提示覆盖证书和密码的风险，需确认是否继续，并可选择是否将凭证记录到日志文件。初始化成功后会显示集群的密码和连接信息，如`curl -ku admin:db3e19a8c1c9f7755763 https://localhost:9200`。
- **启动集群**：启动命令为`bin/Easysearch`，默认监听 9200 端口。启动过程中可能出现无法加载 JNA 本地支持库的警告，但不影响后续启动和使用。

### 3. 连接与验证

使用 Postman 尝试连接，需用到初始化时生成的密码（默认存放在`log/initialize.log`），可正常返回 HTTP 响应，验证了 Easysearch 集群的可访问性。

### 4. Console 使用

下载并运行二进制文件`./console-mac-arm64`，服务监听在 9000 端口，可替代 Kibana 连接 Easysearch、ES 和 OpenSearch。运行过程中会有部分警告信息，如重复的架构定义，但不影响基本功能使用，还可查看集群信息和进行 DSL 查询。

### 5. Gateway 使用

- **配置问题与解决**：INFINI Gateway 是高性能数据网关，Mac 上运行时可能因安全规则报错，需在“系统偏好设置 - 安全性与隐私 - 通用”中点击“仍然允许”。若配置不正确会出现连接不上集群的错误，修改配置文件后可正常启动。
- **启动与功能验证**：启动命令为`./gateway-mac-arm64`，启动后各模块和插件依次启动，可实现索引级别的限速限流、缓存加速、查询审计等功能。认证后可从 Gateway 代理到 Easysearch，还可将 Gateway 注册到 Console。
