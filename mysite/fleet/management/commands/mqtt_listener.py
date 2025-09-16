import os
import json
import time
from django.core.management.base import BaseCommand
from fleet.models import Scooter
import paho.mqtt.client as mqtt

class Command(BaseCommand):
    help = 'Starts a client to listen for MQTT messages from scooters'

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            self.stdout.write(self.style.SUCCESS('Connected to MQTT broker'))
            client.subscribe("scooters/+/location")
            client.subscribe("scooters/+/status")
        else:
            self.stdout.write(self.style.ERROR(f'Failed to connect to MQTT broker, return code {rc}'))

    def on_message(self, client, userdata, msg):
        """Callback for when a message is received from a subscribed topic."""
        try:
            topic_parts = msg.topic.split('/')
            scooter_id = topic_parts[1]
            data_type = topic_parts[2]

            payload = json.loads(msg.payload.decode('utf-8'))

            try:
                # Corrected to use 'id' which is the actual primary key for the Scooter model
                scooter = Scooter.objects.get(id=scooter_id)
            except Scooter.DoesNotExist:
                # Corrected the warning message to reflect the change
                self.stdout.write(self.style.WARNING(f"Scooter with id '{scooter_id}' not found."))
                return

            if data_type == 'location':
                scooter.latitude = payload.get('latitude')
                scooter.longitude = payload.get('longitude')
                scooter.save()
                self.stdout.write(self.style.SUCCESS(f"Updated location for scooter '{scooter_id}'"))

            elif data_type == 'status':
                scooter.status = payload.get('status', scooter.status)
                scooter.battery_level = payload.get('battery_level', scooter.battery_level)
                scooter.save()
                self.stdout.write(self.style.SUCCESS(f"Updated status for scooter '{scooter_id}'"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing MQTT message: {e}"))

    def handle(self, *args, **options):
        """Main entry point for the management command."""
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        broker_host = os.environ.get('MQTT_BROKER_HOST', 'mqtt-broker')
        broker_port = 1883

        connected = False
        while not connected:
            try:
                client.connect(broker_host, broker_port, 60)
                connected = True
                self.stdout.write(self.style.SUCCESS(f"Connecting to MQTT broker at {broker_host}:{broker_port}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Could not connect to MQTT broker: {e}. Retrying in 5 seconds..."))
                time.sleep(5)
        
        client.loop_forever()
