"""
Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Licensed under the Apache License, Version 2.0 (the "License").
  You may not use this file except in compliance with the License.
  A copy of the License is located at

      http://www.apache.org/licenses/LICENSE-2.0

  or in the "license" file accompanying this file. This file is distributed
  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
  express or implied. See the License for the specific language governing
  permissions and limitations under the License.
 """

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from collector import Collector
import logging
import argparse
from time import sleep
from socket import gethostname


class IoTClientWrapper(object):
    """ IoTClientWrapper

    Wrapper around the AWS Iot Python SDK. Sets common parameters based on the SDK's Basic PubSub sample
    https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSub.py

    """

    def __init__(self, endpoint, root_ca_path, certificate_path, private_key_path, client_id):
        self.host = endpoint
        self.root_ca_path = root_ca_path
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path

        if not args.client_id:
            self.client_id = gethostname()
        else:
            self.client_id = args.client_id

        self.iot_client = None

    def publish(self, publish_to_topic, payload):
        """Publish to MQTT"""
        self.iot_client.publish(topic=publish_to_topic, payload=payload, QoS=0)

    def subscribe(self, subscribe_to_topic, callback):
        """Subscribe to MQTT"""
        self.iot_client.subscribe(topic=subscribe_to_topic, callback=callback, QoS=1, )

    def connect(self):
        """Connect to AWS IoT"""
        if not self.certificate_path or not self.private_key_path:
            print ("Missing credentials for authentication.")
            exit(2)

        # Configure logging
        logger = logging.getLogger("AWSIoTPythonSDK.core")
        logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        self.iot_client = AWSIoTMQTTClient(self.client_id)
        self.iot_client.configureEndpoint(self.host, 8883)
        self.iot_client.configureCredentials(
            self.root_ca_path, self.private_key_path, self.certificate_path)

        # AWSIoTMQTTClient connection configuration
        self.iot_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.iot_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.iot_client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.iot_client.configureConnectDisconnectTimeout(60)
        self.iot_client.configureMQTTOperationTimeout(60)  # 5 sec

        # Connect and subscribe to AWS IoT
        self.iot_client.connect()

        sleep(2)


def parse_args():
    """Setup Commandline Argument Parsing"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store", required=True, dest="endpoint",
                        help="Your AWS IoT custom endpoint")
    parser.add_argument("-r", "--rootCA", action="store", dest="root_ca_path", default="root-CA.crt",
                        help="Root CA file path")
    parser.add_argument("-c", "--cert", action="store", dest="certificate_path", default="certificate.pem",
                        help="Certificate file path")
    parser.add_argument("-k", "--key", action="store", dest="private_key_path", default="private.key",
                        help="Private key file path")
    parser.add_argument("-id", "--client_id", action="store", dest="client_id",
                        help="MQTT Client id (Thing Name)")
    parser.add_argument("-d", "--dryrun", action="store_true", dest="dry_run", default=False,
                        help="Collect and print metrics to console, do not publish them over mqtt")
    parser.add_argument("-i", "--interval", action="store", dest="upload_interval", default=300,
                        help="Interval in seconds between metric uploads")
    parser.add_argument("-s", "--short_tags", action="store_true", dest="short_tags", default=False,
                        help="Use long-format field names in metrics report")
    parser.add_argument("-f", "--format", action="store", dest="format", choices=["cbor", "json"],
                        help="Choose serialization format for metrics report")
    return parser.parse_args()


def custom_callback(self, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


if __name__ == '__main__':
    # Read in command-line parameters
    args = parse_args()

    if not args.dry_run:
        iot_client = IoTClientWrapper(args.endpoint, args.root_ca_path,
                                      args.certificate_path, args.private_key_path, args.client_id)
        iot_client.connect()

        # client_id must match a registered thing name in your account
        topic = "$aws/things/" + args.client_id + "/defender/metrics/" + args.format
        topic_kg = "ganapatk/things/ganapatk-testIoT/defender/metrics/json"

        # Subscribe to the accepted/rejected topics to indicate status of published metrics reports
        iot_client.subscribe(topic + "/accepted", custom_callback)
        iot_client.subscribe(topic + "/rejected", custom_callback)

    sample_rate = args.upload_interval

    #  Collector samples metrics from the system, it can track the previous metric to generate deltas
    collector = Collector(args.client_id, args.short_tags)

    metric = None
    while True:
        metric = collector.collect_metrics()
        if args.dry_run:
            print (metric.to_json_string(pretty_print=True))
        else:
            print (metric.to_json_string(pretty_print=False))
            if args.format == "cbor":
                iot_client.publish(topic, bytearray(metric.to_cbor()))
            else:
                iot_client.publish(topic, metric.to_json_string())
                iot_client.publish(topic_kg, metric.to_json_string())

        sleep(float(sample_rate))
