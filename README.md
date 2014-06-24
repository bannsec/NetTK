NetTK
=====

The Network Tool Kit.

## Overview
NetTK is a modular and open source approach to monitoring network statistics. It was born due to my ISP having what I dubbed "frequent micro outages". While attempting to investigate the cause of the problem, and determine whether it was my own router/modem or their network, I discovered that there was no good tool for this purpose. Some tools claim to solve this issue, but are rigid and cost money. Often times, they ran only on one platform or would only allow you to perform a ping to specific places.

Another stumbling block was that most network monitoring tools (such as Nagios) focus on if the service is up or not. They don't deal well with the frequent micro outages that I was seeing.

Due to this, I decided to write my own network monitoring application and release to everyone for free use. I also worked on making it a modular framework so that others could easily write their own testing engines and analytic engines. Finally, I wrote it in Python so that it is cross platform and stable.

## Requirements
NetTK has the following requirements:

1. Python 2.7.x
   * I'm unable to use 3.x due to the SCAPY library I'm using not being ported to Python 3.x

## Installation

1. Grab the latest copy of NetTK
  * Click "Download as ZIP" -- or --
  * git clone https://github.com/Owlz/NetTK.git
2. Make sure you have the latest copy of Python 2.7 (https://www.python.org/downloads/)
3. Install the dependencies
  * python matplotlib
  * python scapy

## Quick Start

To get started quickly (after installing), try this:

Edit the netTK.cfg file to the following:

```
[SQLite Database Handler]
module = sqliteDB
dbName = netWatch.db

[Google -- Ping]
host = google.com
alias= Google
module = ping
ctag = 
delay = 2
timeout = 1

[My Router -- Ping]
host = 192.168.1.1
alias= Router
module = ping
ctag = 
delay = 2
timeout = 1
```

Replace the host values with whatever is correct for you. Next, make your netTKAnalysis.cfg file this:

```
[SQLite Database Handler]
module = sqliteDB
dbName = netWatch.db


[lineGraph -- Latency]
sharex  = True 
sharey  = True 

alias_1  = Google
module_1 = ping
ctag_1  = 
age_1   = 30 Minutes
title_1  = Latency to Google via Ping

alias_4  = Router
module_4 = ping
ctag_4   = 
age_4    = 30 Minutes
title_4  = Latency to My Router via Ping
```

Now start it up with the following:

```shell
> sudo python ./netTK.py
```

Next, start up your analysis with the following:

```shell
> python ./netTKAnalysis.py
```

You should start seeing a line graph depicting your ping packet delay times to your router and out to google.

## Running It
NetTK is broken down into two components: monitor and analysis.

### Monitor

Monitor modules are configurable through the netTK.cfg file. Every module will record latency and dropped packets for it's particular area, but will differ by what it is checking. For instance, one module will allow you to constantly ICMP Echo Request (ping) a host, while another will allow you to contantly TCP SYN test a host.

The netTK.cfg file follows this basic format:

```
; [Title] -- This is for your readability, not used anywhere
; host -- (standard) DNS/IP of the host to test
; alias -- (standard) Alias of the host to use. This will be what the sqltable name uses
; module -- (standard) The type of test to use on this host. This is how netWatch decides what to do with the host. For example, "ping".
; ctag -- (optional) Optional tag to be used for defining save table name. Table name becomes "alias_module[_tag]". Useful when module is "tcpping" to keep track of  port/options/etc.
; attributes -- (This can vary by module)
```

For specific variables with respect to any given module, check either the Wiki or the corresponding "example.cfg" file (i.e.: monitor/ping.example.cfg).

### Analysis

The analysis modules let you look at the information you have gathered with the monitor modules in interesting ways. These are also configurable in a plain text way from netTKAnalysis.cfg. It follows the following form:

```
; [Engine] -- This defines what analysis engine you want to use (these are what is under analysis/*)
; alias_x -- (standard) the alias name to use (take this from the netWatch.cfg file)
; module_x -- (standard) The type of test that was used on this host. For example, "ping".
; ctag_x -- (optional) Optional tag to be used for defining save table name. Table name becomes "alias_module[_tag]". Useful when module is "tcpping" to keep track of  port/options/etc.
; attributes -- (This can vary by engine)
```

As with the monitor modules, the analysis module example config files can be found under analysis/module.example.cfg.

### Start it

One you have your monitor and analysis cfg files modified, all you have to do to run it is:

```shell
> sudo python ./netTK.py
```

And then to start your analysis:

```shell
> python ./netTKAnalysis.py
```
