const listRoomsGroups = document.getElementById('listRoomsGroups');
const saveFilter = document.getElementById('saveFilter');
const deleteFilter = document.getElementById('deleteFilter');
const timeFrom = document.getElementById('timeFrom');
const timeTo = document.getElementById('timeTo');
const dateFrom = document.getElementById('dateFrom');
const dateTo = document.getElementById('dateTo');
const formFilter = document.getElementById('formFilter');
const roomsTable = document.getElementById('roomsTable');
const roomsList = document.getElementById('roomsList');
const downloadButton = document.getElementById('downloadButton');

var correspondingDayTable = {"lundi":"01-lundi","mardi":"02-mardi","mercredi":"03-mercredi","jeudi":"04-jeudi","vendredi":"05-vendredi","samedi":"06-samedi","dimanche":"07-dimanche"};
var correspondingLessonTable = {0:"C1_8h-9h30",1:"C2_9h45-11h15",2:"C3_11h30-13h",3:"C4_13h00-14h30",4:"C5_14h45-16h15",5:"C6_16h30-18h00",6:"C7_18h15-19h45"};
var mediumTreshold = 50/100;
var maximumTreshold = 70/100;
var planning = [];
var slot = [];
var days = [];
var numberRoomsSelected = 0;

listRoomsGroups.addEventListener("change", loadRooms);
deleteFilter.addEventListener("click", deleteFilterF);
formFilter.addEventListener("submit", checkFilter);
downloadButton.addEventListener("click", loadJson);

loadRoomsGroups();

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
    if(timeTo.value < timeFrom.value){
        alert("L'heure de départ ne peut pas être supérieur à l'heure final");
        return;
    }
    if(dateTo.value < dateFrom.value){
        alert("La date de départ ne peut pas être supérieur à la date final");
        return;
    }
    for (let i=0, row; row = roomsTable.rows[i]; i++) {
        for (let j=0, col; col = roomsTable.rows[i].cells[j]; j+=2) {
            if(col.firstChild.checked == true){
                checkCb = true;
                rooms.push(roomsTable.rows[i].cells[j+1].innerHTML);
            }
        }  
    }
    if(!checkCb){
        alert("Il faut sélectionner au moins une salle");
        return;
    }
    planning = [];
    slot = [];
    days = [];
    numberRoomsSelected = rooms.length;
    loadRoomsFilter(timeFrom.value, timeTo.value, dateFrom.value, dateTo.value, rooms);
    downloadButton.style.display = "initial";
}

function loadRoomsFilter(timeStart, timeStop, dateStart, dateStop, rooms){
    getRoomsSchedule(timeStart, timeStop, dateStart, dateStop, rooms);
}

function deleteFilterF(){
    listRoomsGroups.value = "";
    listRoomsGroups.dispatchEvent(new Event('change'));
    timeFrom.value = "";
    timeTo.value = "";
    dateFrom.value = "";
    dateTo.value = "";
}

function showRooms(e){
    roomsList.innerHTML = "";
    roomsList.parentNode.children[0].style.display = "initial";
    let planningCase = planning[e.target.parentNode.parentNode.rowIndex-1][e.target.parentNode.cellIndex-1];
    for(let i = 0; i < planningCase.length; i++){
        let li = document.createElement('li');
        li.textContent = planningCase[i];
        roomsList.appendChild(li);
    }
}

function loadJson(){
    let json = {};
    for(let i = 0; i < days.length; i++){
        if(!json.hasOwnProperty(days[i].getWeek())){
            let daysTemp = {};
            for(let j = 0; j < 7; j++){
                let slotTemp = {};
                for(let z = 0; z < 7; z++){
                    slotTemp[Object.values(correspondingLessonTable)[z]] = 0;
                }
                daysTemp[Object.values(correspondingDayTable)[j]] = slotTemp;
            }
            json[days[i].getWeek()] = daysTemp;
        }
    }
    for(let i = 0; i < days.length; i++){
        let day = days[i].toLocaleDateString("fr-FR", { weekday: 'long' })
        for(let j = 0; j < slot.length; j++){
            json[days[i].getWeek()][correspondingDayTable[day]][slot[j]] = planning[j][i].length;
        }
    }
    let dayStart = days[0].getDate()+"-"+(days[0].getMonth()+1)+"-"+days[0].getFullYear();
    let dayEnd = days[days.length-1].getDate()+"-"+(days[days.length-1].getMonth()+1)+"-"+days[days.length-1].getFullYear();
    let title = "json/JSON_number_excel_"+dayStart+"_"+dayEnd+".json";
    createJSONFile(json, title, dayStart, dayEnd);
}