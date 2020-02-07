NetTK
=====

The Network Tool Kit.

## Overview
NetTK is a modular and open source approach to monitoring network statistics. It was born due to my ISP having what I dubbed "frequent micro outages". While attempting to investigate the cause of the problem, and determine whether it was my own router/modem or their network, I discovered that there was no good tool for this purpose. Some tools claim to solve this issue, but are rigid and cost money. Often times, they ran only on one platform or would only allow you to perform a ping to specific places.

Another stumbling block was that most network monitoring tools (such as Nagios) focus on if the service is up or not. They don't deal well with the frequent micro outages that I was seeing.

Due to this, I decided to write my own network monitoring application and release to everyone for free use. I also worked on making it a modular framework so that others could easily write their own testing engines and analytic engines. Finally, I wrote it in Python so that it is cross platform and stable.

## Requirements
NetTK has the following requirements:

1. Python
2. matplotlib python library
3. scapy python library

## Platforms

NetTK was developed and tested on Linux. Theoretically, Unix should work just fine. Mac OS might be a bit more involved to get running (not a Mac guy), and I know Windows is involved to get running. For detailed install help, please see the wiki.

## Installation

1. Grab the latest copy of NetTK
  * Click "Download as ZIP" -- or --
  * git clone https://github.com/Owlz/NetTK.git
2. Make sure you have the latest copy of Python (https://www.python.org/downloads/)
  * Ubuntu: ```> sudo apt-get install python3```
3. Install the python dependencies
  * Ubuntu: ```> sudo apt-get install python3-matplotlib python3-scapy```

## Quick Start

Start it up with the following:

```shell
> sudo python3 ./netTK.py
```
This needs to be root (sudo'd) because SCAPY will not work properly without it.

Next, start up your analysis with the following:

```shell
> python3 ./netTKAnalysis.py
```

You should start seeing a line graph depicting your ping packet delay times to slashdot compared to delay times to google.

## Running It
NetTK is broken down into two components: monitor and analysis.

### Monitor

Monitor modules are configurable through the netTK.cfg file. Every module will record latency and dropped packets for it's particular area, but will differ by what it is checking. For instance, one module will allow you to constantly ICMP Echo Request (ping) a host, while another will allow you to contantly TCP SYN test a host.

The netTK.cfg file follows this basic format:

```
; [Title] -- This is for your readability, not used anywhere
; host -- (standard) DNS/IP of the host to test
; alias -- (standard) Alias of the host to use. This will be what the sqltable name uses
; module -- (standard) The type of test to use on this host. This is how NetTK decides what to do with the host. For example, "ping".
; ctag -- (optional) Optional tag to be used for defining save table name. Table name becomes "alias_module[_tag]". Useful when module is "tcpping" to keep track of  port/options/etc.
; attributes -- (This can vary by module)
```

For specific variables with respect to any given module, check either the Wiki or the corresponding "example.cfg" file (i.e.: monitor/ping.example.cfg).

### Analysis

The analysis modules let you look at the information you have gathered with the monitor modules in interesting ways. These are also configurable in a plain text way from netTKAnalysis.cfg. It follows the following form:

```
; [Engine] -- This defines what analysis engine you want to use (these are what is under analysis/*)
; alias_x -- (standard) the alias name to use (take this from the NetTK.cfg file)
; module_x -- (standard) The type of test that was used on this host. For example, "ping".
; ctag_x -- (optional) Optional tag to be used for defining save table name. Table name becomes "alias_module[_tag]". Useful when module is "tcpping" to keep track of  port/options/etc.
; attributes -- (This can vary by engine)
```

As with the monitor modules, the analysis module example config files can be found under analysis/module.example.cfg.

### Start it

One you have your monitor and analysis cfg files modified, all you have to do to run it is:

```shell
> sudo python3 ./netTK.py
```

And then to start your analysis:

```shell
> python3 ./netTKAnalysis.py
```
