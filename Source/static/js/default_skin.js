var defultComplexNetSystemCT = {
    Sensors: ["Training", "Simulation", "Playback"],
    Sords: ["ooo", "yyy", "zzz"],
    Looks: ["aaa", "bbb", "ccc"],
    Hears: ["ddd", "eee", "fff"],
    Glasses: ["hhh", "lll", "mmm"]
}

var defultComplexNetConfigCT = {
    Link_System: ["System1", "System2", "System3"],
    Link_Ext_Simulation: ["System1", "System2", "System3"],
    Simulation_Watch: ["W", "W2", "W3"],
    Simulation_DIS: ["D1", "D2", "D3"],
    Simulation_Ext_Sim_Flag: false,
    Backup_Env: ["Env1", "Env2", "Env3"],
    Backup_env_sim_Flag: true
}

function ChangeComplexNetHeaders() {
    $('#HeaderLink')[0].innerHTML = "hi";
    $('#HeaderSimulation')[0].innerHTML = "cat";
    $('#HeaderConfigC')[0].innerHTML = "in";
    $('#HeaderSensors')[0].innerHTML = "the";
    $('#HeaderGlasses')[0].innerHTML = "hat";
    $('#HeaderSord')[0].innerHTML = "hatSord";
    $('#HeaderWatch')[0].innerHTML = "hatWatch";
    $('#HeaderHear')[0].innerHTML = "Banana";
    $('#HeaderGlasses')[0].innerHTML = "Orange"
}

function fillComplexNetDefaultCT() {
    // Config Data
    var keys2 = Object.keys(Config_form_controls);
    for (k = 0; k < keys2.length; k++) {
        var obj = Config_form_controls[keys2[k]];
        var data = defultComplexNetConfigCT[keys2[k]];
        clear_object(obj);
        fill_object(obj, data);
    }

    // Complex Net Data
    var keys = Object.keys(Complex_Net_form_controls);

    for (j = 0; j < keys.length; j++) {
        var keys2 = Object.keys(Complex_Net_form_controls[keys[j]]);
        for (k = 0; k < keys2.length; k++) {
            var obj = Complex_Net_form_controls[keys[j]][keys2[k]];
            clear_object(obj);
            fill_object(obj, defultComplexNetSystemCT[keys[j]]);
        }
    }
}