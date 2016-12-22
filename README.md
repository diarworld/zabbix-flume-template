# zabbix-flume-template
Zabbix autodiscovery template and externalscript for monitoring Apache Flume via http.


### Installation
* Put check_flume_metrics.py to all Apache Flume hosts. By default directory is: /usr/lib/zabbix/externalscripts/. Change permissions to run this script:
```
$ chmod +x /usr/lib/zabbix/externalscripts/check_flume_metrics.py
```
* Put userparameter_flume.conf to /etc/zabbix/zabbix_agentd.d/userparameter_flume.conf (Modify this config, if you use different path for externascript)
* restart zabbix agent on Flume hosts.
* Import zabbix-flume-template to your Zabbix.


### Test insallation


```
usage: check_flume_metrics.py [-h] [--discover type] [--check flow metric]
                              [--address ADDRESS] [--port PORT]

Simple python script for checking flume metrcis via http

optional arguments:
  -h, --help            show this help message and exit
  --discover type, -d type
                        Discover all flume flows by type
  --check flow metric, -c flow metric
                        Check specified metric
  --address ADDRESS, -a ADDRESS
                        Flume address. Default is: localhost
  --port PORT, -p PORT  Flume http port. Default is: 41414
```

If you installed zabbix_get package, you may run :
```
zabbix_get -s flumehost1 -k flume.check[41414,"CHANNEL.prod-channel","ChannelFillPercentage"]

```

#### Examples

Discovery:

```
$ sudo -u zabbix /etc/zabbix/externalscripts/check_flume_metrics.py --discover SOURCE -a flumehost1
{"data": [{"{#NAME}": "SOURCE.test-source"}, {"{#NAME}": "SOURCE.prod-source"}, {"{#NAME}": "SOURCE.third-source"}]}

```

Check

```
$ sudo -u zabbix /etc/zabbix/externalscripts/check_flume_metrics.py --check SOURCE.test-source KafkaEventGetTimer -a flumehost1
28030074
```

#### Notes
* Tested with Zabbix 3.2 and Flume CDH-5.7.0-1.cdh5.7.0.p0.45 version.