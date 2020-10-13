def task1_delet_old_content():
     #x = mycol.delete_many({})
     #print(x.deleted_count, " documents deleted.")
     import pymongo
     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
     mydb = myclient["mydatabase"]
     mycol = mydb["customers"]
     mycol.drop()
     #mycol.delete_many({})

def task2_sub_data():

  #!/usr/bin/env python3
  import paho.mqtt.client as mqtt
  import datetime
  from pymongo import MongoClient
  import pymongo

  def on_connect(client, userdata, flags, rc):
    client.subscribe("test")

  def on_message(client, userdata, msg):
    receiveTime=datetime.datetime.now()
    message=msg.payload.decode("utf-8")
    isfloatValue=False
    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue=True
    except:
        isfloatValue=False

    if isfloatValue:
        print(str(receiveTime) + ": " + msg.topic + " " + str(val))
        #post={"topic":msg.topic,"value":val}
        post={"value":val}
    else:
        print(str(receiveTime) + ": " + msg.topic + " " + message)
        #post={"topic":msg.topic,"value":message}
        post={"value":message}
    mycol.insert_one(post)
    client2.publish(topic="TestingTopic", payload=str(message), qos=0, retain=False)
    #client2.publish(topic="TestingTopic", payload=str(message))
    #client2.publish("TestingTopic",str(message))
  # Set up client for MongoDB
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["mydatabase"]
  mycol = mydb["customers"]
  #delet_old_content()
  # Initialize the client that should connect to the Mosquitto broker
  client = mqtt.Client()
  client.connect("192.168.1.108", 1883, 60)
  client.on_connect = on_connect
  client.on_message = on_message

  # connect(host, port=1883, keepalive=60, bind_address="")
  MQTT_BROKER_HOST = "35.177.249.172"
  MQTT_BROKER_PORT = 8080
  MQTT_KEEP_ALIVE_INTERVAL = 60
  client2 = mqtt.Client()
  client2.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_KEEP_ALIVE_INTERVAL)

  # Blocking loop to the Mosquitto broker
  client.loop_forever()
  client2.loop_forever()
  #client.loop()
  #client2.loop()
  client.disconnect()
  client2.disconnect()

if __name__ == "__main__":  

    task1_delet_old_content()
    task2_sub_data()
