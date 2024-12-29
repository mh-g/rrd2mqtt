import argparse
import rrdtool
import paho.mqtt.client as mqtt
from time import sleep
import datetime

# read and publish database info in separate topics containing only the value
def publish(client, domain, name, max_age):
    info = rrdtool.lastupdate(name)
    if datetime.datetime.now() - info['date'] < datetime.timedelta(seconds=max_age):
        for ds in info['ds']:
            client.publish(f'/{domain}/{name.split("/")[-1]}/{ds}', info['ds'][ds])


# read and publish database info in a single json topic
def publish_json(client, domain, name, max_age):
    info = rrdtool.lastupdate(name)
    if datetime.datetime.now() - info['date'] < datetime.timedelta(seconds=max_age):
        result = '{\n'
        first = True
        for ds in info['ds']:
            if first:
                first = False
            else:
                result += ',\n'
            result += f'    "{ds}": {info["ds"][ds]}'
        result += '\n}'
        client.publish(f'/{domain}/{name.split("/")[-1]}', result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rrdfile')
    parser.add_argument('mqttserver')
    parser.add_argument('-d', '--domain', help = 'prefix used to generate topic name',
                        default = 'rrd2mqtt')
    parser.add_argument('-c', '--cycle', type = float,
                        help = 'rate in seconds for checks and publishes (if not set publish only once)',
                        default = -1)
    parser.add_argument('-m', '--max_age', type = float,
                        help = 'maximum age of data to be published in seconds',
                        default = 60)
    parser.add_argument('-j', '--json', help = 'use single json-formatted topic for all data sets',
			action='store_true')
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(args.mqttserver)

    while True:
        if args.json:
            publish_json(client, args.domain, args.rrdfile, args.max_age)
        else:
            publish(client, args.domain, args.rrdfile, args.max_age)
        if args.cycle > 0.0:
            sleep(args.cycle)
        else:
            break

#     client.loop_forever()
