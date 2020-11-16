var $url_register = window.location.origin + "/api/register"
var $url_consult = window.location.origin + "/api/consult"

function update_event(event, pause_id, hour) {
    if (hour){
        $("#" + event + "-" + pause_id + " label").text(hour)
        $("#" + event + "-" + pause_id + " button").attr("disabled", "disabled")
    };
}

function update_entry(hour) {
    if (hour) {
        $("#entry label").text(hour)
        $("#entry button").attr("disabled", "disabled")
    };
}

function update_finish(hour) {
    if (hour) {
        $("#finish label").text(hour)
        $("#finish button").attr("disabled", "disabled")
    };
}

function disable_buttons(){
    $(".form-body button").attr("disabled", "disabled");
}

$(document).ready(function () {
    today = moment().format("YYYY-MM-DD")
    $.ajax({
        url: $url_consult + "?date=" + today,
        type: "GET",
        success: function (response) {
            console.log(response)
            update_entry(response.entry)
            update_finish(response.finish)
            if (response.pauses) {
                $.each(response.pauses, function (index, register) {
                    update_event("entry", register.pause_id, register.entry)
                    update_event("finish", register.pause_id, register.finish)
                });
            };
            if (response.finish){
                disable_buttons();
            };
        }
    });
});

function register_pause(pause_id, event) {
    $.ajax({
        url: $url_register,
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            id: pause_id,
            event: event,
            type: "pause"
        }),
        success: function (response) {
            update_event("entry", response.data.pause_id, response.data.entry)
            update_event("finish", response.data.pause_id, response.data.finish)
        },
        error: function (response) {
            console.log(response)
            alert(JSON.parse(response.response).message)
        }
    })
}


function register_entry() {
    $.ajax({
        url: $url_register,
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            id: 0,
            event: "entry",
            type: "register"
        }),
        success: function (response) {
            console.log(response)
            update_entry(response.data.entry)
        },
        error: function (response) {
            console.log(response)
            alert(JSON.parse(response.response).message)
        }
    })
}


function register_finish() {
    $.ajax({
        url: $url_register,
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            id: 0,
            event: "finish",
            type: "register"
        }),
        success: function (response) {
            update_finish(response.data.finish)
            disable_buttons();
        },
        error: function (response) {
            alert(JSON.parse(response.response).message)
        }
    })
}
