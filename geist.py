from operator import itemgetter
from datetime import datetime
from collections import deque
import csv
import time
import smtplib
import requests
import json
import ast
import os
starttime=time.time()

os.chdir(os.path.dirname(os.path.realpath(__file__)))

while True:
    print("tick")
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))


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
        global door2_state
        global door2_label
        global door2_sensor

        global door3
        global door3_state
        global door3_label
        global door3_sensor

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
                    if door2_sensor == True:
                        if door3_sensor == True:
                            print("Dang there are four doors!")
                        else:
                            door3_sensor = True
                            door3_label = sensor_label
                            door3 = sensor_value
                            print(door3)
                            if int(float(door3)) == 0:
                                door3_state = "Normal"
                            elif int(float(door3)) == 1:
                                if business_hours == True:
                                    door3_state = "Warning"
                                else: 
                                    door3_state = "Alarm"
                    else:
                        door2_sensor = True
                        door2_label = sensor_label
                        door2 = sensor_value
                        if int(float(door2)) == 0:
                            door2_state = "Normal"
                        elif int(float(door2)) == 1:
                            if business_hours == True:
                                door2_state = "Warning"
                            else: 
                                door2_state = "Alarm"
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

            door2_sensor = False
            door2_label = None
            door2 = None
            door2_state = None

            door3_sensor = False
            door3_label = None
            door3 = None
            door3_state = None

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
                    # Checks for overall criticality per geist based on highest criticality of any one sensor.
                    sensor_states = [temp_internal_state, temp_internal_state, door_state, door2_state, door3_state, smoke_state, power_failure_state, flood_state, remote_temp_state, plant_voltage_state, generator_state, hydrogen_state]    
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
                                            "sensor": door2_sensor,
                                            "label": door2_label,
                                            "value": door2,
                                            "state": door2_state
                                            },
                                "door3": {
                                            "sensor": door3_sensor,
                                            "label": door3_label,
                                            "value": door3,
                                            "state": door3_state
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
    csvtimestamp = (datetime.now().strftime('%Y-%m-%d %H:%M'))

    for sensors in dashboard_data:
        hostname = sensors['device']['name']
        filename = hostname + ".csv"
        print('\n')


        ###########################################################################
        # Check/update current hourly high/low values to .json file

        temp_internal_high = None
        temp_internal_low = None

        door_high = None
        door_low = None

        door2_high = None
        door2_low = None

        door3_high = None
        door3_low = None

        smoke_high = None
        smoke_low = None

        power_failure_high = None
        power_failure_low = None

        flood_high = None
        flood_low = None

        flood2_high = None
        flood2_low = None

        remote_temp_high = None
        remote_temp_low = None

        plant_voltage_high = None
        plant_voltage_low = None

        generator_high = None
        generator_low = None

        hydrogen_high = None
        hydrogen_low = None


        # Check to see if .json file exists
        if os.path.isfile('csv/{}/hourly_extremes.json'.format(hostname)):
            ###########################################################################
            # Reads in all current high/low variables and sets them in order to compare
            with open('csv/{}/hourly_extremes.json'.format(hostname)) as json_extremes:
                json_data = json.load(json_extremes)
                temp_internal_high = json_data["temp_internal"]["high"]
                temp_internal_low = json_data["temp_internal"]["low"]
                door_high = json_data["door"]["high"]
                door_low = json_data["door"]["low"]
                door2_high = json_data["door2"]["high"]
                door2_low = json_data["door2"]["low"]
                door3_high = json_data["door3"]["high"]
                door3_low = json_data["door3"]["low"]
                smoke_high = json_data["smoke"]["high"]
                smoke_low = json_data["smoke"]["low"]
                power_failure_high = json_data["power_failure"]["high"]
                power_failure_low = json_data["power_failure"]["low"]
                flood_high = json_data["flood"]["high"]
                flood_low = json_data["flood"]["low"]
                flood2_high = json_data["flood2"]["high"]
                flood2_low = json_data["flood2"]["low"]
                remote_temp_high = json_data["remote_temp"]["high"]
                remote_temp_low = json_data["remote_temp"]["low"]
                plant_voltage_high = json_data["plant_voltage"]["high"]
                plant_voltage_low = json_data["plant_voltage"]["low"]
                generator_high = json_data["generator"]["high"]
                generator_low = json_data["generator"]["low"]
                hydrogen_high = json_data["hydrogen"]["high"]
                hydrogen_low = json_data["hydrogen"]["low"]


            # check current values against highs and lows in .json

        # update any values as needed

        # rewrite dictionary out as updated .json file

        # at the begining of each our write highs/lows to hourly .csv file

        # reset .json file to defaults (or delete file?) for next hour



        #######################################
        # Assign Variable values for minute.csv
        temp_internal_number = float(sensors['temp_internal']['number'])
        if temp_internal_low == None:
                temp_internal_low = 200
        if temp_internal_high == None:
                temp_internal_high = 0
        if temp_internal_number > temp_internal_high:
            temp_internal_high = temp_internal_number
        if temp_internal_number < temp_internal_low:
            temp_internal_low = temp_internal_number
        door = None
        if sensors['door']['sensor'] == True:
            door = int(float(sensors['door']['value']))
            if door_low == None:
                door_low = 2
            if door_high == None:
                door_high = 0
            if door > door_high:
                door_high = door
            if door < door_low:
                door_low = door
        door2 = None
        if sensors['door2']['sensor'] == True:
            door2 = int(float(sensors['door2']['value']))
            if door2_low == None:
                door2_low = 2
            if door2_high == None:
                door2_high = 0
            if door2 > door2_high:
                door2_high = door2
            if door2 < door2_low:
                door2_low = door2
        door3 = None
        if sensors['door3']['sensor'] == True:
            door3 = int(float(sensors['door3']['value']))
            if door3_low == None:
                door3_low = 2
            if door3_high == None:
                door3_high = 0
            if door3 > door3_high:
                door3_high = door3
            if door3 < door3_low:
                door3_low = door3
        smoke = None
        if sensors['smoke']['sensor'] == True:
            smoke = int(float(sensors['smoke']['value']))
            if smoke_low == None:
                smoke_low = 2
            if smoke_high == None:
                smoke_high = 0
            if smoke > smoke_high:
                smoke_high = smoke
            if smoke < smoke_low:
                smoke_low = smoke
        power_failure = None
        if sensors['power_failure']['sensor'] == True:
            power_failure = int(float(sensors['power_failure']['value']))
            if power_failure_low == None:
                power_failure_low = 2
            if power_failure_high == None:
                power_failure_high = 0
            if power_failure > power_failure_high:
                power_failure_high = power_failure
            if power_failure < power_failure_low:
                power_failure_low = power_failure
        flood = None
        if sensors['flood']['sensor'] == True:
            flood = int(float(sensors['flood']['value']))
            if flood_low == None:
                flood_low = 2
            if flood_high == None:
                flood_high = 0
            if flood > flood_high:
                flood_high = flood
            if flood < flood_low:
                flood_low = flood
        flood2 = None
        if sensors['flood2']['sensor'] == True:
            flood2 = int(float(sensors['flood2']['value']))
            if flood2_low == None:
                flood2_low = 2
            if flood2_high == None:
                flood2_high = 0
            if flood2 > flood2_high:
                flood2_high = flood2
            if flood2 < flood2_low:
                flood2_low = flood2
        remote_temp = None
        if sensors['remote_temp']['sensor'] == True:
            remote_temp = float(sensors['remote_temp']['value'].split('°')[0])
            if remote_temp_low == None:
                remote_temp_low = 200.0
            if remote_temp_high == None:
                remote_temp_high = 0.0
            if remote_temp > remote_temp_high:
                remote_temp_high = remote_temp
            if remote_temp < remote_temp_low:
                remote_temp_low = remote_temp
        plant_voltage = None
        if sensors['plant_voltage']['sensor'] == True:
            plant_voltage = float(sensors['plant_voltage']['value'])
            if plant_voltage_low == None:
                plant_voltage_low = 0.0
            if plant_voltage_high == None:
                plant_voltage_high = -100.0
            if plant_voltage > plant_voltage_high:
                plant_voltage_high = plant_voltage
            if plant_voltage < plant_voltage_low:
                plant_voltage_low = plant_voltage
        generator = None
        if sensors['generator']['sensor'] == True:
            generator = float(sensors['generator']['value'])
            if generator_low == None:
                generator_low = 100.0
            if generator_high == None:
                generator_high = 0.0
            if generator > generator_high:
                generator_high = generator
            if generator < generator_low:
                generator_low = generator

        hydrogen = None
        if sensors['hydrogen']['sensor'] == True:
            hydrogen = float(sensors['hydrogen']['value'])
            if hydrogen_low == None:
                hydrogen_low = 5
            if hydrogen_high == None:
                hydrogen_high = 0
            if hydrogen > hydrogen_high:
                hydrogen_high = hydrogen
            if hydrogen < hydrogen_low:
                hydrogen_low = hydrogen
        
        
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

        ##################################################################
        # Removes first line in CSV when there are 24 hours of minute data
        # empty list to append CSV data before deleting oldest line and rewriting data as new csv.
        list_removed_first = []
        totalrows = sum(1 for line in open('csv/{}/minute.csv'.format(hostname)))
        print("Total lines - " + str(totalrows))
        # 1140 is number of minutes in 24 hours. Keeps one day of data.
        if totalrows >= 1140:
            with open('csv/{}/minute.csv'.format(hostname), 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    list_removed_first.append(row)
                del list_removed_first[1]

            writeData = open('csv/{}/minute.csv'.format(hostname), 'w')
            with writeData:
                writer = csv.writer(writeData)
                writer.writerows(list_removed_first)

        
        ###########################################################################
        # Pull up previous last row in CSV to compare to one just written for logic  
        need_to_delete_json = False
        if totalrows >= 4:
            previous_row_hour= 25
            this_row_minute = 25
            
            with open('csv/{}/minute.csv'.format(hostname), 'r') as csv_file:
                try:
                    #Number after (csv_vile), is how many lines from end of file
                    lastrow = deque(csv.reader(csv_file), 2)[0]
                except IndexError:  # empty file
                    lastrow = None
                this_line_time = lastrow[0]
                # remove minutes from string
                hour = this_line_time[:-3]
                # remove date from string - leaving only the hour number
                previous_row_hour = int(float(hour.split(' ', 1)[-1]))
                print("Previous hour number - " + str(previous_row_hour))
                print("Current hour number - " + str(current_hour))
                current_hour= int(float((datetime.now().strftime('%H'))))
                if current_hour != previous_row_hour:
                    need_to_delete_json = True
                    # Append high/low data to hourly csv

                    if not os.path.isfile('csv/{}/hour.csv'.format(hostname)):
                        writeHeaders = open('csv/{}/hour.csv'.format(hostname), 'a')
                        with writeHeaders:
                            csvfields = [["timestamp", "temp_internal_high", "temp_internal_low", "door_high", "door_low", "door2_high", "door2_low", "door3_high", "door3_low", "smoke_high", "smoke_low", "power_failure_high", "power_failure_low", "flood_high", "flood_low", "flood2_high", "flood2_low", "remote_temp_high", "remote_temp_low", "generator_high", "generator_low", "hydrogen_high", "hydrogen_low"]]
                            writer = csv.writer(writeHeaders)
                            writer.writerows(csvfields)

                    appendHourRow = open('csv/{}/hour.csv'.format(hostname), 'a')
                    with appendHourRow:
                        hourlycsvfields = [[csvtimestamp, temp_internal_high, temp_internal_low, door_high, door_low, door2_high, door2_low, door3_high, door3_low, smoke_high, smoke_low, power_failure_high, power_failure_low, flood_high, flood_low, flood2_high, flood2_low, remote_temp_high, remote_temp_low, generator_high, generator_low, hydrogen_high, hydrogen_low]]
                        writer = csv.writer(appendHourRow)
                        writer.writerows(hourlycsvfields)      
                
                




        print("Writing complete")



        value_extremes = {"timestamp": {
                                        "time": csvtimestamp
                                        },
                        "temp_internal": {
                                        "high": temp_internal_high,
                                        "low": temp_internal_low
                                        },
                                "door": {
                                        "high": door_high,
                                        "low": door_low
                                        },
                                "door2": {
                                        "high": door2_high,
                                        "low": door2_low
                                        },
                                "door3": {
                                        "high": door3_high,
                                        "low": door3_low
                                        },
                                "smoke": {
                                        "high": smoke_high,
                                        "low": smoke_low
                                        },
                        "power_failure": {
                                        "high": power_failure_high,
                                        "low": power_failure_low
                                        },
                                "flood": {
                                        "high": flood_high,
                                        "low": flood_low
                                        },
                                "flood2": {
                                        "high": flood2_high,
                                        "low": flood2_low
                                        },
                            "remote_temp": {
                                        "high": remote_temp_high,
                                        "low": remote_temp_low
                                        },
                        "plant_voltage": {
                                        "high": plant_voltage_high,
                                        "low": plant_voltage_low
                                        },
                            "generator": {
                                        "high": generator_high,
                                        "low": generator_low
                                        },
                            "hydrogen": {
                                        "high": hydrogen_high,
                                        "low": hydrogen_low
                                        }
                            }

        with open('csv/{}/hourly_extremes.json'.format(hostname), 'w') as json_file:
            json.dump(value_extremes, json_file)

        if need_to_delete_json == True:
            os.remove('csv/{}/hourly_extremes.json'.format(hostname))


            

    '''
    ##################################################
    # Find first and last total pdu values in csv file
    def hourValues():  
        with open('csv/{}/minute.csv'.format(hostname), 'r') as csv_file:
            next(csv_file)
            csv_reader = csv.reader(csv_file)

            timestamp = ""
            last_line_hour = ""

            hourly_temps = []
            all_values = []

            hour_low = 0.00
            hour_high = 0.00
            for line in csv_reader:
                this_line_time = line[0]
                # remove minutes from string
                hour = this_line_time[:-3]
                # remove date from string
                ######
                this_hour_number = hour.split(' ', 1)[-1]
                this_line_temp = float(line[1])

                if last_line_hour == "":
                    last_line_hour = this_hour_number
                    timestamp = this_line_time
                    hourly_temps.append(this_line_temp)

                else:
                    if last_line_hour == this_hour_number:
                        hourly_temps.append(this_line_temp)
                    else:
                        hourly_dict = {"timestamp":timestamp, "temps":hourly_temps}
                        all_values.append(hourly_dict)
                        last_line_hour = this_hour_number
                        timestamp = this_line_time
                        hourly_temps = []
                            


            processed_temp_list = []
            final_values = []
            for temp_list in all_values:
                division_count = 0
                added_total = 0
                high_temp = 0.00
                low_temp = 200.00
                all_temperatures = (temp_list["temps"])
                hourly_timestamp = (temp_list["timestamp"])
                for temp in all_temperatures:
                    added_total += temp
                    division_count += 1
                    if temp > high_temp:
                        high_temp = temp
                    if temp < low_temp:
                        low_temp = temp


                processed_temps = {"timestamp": hourly_timestamp,
                                "high_temp": high_temp,
                                "low_temp": low_temp}
                
                processed_temp_list.append(processed_temps)



            
            for line in processed_temp_list:
                csvfields = ["timestamp", "high_temp", "low_temp"]
                csvdata = [line['timestamp'], line['high_temp'], line['low_temp']]
                final_values.append(csvdata)
            
            print(final_values)
            

            myFile = open('csv/{}/hour.csv'.format(hostname), 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(final_values)
                
            print("Writing complete")

            def get_last_row(csv_filename):
            with open(csv_filename, 'r') as f:
            try:
                lastrow = deque(csv.reader(f), 1)[0]
            except IndexError:  # empty file
                lastrow = None
            return lastrow
    '''

    ##############################
    # To test for naming in Geist of individual sensors
    # for device in dashboard_data:
    #    print("\n")
    #    print(device["device"]["name"])
    #    print(device["device"]["ip_address"] + "/#overview")
