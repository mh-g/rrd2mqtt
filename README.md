# rrd2mqtt

Small script to publish updates to an RRD database as MQTT topics. It analyses the latest entry in an RRD file, checks its age and publishes all found data sets as topics with the name "[domain]/[dataset_name]". Runs either cyclically or as one-shot.

Takes two mandatory arguments:
  - path to RRD database file
  - MQTT server
Optional arguments:
  - -c/--cycle: rate in seconds for checks and publishes if > 0, otherwise publish only once; defaults to -1
  - -d/--domain: prefix used to generate topic name, defaults to "rrd2mqtt"
  - -d/--max_age: maximum age of data to be published in seconds, defaults to 60s

This script was created to fulfill a need to feed Home Assistant with some sensor data that come in proprietary format via network but are also available in RRDs.
