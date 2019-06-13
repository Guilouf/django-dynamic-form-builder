function getForm(choice_pk) {
    /*Change the form when the selector state changes and get the form from a request*/
    let xhr = new XMLHttpRequest();
    // Fake url arg just for reverse the root of the url
    xhr.open("GET", "{% url 'template' 42 %}".replace('42', choice_pk), true);
    xhr.send();  // Get the html form code
    xhr.onreadystatechange = function () {
        if(xhr.readyState === 4 && xhr.status === 200) {  // trigger if request ok
            appendForm(xhr.response)
        } else { // no choice ----- form erased
            appendForm(null)
        }
    }
}

    function appendForm(form) {
        /*Modify the form on the fly*/
        document.getElementById('overridable').innerHTML = form;
    }
