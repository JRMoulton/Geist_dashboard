$(document).ready(run_update)

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

        id.children(".temp_internal").children().html(data[device].temp_internal.value); //temp_internal update

        if (data[device].door.sensor == true) {
            if (data[device].door.state == "Normal") {
                id.children(".door").children().attr("src","/static/img/door_normal.png");
            } else if (data[device].door.state == "Warning") {
                id.children(".door").children().attr("src","/static/img/door_warning.png");
            } else {
                id.children(".door").children().attr("src", "/static/img/door_critical.png");
           };
        };

        if (data[device].smoke.sensor == true) {
            if (data[device].smoke.state == "Normal") {
                id.children(".smoke").children().attr("src","/static/img/smoke_normal.png");
            } else if (data[device].smoke.state == "Warning") {
                id.children(".smoke").children().attr("src", "/static/img/smoke_warning.png");
            } else {
                id.children(".smoke").children().attr("src", "/static/img/smoke_warning.png");
            };
        };

        if (data[device].power_failure.sensor == true) {
            if (data[device].power_failure.state == "Normal") {
                id.children(".commercial_power").children().attr("src", "/static/img/commercial_power_normal.png");
            } else if (data[device].power_failure.state == "Warning") {
                id.children(".commercial_power").children().attr("src", "/static/img/commercial_power_warning.png");
            } else {
                id.children(".commercial_power").children().attr("src", "/static/img/commercial_power_critical.png");
            };
        };     
    
        if (data[device].flood.sensor == true) {
            if (data[device].flood.state == "Normal") {
                id.children(".flood").children().attr("src", "/static/img/flood_normal.png");
            } else if (data[device].flood.state == "Warning") {
                id.children(".flood").children().attr("src", "/static/img/flood_warning.png");
            } else {
                id.children(".flood").children().attr("src", "/static/img/flood_warning.png");
           };
        };

        if (data[device].remote_temp.sensor == true) {
            id.children(".remote_temp").children().html(data[device].remote_temp.value)
            if (data[device].remote_temp.state == "Normal") {
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_normal.png");
                document.getElementById(data[device].device.name + "_temp").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_temp").classList.add("color_normal"); 
            } else if (data[device].remote_temp.state == "Warning") {
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_warning.png");
                document.getElementById(data[device].device.name + "_temp").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_temp").classList.add("color_warning"); 
            } else if (data[device].remote_temp.state == "Low") {
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_low.png");
                document.getElementById(data[device].device.name + "_temp").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_temp").classList.add("color_low"); 
            } else {
                id.children(".remote_temp").children().attr("src", "/static/img/remote_temp_critical.png");
                document.getElementById(data[device].device.name + "_temp").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_temp").classList.add("color_critical"); 
            }
        };

        if (data[device].plant_voltage.sensor == true) {
            id.children(".plant_voltage").children().html(data[device].plant_voltage.value)
            if (data[device].plant_voltage.state == "Normal") {
                id.children(".plant_voltage").children().attr("src", "/static/img/plant_voltage_normal.png");
                document.getElementById(data[device].device.name + "_volt").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_volt").classList.add("color_normal"); 
            } else if (data[device].plant_voltage.state == "Warning") {
                id.children(".plant_voltage").children().attt("src", "/static/img/plant_voltage_warning.png");
                document.getElementById(data[device].device.name + "_volt").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_volt").classList.add("color_warning");
            } else {
                id.children(".plant_voltage").children().attr("src", "/static/img/plant_voltage_critical.png");
                document.getElementById(data[device].device.name + "_volt").classList.remove("color_warning", "color_low", "color_critical", "color_normal");
                document.getElementById(data[device].device.name + "_volt").classList.add("color_critical");
            };
        };

        if (data[device].generator.sensor == true) {
            if (data[device].generator.state == "Normal") {
                id.children(".generator").children().attr("src", "/static/img/generator_normal.png");
            } else if (data[device].generator.state == "Warning") {
                id.children(".generator").children().attr("src", "/static/img/generator_warning.png");
            } else {
                id.children(".generator").children().attr("src", "/static/img/generator_critical.png");
            };
        };

        if (data[device].hydrogen.sensor == true) {
            if (data[device].hydrogen.state == "Normal") {
                id.children(".hydrogen").children().attr("src", "/static/img/hydrogen_normal.png");
            } else if (data[device].hydrogen.state == "Warning") {
                id.children(".hydrogen").children().attr("src", "/static/img/hydrogen_warning.png");
            } else {
                id.children(".hydrogen").children().attr("src", "/static/img/hydrogen_critical.png");
           };
        };
    };
};

setInterval(run_update, 30*1000)