from operator import itemgetter
from datetime import datetime
import csv
import time
import requests
import smtplib
import json
import ast
import os

dashboard_data = []
geist_list = []
geist_list_count = 0

#########################################################
# Datetime variables to determine business hours
weekday = datetime.today().weekday()
current_hour = int((datetime.now().strftime('%H')))
business_hours = False
holidays = ["09-03-18", "11-22-18", "12-25-18"]
today = (datetime.now().strftime('%m-%d-%y'))

#########################################################
# Returns true if current day/time is during business hours.
if weekday < 5:
    if 6 < current_hour < 18:
        if not today in holidays:
            business_hours = True


###############################
# Assign each analog sensor values to the right variables. ie: door, door_state
def assignSensor(sensor_mode, sensor_value, sensor_label):
    global business_hours

    global smoke
    global smoke_state
    global smoke_label
    global smoke_sensor

    global door
    global door_state
    global door_label
    global door_sensor

    global door2
    global door_state2
    global door_label2
    global door_sensor2

    global door3
    global door_state3
    global door_label3
    global door_sensor3

    global power_failure
    global power_failure_state
    global power_failure_label
    global power_failure_sensor

    global flood
    global flood_state
    global flood_label
    global flood_sensor

    global flood2
    global flood2_state
    global flood2_label
    global flood2_sensor

    global plant_voltage
    global plant_voltage_state
    global plant_voltage_label
    global plant_voltage_sensor

    global generator
    global generator_state
    global generator_label
    global generator_sensor

    global hydrogen
    global hydrogen_state
    global hydrogen_label
    global hydrogen_sensor


    if "Spare" in sensor_label:
        print("Spare - not in use")

    elif "door" in sensor_mode:
        if "Generator" in sensor_label:
            generator_sensor = True
            generator_label = sensor_label
            generator = sensor_value
    
            ########################
            # Determine alarm status
            int(float(generator))
            if int(float(generator)) == 0:
                generator_state = "Alarm"
            else:
                generator_state = "Normal"
        else:
            if door_sensor == True:
                if door_sensor2 == True:
                    if door_sensor3 == True:
                        print("Dang there are four doors!")
                    else:
                        door_sensor3 = True
                        door_label3 = sensor_label
                        door3 = sensor_value
                        print(door3)
                        if int(float(door3)) == 0:
                            door_state3 = "Normal"
                        elif int(float(door3)) == 1:
                            if business_hours == True:
                                door_state3 = "Warning"
                            else: 
                                door_state3 = "Alarm"
                else:
                    door_sensor2 = True
                    door_label2 = sensor_label
                    door2 = sensor_value
                    if int(float(door2)) == 0:
                        door_state2 = "Normal"
                    elif int(float(door2)) == 1:
                        if business_hours == True:
                            door_state2 = "Warning"
                        else: 
                            door_state2 = "Alarm"
            else:    
                door_sensor = True
                door_label = sensor_label
                door = sensor_value
                if int(float(door)) == 0:
                    door_state = "Normal"
                elif int(float(door)) == 1:
                    if business_hours == True:
                        door_state = "Warning"
                    else: 
                        door_state = "Alarm"
    elif "smoke" in sensor_mode:
        smoke_sensor = True
        smoke_label = sensor_label
        smoke = sensor_value
        if int(float(smoke)) == 0:
            smoke_state = "Alarm"
        elif int(float(smoke)) == 1:
            smoke_state = "Normal"
    elif "powerFailure" in sensor_mode:
        power_failure_sensor = True
        power_failure_label = sensor_label
        power_failure = sensor_value
        if int(float(power_failure)) == 0:
            power_failure_state = "Alarm"
        elif int(float(power_failure)) == 1:
            power_failure_state = "Normal"
    elif "flood" in sensor_mode:
        if flood_sensor == True:
            flood2_sensor = True
            flood2_label = sensor_label
            flood2 = sensor_value
            if int(float(flood2)) == 0:
                flood_state = "Alarm"
            elif int(float(flood2)) == 1:
                flood2_state = "Normal"
        else:
            flood_sensor = True
            flood_label = sensor_label
            flood = sensor_value
            if int(float(flood)) == 0:
                flood_state = "Alarm"
            elif int(float(flood)) == 1:
                flood_state = "Normal"
    elif "ivsPosGnd" in sensor_mode:
        plant_voltage_sensor = True
        plant_voltage_label = sensor_label
        plant_voltage = str(round(float(sensor_value),1))
  
        ########################
        # Determine alarm status
        plant_voltage_float = (float(plant_voltage))
        if -48 <= plant_voltage_float < -51:
            plant_voltage_state = "Warning"
        elif plant_voltage_float > -48:
            plant_voltage_state = "Alarm"
        else:
            plant_voltage_state = "Normal"
    elif "customVoltage" in sensor_mode: 
        if "Hydrogen" in sensor_label:
            old_max = 100.0
            old_min = 0.0
            new_max = 4.0
            new_min = 0.25
            old_value = float(sensor_value)
            old_range = (old_max - old_min)  
            new_range = (new_max - new_min)  
            new_value = (((old_value - old_min) * new_range) / old_range) + new_min
            hydrogen_sensor = True
            hydrogen_label = sensor_label
            hydrogen = round(new_value,1)
    
            ########################
            # Determine alarm status
            if 5 <= hydrogen < 6:
                hydrogen_state = "Warning"
            elif hydrogen >= 6:
                hydrogen_state = "Alarm"
            else:
                hydrogen_state = "Normal"
        else:
            generator_sensor = True
            generator_label = sensor_label
            generator = sensor_value
    
            ########################
            # Determine alarm status
            generator_float = (float(generator))
            if generator_float > 5:
                generator_state = "Alarm"
            else:
                generator_state = "Normal"


