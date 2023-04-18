
function getTotal() {
    var num = document.getElementById("number").value;
    var ticket_price = document.getElementById("price").value;
    document.getElementById('total').value = Number(num) * Number(ticket_price);
}


function confirmDeleteShow() {
    alert('You clicked for alert');
}