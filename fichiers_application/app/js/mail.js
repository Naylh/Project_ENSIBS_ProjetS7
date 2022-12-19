let contact = document.getElementById("contact");
let boutton = document.getElementById("boutton");
let texte = document.getElementById("texte");
var users = [];
let list = document.getElementById("menu-deroulant");
let listMail = document.getElementById("list-mail");
let Talerte = document.getElementById('tauxAlerte');
let Tvalue = document.getElementById('alerteValue');
let salle = document.getElementById('bodySalle');

boutton.addEventListener("change", addWhoContact);
texte.addEventListener("change", filtreListe);
update.addEventListener("click", insertTauxAlerte);
formFilter.addEventListener("submit", checkFilter);
listRoomsGroups.addEventListener("change", loadRooms);

getUsers();
getWhoContact();
tauxAlerte();
loadRoomsGroups();

function addWhoContact(e){
    e.preventDefault();
    setWhoContact();
}

boutton.onclick = addWhoContact;

function loadRoomsGroups(){
    getRoomsGroups(1);
}

function loadRooms(){
    getRooms(listRoomsGroups.options[listRoomsGroups.selectedIndex].value, 1);
}

function checkFilter(e) {
    e.preventDefault();
    let checkCb = false;
    let rooms = [];
    salle.innerHTML="";
    for (let i=0, row; row = roomsTable.rows[i]; i++) {
        for (let j=0, col; col = roomsTable.rows[i].cells[j]; j+=2) {
            if(col.firstChild.checked == true ){
                checkCb = true;
                rooms.push(roomsTable.rows[i].cells[j+1].innerHTML);
                let tr = document.createElement("tr");
                let td = document.createElement("td");
                td.textContent = roomsTable.rows[i].cells[j+1].innerHTML;
                tr.appendChild(td);
                salle.appendChild(tr);
            }
         }  
      
    }
if(!checkCb){
    alert("Il faut sélectionner au moins une salle");
    return;
}
}



function filtreListe(){
  var texte, filter, ul, li, a, i, txtValue;
  
  texte = document.getElementById('texte');
  if(texte.value == ""){
    listMail.style.display = "none";

  }else{
    listMail.style.display = "block";
  }
  filter = texte.value.toUpperCase();
  ul = document.getElementById("ul");
  li = ul.getElementsByTagName('li');
  for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("a")[0];
      txtValue = a.textContent;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
}

function addMail(){
  
  let ul = document.getElementById("ul");
  for(let i = 0; i < users.length; i++){
    let li = document.createElement("li");
    let a = document.createElement("a");
    a.textContent = users[i].mail;
    a.addEventListener("click",Inputmail);
    li.appendChild(a);
    ul.appendChild(li);
  }
}

function Inputmail(e){
  e.preventDefault();
  texte.value = e.target.textContent;
}

function tauxAlerte(){
  Tvalue.textContent = Talerte.value;
}


function insertTauxAlerte(e){
	e.preventDefault();
  for(let i = 0; i < salle.childElementCount; i++){
    updateTaux(Talerte.value, salle.children[i].textContent);
  }
}


  