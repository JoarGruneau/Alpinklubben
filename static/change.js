function change_form(change_to) {
    var form_changes = document.getElementsByClassName("change_form");
    var i;
    for (i = 0; i < form_changes.length; i++) {
        form_changes[i].value = change_to;
    };
};



function change_text(change_to) {
    var text_changes = document.getElementsByClassName("change_text");
    var i;
    for (i = 0; i < text_changes.length; i++) {
        text_changes[i].innerHTML = change_to;
    }
}

function change_price(change_to, scale) {
    var price_changes = document.getElementsByClassName("change_price");
    var i;
    var number;
    for (i = 0; i < price_changes.length; i++) {
        number = parseInt(price_changes[i].innerHTML.replace(/[^0-9\.]/g, ''), 10);
        price_changes[i].innerHTML = change_to + ": " + number*scale + " kr";
    }
}