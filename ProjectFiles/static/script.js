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