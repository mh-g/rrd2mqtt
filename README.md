# rrd2mqtt

Small script to publish updates to an RRD database (https://oss.oetiker.ch/rrdtool/) as MQTT topics (https://mqtt.org/).

It analyses the latest entry in an RRD file, checks its age and publishes all found data sets as topics with the name "/[domain]/[rrd_filename]/[dataset_name]". rrd_filename is without any path information. In json mode, all data sets are published within one topic with the name "/[domain]/[rrd_filename]" as a dictionary with dataset_name as the keys.

Runs either cyclically or as one-shot.

Takes two mandatory arguments:
  - path to RRD database file
  - MQTT server

Optional arguments:
  - -c/--cycle: rate in seconds for checks and publishes if > 0, otherwise publish only once; defaults to -1
  - -d/--domain: prefix used to generate topic name, defaults to "rrd2mqtt"
  - -m/--max_age: maximum age of data to be published in seconds, defaults to 60s
  - -j/--json: publish a single topic with all data sets in json format instead of one topic per data set

This script was created to fulfill a need to feed Home Assistant with some sensor data that come in proprietary format via network but are also available in RRDs.
