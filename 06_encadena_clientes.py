from paho.mqtt.client import Client
from time import sleep

TIMER_STOP = 'clients/timerstop'
TEMP = 'temperature/t1'
HUMIDITY = 'humidity'
NUMBERS = 'numbers'

def timer(time, data):
     mqttc = Client()
     mqttc.connect(data['broker'])
     msg = f'timer working. timeout: {time}'
     print(msg)
     mqttc.publish(TIMER_STOP, msg)
     sleep(time)
     msg = f'timer working. timeout: {time}'
     mqttc.publish(TIMER_STOP, msg)
     print('timer end working')
     mqttc.disconnect()
     
def on_message(mqttc, data, msg):
     print (f'message:{msg.topic}:{msg.payload}:{data}')
     if data['status'] == 0:
         temp = int(msg.payload)
         if temp > data['temp_threshold']:
             print(f'Umbral superado {temp}, subscribimos a números')
             mqttc.unsubscribe(TEMP)
             mqttc.subscribe(NUMBERS)
             data['status'] = 2
             
     elif data['status'] == 1:
         humidity = int(msg.payload)
         if humidity > data['humidity_threshold']:
             print(f'Umbral superado {humidity}, subscribimos a números')
             mqttc.unsubscribe(HUMIDITY)
             mqttc.subscribe(NUMBERS)
             data['status'] = 2
         
     elif data['status'] == 2:
         nmbr = int(msg.payload)
         if nmbr % 7 == 0:
             if (nmbr // 7) % 2 == 0:
                 print(f'Condición superada {nmbr}, subscribimos a temperatura')
                 mqttc.unsubscribe(NUMBERS)
                 mqttc.subscribe(TEMP)
                 data['status'] = 0
             else:
                 print(f'Condición superada {nmbr}, subscribimos a humedad')
                 mqttc.unsubscribe(NUMBERS)
                 mqttc.subscribe(HUMIDITY)
                 data['status'] = 0
                 
def main(broker):
     data = {'temp_threshold':20,
     'humidity_threshold':80,
     'status': 0}
     mqttc = Client(userdata=data)
     mqttc.on_message = on_message
     mqttc.enable_logger()
     mqttc.connect(broker)
     mqttc.subscribe(TEMP)
     mqttc.loop_forever()
if __name__ == "__main__":
     import sys
     if len(sys.argv)<2:
         print(f"Usage: {sys.argv[0]} broker")
         sys.exit(1)
     broker = sys.argv[1]
     main(broker)