###############################

###############################
# Curl request to SevOne to get device list
url = "http://10.225.254.110/api/v2/devices?size=10000"
headers = {"Accept": "application/json", "X-AUTH-TOKEN": "eyJhbGciOiJIUzUxMiJ9eyJpc3MiOiJzY2FsZHdlbGwifQlXLQ1GDr18jn2KQ__-hVHMbc2eDPLV7MTbjhTxiiAkt1VDPdZbLqluESHuRnax5vnfXWyE7xS3jRS37iwCoItA"}
r = requests.get(url, headers=headers)
all_devices = str(json.loads(r.text))
device_dict = all_devices[all_devices.find("[")+1:all_devices.find("]")]
devices_dict_str = "[" + device_dict + "]"
device_list = ast.literal_eval(devices_dict_str)


for list in device_list:
    device_hostname = list['name']
    device_ip_address = str(list['ipAddress'])
    device_alt_name = list['alternateName']
    sub_list = {'hostname': device_hostname, 'ip_address': device_ip_address, 'alt_name': device_alt_name}
    if "-ev-" in device_hostname:
        geist_list.append(sub_list)
        geist_list_count += 1    


geist_list_ordered = sorted(geist_list, key=itemgetter('alt_name'))
print(geist_list_ordered)
print(geist_list_count)

