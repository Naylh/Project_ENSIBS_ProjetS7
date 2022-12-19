const buttonLogin = document.getElementById('buttonLogin');

buttonLogin.addEventListener('click',redirectPlanning);

function redirectPlanning() {
    location.href = "/planning";
}
