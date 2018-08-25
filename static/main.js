$(document).ready(run_update)
setInterval(run_update, 3*1000)
function run_update() {
    $.getJSON( "/static/data.json?" + Math.random())
        .done(updateData)
        

        .fail(function(){
            console.log("failed to read data");
        })
};


function updateData(data) {
    for (device in data) {
        id = $("#" + data[device].device.name).children();  //Selector for the sensor values

        if (data[device].device.geist_criticality == "Normal"){
            document.getElementById(data[device].device.name).classList.remove("warning", "low", "critical", "normal");
            document.getElementById(data[device].device.name).classList.add("normal");
        } else if (data[device].device.geist_criticality == "Warning"){
            document.getElementById(data[device].device.name).classList.remove("warning", "low", "critical", "normal");
            document.getElementById(data[device].device.name).classList.add("warning");
        } else if (data[device].device.geist_criticality == "Low"){
            document.getElementById(data[device].device.name).classList.remove("warning", "low", "critical", "normal");
            document.getElementById(data[device].device.name).classList.add("low");
        } else {
            document.getElementById(data[device].device.name).classList.remove("warning", "low", "critical", "normal");
            document.getElementById(data[device].device.name).classList.add("critical");
        }

        id.children(".temp_internal").children().html(data[device].temp_internal.value); //temp_internal update
        if (data[device].temp_internal.state == "Normal"){
            document.getElementById(data[device].device.name + "_temp_in").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
            document.getElementById(data[device].device.name + "_temp_in").classList.add("color_normal");
        } else if (data[device].temp_internal.state == "Warning"){
            document.getElementById(data[device].device.name + "_temp_in").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
            document.getElementById(data[device].device.name + "_temp_in").classList.add("color_warning");
        } else if (data[device].temp_internal.state == "Low"){
            document.getElementById(data[device].device.name + "_temp_in").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
            document.getElementById(data[device].device.name + "_temp_in").classList.add("color_low");
        } else {
            document.getElementById(data[device].device.name + "_temp_in").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
            document.getElementById(data[device].device.name + "_temp_in").classList.add("color_critical");

        }

        if (data[device].door.sensor == true) {
            if (data[device].door.state == "Normal") {
                document.getElementById(data[device].device.name + "_door_tooltip").innerHTML = (data[device].door.label) + " is Closed";
                id.children(".door").children().attr("src","/static/img/door_normal.png");
            } else if (data[device].door.state == "Warning") {
                document.getElementById(data[device].device.name + "_door_tooltip").innerHTML = (data[device].door.label) + " is open during business hours";
                id.children(".door").children().attr("src","/static/img/door_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_door_tooltip").innerHTML = (data[device].door.label) + " is Open";
                id.children(".door").children().attr("src", "/static/img/door_critical.png");
           };
        };

        if (data[device].door2.sensor == true) {
            if (data[device].door2.state == "Normal") {
                document.getElementById(data[device].device.name + "_door2_tooltip").innerHTML = (data[device].door2.label) + " is Closed";
                id.children(".door").children().attr("src","/static/img/door_normal.png");
            } else if (data[device].door2.state == "Warning") {
                document.getElementById(data[device].device.name + "_door2_tooltip").innerHTML = (data[device].door2.label) + " is open during business hours";
                id.children(".door").children().attr("src","/static/img/door_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_door2_tooltip").innerHTML = (data[device].door2.label) + " is Open";
                id.children(".door").children().attr("src", "/static/img/door_critical.png");
           };
        };

        if (data[device].door3.sensor == true) {
            if (data[device].door3.state == "Normal") {
                document.getElementById(data[device].device.name + "_door3_tooltip").innerHTML = (data[device].door3.label) + " is Closed";
                id.children(".door").children().attr("src","/static/img/door_normal.png");
            } else if (data[device].door3.state == "Warning") {
                document.getElementById(data[device].device.name + "_door3_tooltip").innerHTML = (data[device].door3.label) + " is open during business hours";
                id.children(".door").children().attr("src","/static/img/door_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_door3_tooltip").innerHTML = (data[device].door3.label) + " is Open";
                id.children(".door").children().attr("src", "/static/img/door_critical.png");
           };
        };

        if (data[device].smoke.sensor == true) {
            if (data[device].smoke.state == "Normal") {
                document.getElementById(data[device].device.name + "_smoke_tooltip").innerHTML = (data[device].smoke.label) + " State is Normal";
                id.children(".smoke").children().attr("src","/static/img/smoke_normal.png");
            } else if (data[device].smoke.state == "Warning") {
                document.getElementById(data[device].device.name + "_smoke_tooltip").innerHTML = (data[device].smoke.label) + " State is set to Warning";
                id.children(".smoke").children().attr("src", "/static/img/smoke_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_smoke_tooltip").innerHTML = (data[device].smoke.label) + " is in Alarm";
                id.children(".smoke").children().attr("src", "/static/img/smoke_critical.png");
            };
        };

        if (data[device].power_failure.sensor == true) {
            if (data[device].power_failure.state == "Normal") {
                document.getElementById(data[device].device.name + "_power_tooltip").innerHTML = "Commercial Power is Available";
                id.children(".commercial_power").children().attr("src", "/static/img/commercial_power_normal.png");
            } else if (data[device].power_failure.state == "Warning") {
                document.getElementById(data[device].device.name + "_power_tooltip").innerHTML = "Commercial Power State - Warning";
                id.children(".commercial_power").children().attr("src", "/static/img/commercial_power_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_power_tooltip").innerHTML = "Commercial Power has Failed";
                id.children(".commercial_power").children().attr("src", "/static/img/commercial_power_critical.png");
            };
        };     
    
        if (data[device].flood.sensor == true) {
            if (data[device].flood.state == "Normal") {
                document.getElementById(data[device].device.name + "_flood_tooltip").innerHTML = "Flood Sensor is Dry";
                id.children(".flood").children().attr("src", "/static/img/flood_normal.png");
            } else if (data[device].flood.state == "Warning") {
                document.getElementById(data[device].device.name + "_flood_tooltip").innerHTML = "Flood Sensor State - Warning";
                id.children(".flood").children().attr("src", "/static/img/flood_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_flood_tooltip").innerHTML = "Flood Sensor is Wet";
                id.children(".flood").children().attr("src", "/static/img/flood_warning.png");
           };
        };

        if (data[device].remote_temp.sensor == true) {
            document.getElementById(data[device].device.name + "_rem_temp").innerHTML = (data[device].remote_temp.value);
            //id.children(".remote_temp").children().html(data[device].remote_temp.value)
            if (data[device].remote_temp.state == "Normal") {
                document.getElementById(data[device].device.name + "_rem_temp_tooltip").innerHTML = (data[device].remote_temp.label) + " Temperature is Normal";
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_normal.png");
                document.getElementById(data[device].device.name + "_rem_temp").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_rem_temp").classList.add("color_normal"); 
            } else if (data[device].remote_temp.state == "Warning") {
                document.getElementById(data[device].device.name + "_rem_temp_tooltip").innerHTML = "Remote Temperature State is Normal";
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_warning.png");
                document.getElementById(data[device].device.name + "_rem_temp_tooltip").innerHTML = (data[device].remote_temp.label) + " Temperature getting too warm";
                document.getElementById(data[device].device.name + "_rem_temp").classList.add("color_warning");
            } else if (data[device].remote_temp.state == "Low") {
                document.getElementById(data[device].device.name + "_rem_temp_tooltip").innerHTML = "Remote Temperature State is Normal";
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_low.png");
                document.getElementById(data[device].device.name + "_rem_temp_tooltip").innerHTML = (data[device].remote_temp.label) + " Temperature is too low";
                document.getElementById(data[device].device.name + "_rem_temp").classList.add("color_low"); 
            } else {
                document.getElementById(data[device].device.name + "_rem_temp_tooltip").innerHTML = (data[device].remote_temp.label) + " Temperature is too hot";
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_critical.png");
                document.getElementById(data[device].device.name + "_rem_temp").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_rem_temp").classList.add("color_critical"); 
            }
        };

        if (data[device].plant_voltage.sensor == true) {
            id.children(".plant_voltage").children().html(data[device].plant_voltage.value)
            if (data[device].plant_voltage.state == "Normal") {
                id.children(".plant_voltage").children().attr("src", "/static/img/plant_voltage_normal.png");
                document.getElementById(data[device].device.name + "_volt_tooltip").innerHTML = "Plant Voltage is Normal at " + (data[device].plant_voltage.value) + "V";
                document.getElementById(data[device].device.name + "_volt").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_volt").classList.add("color_normal"); 
            } else if (data[device].plant_voltage.state == "Warning") {
                id.children(".plant_voltage").children().attr("src", "/static/img/plant_voltage_warning.png");
                document.getElementById(data[device].device.name + "_volt_tooltip").innerHTML = "Plant Voltage is Getting Low at " + (data[device].plant_voltage.value) + "V";
                document.getElementById(data[device].device.name + "_volt").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_volt").classList.add("color_warning");
            } else {
                id.children(".plant_voltage").children().attr("src", "/static/img/plant_voltage_critical.png");
                document.getElementById(data[device].device.name + "_volt_tooltip").innerHTML = "Plant Voltage is Critically low at " + (data[device].plant_voltage.value) + "V";
                document.getElementById(data[device].device.name + "_volt").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_volt").classList.add("color_critical");
            };
        };

        if (data[device].generator.sensor == true) {
            if (data[device].generator.state == "Normal") {
                document.getElementById(data[device].device.name + "_gen_tooltip").innerHTML = "Generator Normal - Load " + (data[device].generator.value) + " Amps";
                id.children(".generator").children().attr("src", "/static/img/generator_normal.png");
            } else if (data[device].generator.state == "Warning") {
                document.getElementById(data[device].device.name + "_gen_tooltip").innerHTML = "Generator Warning - Load " + (data[device].generator.value) + " Amps";
                id.children(".generator").children().attr("src", "/static/img/generator_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_gen_tooltip").innerHTML = "Generator is Running - " + (data[device].generator.value) + " Amps";
                id.children(".generator").children().attr("src", "/static/img/generator_critical.png");
            };
        };

        if (data[device].hydrogen.sensor == true) {
            if (data[device].hydrogen.state == "Normal") {
                document.getElementById(data[device].device.name + "_hydro_tooltip").innerHTML = "Hydrogen Level is Normal at " + (data[device].hydrogen.value) + "% LEL";
                id.children(".hydrogen").children().attr("src", "/static/img/hydrogen_normal.png");
            } else if (data[device].hydrogen.state == "Warning") {
                document.getElementById(data[device].device.name + "_hydro_tooltip").innerHTML = "Hydrogen Level in Warning State at " + (data[device].hydrogen.value) + "% LEL";
                id.children(".hydrogen").children().attr("src", "/static/img/hydrogen_warning.png");
            } else {
                document.getElementById(data[device].device.name + "_hydro_tooltip").innerHTML = "Hydrogen Level Critical at " + (data[device].hydrogen.value) + "% LEL";
                id.children(".hydrogen").children().attr("src", "/static/img/hydrogen_critical.png");
           };
        };
    };
};

