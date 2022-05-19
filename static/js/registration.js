$(function() { $('#form').submit(function() {
    Name = document.getElementsByName("name")[0].value
    surname = document.getElementsByName("surename")[0].value
    username = document.getElementsByName("username")[0].value
    email = document.getElementsByName("email")[0].value
    if (Name == null || Name == "") {
        $("#errors").append("Username is empty")
        return false;
    }
    if (surname == null || surname == "") {
        $("#errors").append("Surname is empty")
        return false
    }
    if (username == null || username == "") {
        $("#errors").append("name is empty")
        return false
    }
    if (email == null || email == "") {
        $("#errors").append("Email is empty")
        return false
    }
    pass = document.getElementById("Password").value
    passConf = document.getElementById("PasswordConfirmation").value
    if (pass != passConf) {
        $("#errors").append("Incorrect password")
        return false
    }
    return false
})})