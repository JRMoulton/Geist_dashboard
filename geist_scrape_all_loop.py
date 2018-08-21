import csv
import time
import datetime
import requests
import smtplib
import json
import ast

def looptest():
    dashboard_data = []
    geist_list = []
    geist_list_count = 0


    ###############################
    # Assign each analog sensor values to the right variables. ie: door, door_state
    def assignSensor(sensor_mode, sensor_value, sensor_label):
        global smoke
        global smoke_state
        global smoke_label
        global smoke_sensor

        global door
        global door_state
        global door_label
        global door_sensor

        global power_failure
        global power_failure_state
        global power_failure_label
        global power_failure_sensor

        global flood
        global flood_state
        global flood_label
        global flood_sensor

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
                if float(generator) >= 5:
                    generator_state = "Alarm"
                else:
                    generator_state = "Normal"
            else:
                door_sensor = True
                door_label = sensor_label
                door = sensor_value
                if door == "0.00":
                    door_state = "Normal"
                elif door == "1.00":
                    door_state = "Alarm"
        elif "smoke" in sensor_mode:
            
            smoke_sensor = True
            smoke_label = sensor_label
            smoke = sensor_value
            if smoke == "0.00":
                smoke_state = "Alarm"
            elif smoke == "1.00":
                smoke_state = "Normal"
        elif "powerFailure" in sensor_mode:
            power_failure_sensor = True
            power_failure_label = sensor_label
            power_failure = sensor_value
            if power_failure == "0.00":
                power_failure_state = "Alarm"
            elif power_failure == "1.00":
                power_failure_state = "Normal"
        elif "flood" in sensor_mode:
            flood_sensor = True
            flood_label = sensor_label
            flood = sensor_value
            if flood == "0.00":
                flood_state = "Alarm"
            elif flood == "1.00":
                flood_state = "Normal"
        elif "ivsPosGnd" in sensor_mode:
            plant_voltage_sensor = True
            plant_voltage_label = sensor_label
            plant_voltage = str(round(float(sensor_value),1))
    
            ########################
            # Determine alarm status
            plant_voltage_float = (float(plant_voltage))
            if -51 <= plant_voltage_float < -53:
                plant_voltage_state = "Warning"
            elif plant_voltage_float > -51:
                plant_voltage_state = "Alarm"
            else:
                plant_voltage_state = "Normal"
        elif "customVoltage" in sensor_mode:
            if "Hydrogen" in sensor_label:
                hydrogen_sensor = True
                hydrogen_label = sensor_label
                hydrogen = sensor_value
        
                ########################
                # Determine alarm status
                hydrogen_float = (float(hydrogen))
                if 50 <= hydrogen_float < 80:
                    hydrogen_state = "Warning"
                elif hydrogen_float >= 80:
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
        sub_list = {'hostname': device_hostname, 'ip_address': device_ip_address}
        if "-ev-" in device_hostname:
            geist_list.append(sub_list)
            geist_list_count += 1    

    print(geist_list)
    print(geist_list_count)

    for device in geist_list:
        hostname = device['hostname']
        ip_address = device['ip_address']
        device_link = "http://" + ip_address + "/#overview"


        ###############################
        r = requests.get('http://{}/api/dev'.format(ip_address))
        output = (r.text)
        output_dict = json.loads(output)

        #print(output_dict)

        for key, value in output_dict.items():
            temp_internal_sensor = False
            temp_internal_label = ""
            temp_internal = ""
            temp_internal_state = ""

            remote_temp_sensor = False
            remote_temp_label = ""
            remote_temp = ""
            remote_temp_state = ""

            door_sensor = False
            door_label = ""
            door = ""
            door_state = ""

            smoke_sensor = False
            smoke_label = ""
            smoke = ""
            smoke_state = ""

            power_failure_sensor = False
            power_failure_label = ""
            power_failure = ""
            power_failure_state = ""

            flood_sensor = False
            flood_label = ""
            flood = ""
            flood_state = ""

            plant_voltage_sensor = False
            plant_voltage_label = ""
            plant_voltage = ""
            plant_voltage_state = ""

            generator_sensor = False
            generator_label = ""
            generator = ""
            generator_state = ""

            hydrogen_sensor = False
            hydrogen_label = ""
            hydrogen = ""
            hydrogen_state = ""
            
            
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

                        temp_internal_state = "testing"
                        temp_internal = temp_internal_value + " °" + temp_internal_unit
                        temp_internal_float = (float(temp_internal_value))
                        if 75 <= temp_internal_float < 80:
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
                        

                    elif "remotetemp" in inner_dict2.values():
                        if "unavailable" in inner_dict2.values():
                            print("Unavailable Remote Temp!!!")
                        else:
                            print("Remote Temperature!")
                            remote_temp_sensor = True

                            remote_temp_value = str(round(float(inner_dict2["entity"]["0"]["measurement"]["0"]["value"])))
                            remote_temp_label = inner_dict2["entity"]["0"]["measurement"]["0"]["type"]
                            remote_temp_unit = inner_dict2["entity"]["0"]["measurement"]["0"]["units"]

                            remote_temp = remote_temp_value + "°"
                            remote_temp_float = float(remote_temp_value)

                            if 73 <= remote_temp_float < 80:
                                    remote_temp_state = "Warning"
                            elif remote_temp_float >= 80:
                                remote_temp_state = "Alarm"
                            elif remote_temp_float < 50:
                                remote_temp_state = "Low"
                            else:
                                remote_temp_state = "Normal"  

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
                                            "state": temp_internal_state
                                            },
                                    "door": {
                                            "sensor": door_sensor,
                                            "label": door_label,
                                            "value": door,
                                            "state": door_state
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

    ##############################
    # To test for naming in Geist of individual sensors 
    #for device in dashboard_data:
    #    print("\n")
    #    print(device["device"]["name"])
    #    print(device["device"]["ip_address"] + "/#overview")

variable = 1

while variable == 1:
    looptest()