function confirm_password(password, confirm_password){
    if(password == confirm_password){
        postFunction();
    }else{
        window.alert("Password doesn't match!");
    }
    window.alert("Password doesn't match!");
}

function postFunction(){
    var ajax = new XMLHttpRequest();
    var data = document.getElementById("registration_form");
    var formData = new FormData(data);
    ajax.open("POST","/register_account", true);
    ajax.send(formData);
}

function show_pet_modal(){
    document.getElementById('modal_pet').style.display = 'block'
    document.getElementById('modal_pet').style.opacity = 1
}

function show_serv_modal(){
    document.getElementById('serv_mod').style.display = 'block'
    document.getElementById('serv_mod').style.opacity = 1;
}


function close_modal(){
    document.getElementById('serv_mod').style.opacity = 0;
    setTimeout(function() { display_none(); }, 1000);
}

function display_none(){
    document.getElementById('serv_mod').style.display='none';
}

function admin_inquiry_modal(id, p_id, o_id, service, date, venue){
    document.getElementById('modal').style.display = 'block';
    document.getElementById('record_id').value = id;
    document.getElementById('pet_id').value = p_id;
    document.getElementById('owner_id').value = o_id;
    document.getElementById('service').value = service;
    document.getElementById('date').value = date;
    document.getElementById('venue').value = venue;
}

function admin_inquiry_modal_close(){
    document.getElementById('modal').style.display = 'none';
    document.getElementById('record_id').value = '';
    document.getElementById('pet_id').value = '';
    document.getElementById('owner_id').value = '';
    document.getElementById('service').value = '';
    document.getElementById('date').value = '';
    document.getElementById('venue').value = 'vue';
}

function admin_transact_modal(id, p_id, o_id, service, date, venue){
    document.getElementById('transact_modal').style.display = 'block';
    document.getElementById('rid').value = id;
    document.getElementById('pid').value = p_id;
    document.getElementById('owner_id_1').value = o_id;
    document.getElementById('service_1').value = service;
    document.getElementById('date_1').value = date;
    document.getElementById('venue_1').value = venue;
}

function admin_transact_modal_close(){
    document.getElementById('transact_modal').style.display = 'none';
}