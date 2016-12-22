# zabbix-flume-template
Zabbix template and externalscript for monitoring Apache Flume via http.


### Installation
* Put check_flume_metrics.py to all Apache Flume hosts.
* Put userparameter_flume.conf to /etc/zabbix/zabbix_agentd.d/userparameter_flume.conf (Modify it, if you use different path for externascript)
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

#### Example

Discovery:

```
$/etc/zabbix/externalscripts/check_flume_metrics.py --discover SOURCE -a flumehost1
{"data": [{"{#NAME}": "SOURCE.test-source"}, {"{#NAME}": "SOURCE.prod-source"}, {"{#NAME}": "SOURCE.third-source"}]}

```

Check

```
$/etc/zabbix/externalscripts/check_flume_metrics.py --check SOURCE.test-source KafkaEventGetTimer -a flumehost1
28030074
```
