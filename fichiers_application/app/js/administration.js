const listRoomsGroups = document.getElementById("listRoomsGroups");
const listRooms = document.getElementById("listRooms");
const formCreateGroup = document.getElementById("formCreateGroup");
const formAddRoomToGroup = document.getElementById("formAddRoomToGroup");
const listDeleteRoomsGroups = document.getElementById("listDeleteRoomsGroups");
const formDeleteGroup = document.getElementById("formDeleteGroup");
const formForceParse = document.getElementById("formForceParse");
const formUpdateRole = document.getElementById("formUpdateRole");
const listRoles = document.getElementById("role-select");
const divMail = document.getElementById("divMail");
const textMail = document.getElementById("textMail");
const listadmin = document.getElementById("listadmin");
const buttonAddRoomToGroup = document.getElementById("buttonAddRoomToGroup");
var users = [];

formCreateGroup.addEventListener("submit", newGroup);
formAddRoomToGroup.addEventListener("submit", addRoomToGroup);
listRoomsGroups.addEventListener("change", loadRooms);
formDeleteGroup.addEventListener("submit", deleteGroup);
formForceParse.addEventListener("submit", forceParse);
formUpdateRole.addEventListener("submit", updateRole);


loadRoomsGroups();
getUsers();
loadAdmin();

function loadRoomsGroups(){
    getRoomsGroups(1);
	getRoomsGroups(3);
}

function loadRooms(){
	if(listRoomsGroups.options[listRoomsGroups.selectedIndex].value == ""){
		listRooms.innerHTML = '<option value=""></option>';
	}
	else{
		getRooms(listRoomsGroups.options[listRoomsGroups.selectedIndex].value, 2);
	}
}

function newGroup(e) {
	e.preventDefault();
    let groupName = document.getElementById('groupeName').value;
    if (groupName === "") { 
        alert("Rentrez un nom de groupe non vide"); 
        return;
    }
	getRoomsGroups(2);
}

function addRoomToGroup(e){
	e.preventDefault();
	let group = listRoomsGroups.options[listRoomsGroups.selectedIndex].value;
	if(group != ""){
		let room = listRooms.options[listRooms.selectedIndex].value;
		insertRoomInGroup(group, room);
	}
}

function deleteGroup(e){
    e.preventDefault();
	deleteGroupDB(listDeleteRoomsGroups.options[listDeleteRoomsGroups.selectedIndex].value);
}

function forceParse(e){
	e.preventDefault();
	forceParseDB();
	alert("Attendez environ 1 minute pour voir les changements");
}

function updateRole(e){
	e.preventDefault();
	updateRoleDB(textMail.value, listRoles.options[listRoles.selectedIndex].value)
}


function filtreListe(){
	var texte, filter, ul, li, a, i, txtValue;

	texte = document.getElementById('textMail');
	if(texte.value == ""){
		divMail.style.display = "none";
	}else{
		divMail.style.display = "block";
	}
	filter = texte.value.toUpperCase();
	ul = document.getElementById("listMail");
	li = ul.getElementsByTagName('li');
	for (i = 0; i < li.length; i++) {
		a = li[i].getElementsByTagName("a")[0];
		txtValue = a.textContent || a.innerText;
		if (txtValue.toUpperCase().indexOf(filter) > -1) {
		  li[i].style.display = "";
		} else {
		  li[i].style.display = "none";
		}
	}
}

function addMail(){
	let ul = document.getElementById("listMail");
	for(let i = 0; i < users.length; i++){
		let li = document.createElement("li");
		let a = document.createElement("a");
		a.textContent = users[i].mail;
		a.addEventListener("click",Inputmail)
		li.appendChild(a);
		ul.appendChild(li);
	}
}

function loadAdmin(){
	getAdmin();
}

function Inputmail(e){
	e.preventDefault();
	textMail.value = e.target.textContent;
}