for device in geist_list_ordered:
    hostname = device['hostname']
    ip_address = device['ip_address']
    alt_name = device ['alt_name']
    device_link = "http://" + ip_address + "/#overview"


    ###############################
    r = requests.get('http://{}/api/dev'.format(ip_address))
    output = (r.text)
    output_dict = json.loads(output)

    #print(output_dict)

    for key, value in output_dict.items():
        temp_internal_sensor = False
        temp_internal_label = None
        temp_internal = None
        temp_internal_state = None
        temp_internal_number = None


        remote_temp_sensor = False
        remote_temp_label = None
        remote_temp = None
        remote_temp_state = None

        door_sensor = False
        door_label = None
        door = None
        door_state = None

        door_sensor2 = False
        door_label2 = None
        door2 = None
        door_state2 = None

        door_sensor3 = False
        door_label3 = None
        door3 = None
        door_state3 = None

        smoke_sensor = False
        smoke_label = None
        smoke = None
        smoke_state = None

        power_failure_sensor = False
        power_failure_label = None
        power_failure = None
        power_failure_state = None

        flood_sensor = False
        flood_label = None
        flood = None
        flood_state = None
        
        flood2_sensor = False
        flood2_label = None
        flood2 = None
        flood2_state = None

        plant_voltage_sensor = False
        plant_voltage_label = None
        plant_voltage = None
        plant_voltage_state = None

        generator_sensor = False
        generator_label = None
        generator = None
        generator_state = None

        hydrogen_sensor = False
        hydrogen_label = None
        hydrogen = None
        hydrogen_state = None
        
        
        if "data" in key:
            inner_dict = value
            for key, value in inner_dict.items():
                inner_dict2 = value

                print("*****************************************")
                print("\n")

                if "BB-REL-THA4" in inner_dict2.values():
                    temp_internal_sensor = True
                    print("\n")
                    geist_name = inner_dict2["label"]
                    geist_state = inner_dict2["state"]
                    temp_internal_value = str(round(float(inner_dict2["entity"]["0"]["measurement"]["0"]["value"]),1))
                    temp_internal_label = inner_dict2["entity"]["0"]["measurement"]["0"]["type"]
                    temp_internal_unit = inner_dict2["entity"]["0"]["measurement"]["0"]["units"]
                    temp_internal_number = round(float(inner_dict2["entity"]["0"]["measurement"]["0"]["value"]),1)
                    print(temp_internal_number)

                    temp_internal_state = "testing"
                    temp_internal = temp_internal_value + " °" + temp_internal_unit
                    temp_internal_float = (float(temp_internal_value))
                    if 77 <= temp_internal_float < 80:
                        temp_internal_state = "Warning"
                    elif temp_internal_float >= 80:
                        temp_internal_state = "Alarm"
                    elif temp_internal_float < 50:
                        temp_internal_state = "Low"
                    else:
                        temp_internal_state = "Normal"

                    humidity = inner_dict2["entity"]["0"]["measurement"]["1"]["value"]
                    dew_point = inner_dict2["entity"]["0"]["measurement"]["2"]["value"]
                    analog_0 = inner_dict2["analog"]["0"]["mode"]
                    analog_0_value = inner_dict2["analog"]["0"]["value"]
                    analog_0_label = inner_dict2["analog"]["0"]["label"]
                    analog_1 = inner_dict2["analog"]["1"]["mode"]
                    analog_1_value = inner_dict2["analog"]["1"]["value"]
                    analog_1_label = inner_dict2["analog"]["1"]["label"]
                    analog_2 = inner_dict2["analog"]["2"]["mode"]
                    analog_2_value = inner_dict2["analog"]["2"]["value"]
                    analog_2_label = inner_dict2["analog"]["2"]["label"]
                    analog_3 = inner_dict2["analog"]["3"]["mode"]
                    analog_3_value = inner_dict2["analog"]["3"]["value"]
                    analog_3_label = inner_dict2["analog"]["3"]["label"]

                    ##########################################################
                    # Run function to Assign each value to correct sensor type
                    assignSensor(analog_0, analog_0_value, analog_0_label)
                    assignSensor(analog_1, analog_1_value, analog_1_label)
                    assignSensor(analog_2, analog_2_value, analog_2_label)
                    assignSensor(analog_3, analog_3_value, analog_3_label)
                    

                elif "A2D Sensor" in inner_dict2.values():
                    print("Extra A2D Sensor!")
                    analog_0_a2d = inner_dict2["analog"]["0"]["mode"]
                    analog_0_a2d_value = inner_dict2["analog"]["0"]["value"]
                    analog_0_a2d_label = inner_dict2["analog"]["0"]["label"]
                    print(analog_0_a2d)
                    print(analog_0_a2d_label)
                    print(analog_0_a2d_value)

                    assignSensor(analog_0_a2d, analog_0_a2d_value, analog_0_a2d_label)


                elif "remotetemp" in inner_dict2.values():
                    if "unavailable" in inner_dict2.values():
                        print("Unavailable Remote Temp!!!")
                    else:
                        print("Remote Temperature!")
                        remote_temp_sensor = True

                        remote_temp_value = str(round(float(inner_dict2["entity"]["0"]["measurement"]["0"]["value"])))
                        remote_temp_label = inner_dict2["label"]
                        remote_temp_unit = inner_dict2["entity"]["0"]["measurement"]["0"]["units"]

                        remote_temp = remote_temp_value + "°"
                        remote_temp_float = float(remote_temp_value)

                        if 77 <= remote_temp_float < 80:
                                remote_temp_state = "Warning"
                        elif remote_temp_float >= 80:
                            remote_temp_state = "Alarm"
                        elif remote_temp_float < 40:
                            remote_temp_state = "Low"
                        else:
                            remote_temp_state = "Normal" 
                #########################################################
                # Checks for overall criticality based on highest criticality of any one sensor.
                sensor_states = [temp_internal_state, temp_internal_state, door_state, smoke_state, power_failure_state, flood_state, remote_temp_state, plant_voltage_state, generator_state, hydrogen_state]    
                geist_criticality = "Normal"
                if "Warning" in sensor_states:
                    geist_criticality = "Warning"
                if "Low" in sensor_states:
                    geist_criticality = "Low"
                if "Critical" in sensor_states:
                    geist_criticality = "Critical"
                if "Alarm" in sensor_states:
                    geist_criticality = "Critical"
                #########################################################
                # Create dictionary with fields from all possible sensors
                geist_data = {"device": {
                                        "name": geist_name,
                                        "alt_name": alt_name,
                                        "ip_address": ip_address,
                                        "state": geist_state,
                                        "humidity": humidity,
                                        "dew_point": dew_point,
                                        "device_link": device_link,
                                        "geist_criticality": geist_criticality 
                                        },
                        "temp_internal": {
                                        "sensor": temp_internal_sensor,
                                        "label": temp_internal_label,
                                        "value": temp_internal,
                                        "state": temp_internal_state,
                                        "number": temp_internal_number
                                        },
                                "door": {
                                        "sensor": door_sensor,
                                        "label": door_label,
                                        "value": door,
                                        "state": door_state
                                        },
                               "door2": {
                                        "sensor": door_sensor2,
                                        "label": door_label2,
                                        "value": door2,
                                        "state": door_state2
                                        },
                               "door3": {
                                        "sensor": door_sensor3,
                                        "label": door_label3,
                                        "value": door3,
                                        "state": door_state3
                                        },
                                "smoke": {
                                        "sensor": smoke_sensor,
                                        "label": smoke_label,
                                        "value": smoke,
                                        "state": smoke_state
                                        },
                        "power_failure": {
                                        "sensor": power_failure_sensor,
                                        "label": power_failure_label,
                                        "value": power_failure,
                                        "state": power_failure_state
                                        },
                                "flood": {
                                        "sensor": flood_sensor,
                                        "label": flood_label,
                                        "value": flood,
                                        "state": flood_state
                                        },
                               "flood2": {
                                        "sensor": flood2_sensor,
                                        "label": flood2_label,
                                        "value": flood2,
                                        "state": flood2_state
                                        },
                        "remote_temp": {
                                        "sensor": remote_temp_sensor,
                                        "label": remote_temp_label,
                                        "value": remote_temp,
                                        "state": remote_temp_state
                                        },
                        "plant_voltage": {
                                        "sensor": plant_voltage_sensor,
                                        "label": plant_voltage_label,
                                        "value": plant_voltage,
                                        "state": plant_voltage_state
                                        },
                            "generator": {
                                        "sensor": generator_sensor,
                                        "label": generator_label,
                                        "value": generator,
                                        "state": generator_state
                                        },
                            "hydrogen": {
                                        "sensor": hydrogen_sensor,
                                        "label": hydrogen_label,
                                        "value": hydrogen,
                                        "state": hydrogen_state
                                        }
                            }
            print("\n")
            print(geist_name)
            print(ip_address)
            print(geist_data)
            dashboard_data.append(geist_data)
            print(geist_state)
            print("\n")

