$(function() { 
    const element = document.getElementsByClassName("button")


    for (var i = 0; i < element.length; i++) {  
        element[i].addEventListener("click", () => {
            alert(element[i].id)
            console.log(element[i].id)
        });
    }
});