print("\n")
print("\n")
print("\n")
print(dashboard_data)

with open('static/data.json', 'w') as fp:
    json.dump(dashboard_data, fp)

print("\n")
print("Complete!!!")


###########################################
# Append sensor values to device .csv files
csvtimestamp = (datetime.now().strftime('%m-%d-%y %H:%M'))

for sensors in dashboard_data:
    hostname = sensors['device']['name']
    filename = hostname + ".csv"

    #################################
    # Assign Variable values for .csv
    temp_internal_number = float(sensors['temp_internal']['number'])
    door = None
    if sensors['door']['sensor'] == True:
        door = int(float(sensors['door']['value']))
    door2 = None
    if sensors['door2']['sensor'] == True:
        door2 = int(float(sensors['door2']['value']))
    door3 = None
    if sensors['door3']['sensor'] == True:
        door3 = int(float(sensors['door3']['value']))
    smoke = None
    if sensors['smoke']['sensor'] == True:
        smoke = int(float(sensors['smoke']['value']))
    power_failure = None
    if sensors['power_failure']['sensor'] == True:
        power_failure = int(float(sensors['power_failure']['value']))
    flood = None
    if sensors['flood']['sensor'] == True:
        flood = int(float(sensors['flood']['value']))
    flood2 = None
    if sensors['flood2']['sensor'] == True:
        flood2 = int(float(sensors['flood2']['value']))
    remote_temp = None
    if sensors['remote_temp']['sensor'] == True:
        remote_temp = temp_internal = float(sensors['remote_temp']['value'].split('°')[0])
    remote_temp = None
    if sensors['plant_voltage']['sensor'] == True:
        plant_voltage = temp_internal = float(sensors['plant_voltage']['value'])
    generator = None
    if sensors['generator']['sensor'] == True:
        generator = temp_internal = float(sensors['generator']['value'])
    hydrogen = None
    if sensors['hydrogen']['sensor'] == True:
        hydrogen = temp_internal = float(sensors['hydrogen']['value'])
    
    csvfields = [["timestamp", "temp_internal_number", "door", "door2", "door3", "smoke", "power_failure", "flood", "flood2", "remote_temp", "plant_voltage", "generator", "hydrogen"]]
    csvdata = [[csvtimestamp, temp_internal_number, door, door2, door3, smoke, power_failure, flood, flood2, remote_temp, plant_voltage, generator, hydrogen]]
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    if not os.path.exists("csv"):
        os.makedirs("csv")

    if not os.path.exists("csv/{}".format(hostname)):
        os.makedirs("csv/{}".format(hostname))

    if not os.path.isfile('csv/{}/minute.csv'.format(hostname)):
        writeHeaders = open('csv/{}/minute.csv'.format(hostname), 'a')
        with writeHeaders:
            writer = csv.writer(writeHeaders)
            writer.writerows(csvfields)

    writeData = open('csv/{}/minute.csv'.format(hostname), 'a')
    with writeData:
        writer = csv.writer(writeData)
        writer.writerows(csvdata)


    print("Writing complete")
    print()
    print(csvdata)

##############################
# To test for naming in Geist of individual sensors 
#for device in dashboard_data:
#    print("\n")
#    print(device["device"]["name"])
#    print(device["device"]["ip_address"] + "/#overview")
