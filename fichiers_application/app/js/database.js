var ajax = new XMLHttpRequest();

function getUsers(){
    $.ajax({
        type: "POST",
        url: "/getUsers",
        success: function(result){
            listUsers(result);
            addMail(result);
        }
    })
}

function listUsers(result){
    for(let i = 0; i < result.length; i++){
        users.push(result[i]);
    }
}

function setWhoContact(){
    for(let i = 0; i < users.length; i++){
        if (texte.value == users[i].mail){
            $.ajax({
                type: "POST",
                url: "/setWhoContact",
                data:{
                    id: users[i].id_user
                },
                success: function(result){
                    getWhoContact();
                }
            })
            return;
        }
    }
    alert("Incorrect");
}

function getWhoContact(){
    $.ajax({
        type: "POST",
        url: "/getWhoContact",
        success: function(result){
            let contact = document.getElementById("bodyContact");
            let rowsBody = contact.rows;
            while(rowsBody.length > 0){
                rowsBody[0].parentNode.removeChild(rowsBody[0]);
            }
            //let data = JSON.parse(result);
            for(let i = 0; i < result.length; i++){
                let tr = document.createElement("tr");
                let td = document.createElement("td");
                td.textContent = result[i].prenom_user + " " + result[i].nom_user;
                tr.appendChild(td);
                contact.appendChild(tr);                
            }
        }
    })
}

function getAdmin(){
    $.ajax({
        type: "POST",
        url: "/getAdmin",
        success: function(result){
            let contact = document.getElementById("bodyAdmin");
            //let data = JSON.parse(result);
            for(let i = 0; i < result.length; i++){
                let tr = document.createElement("tr");
                let td = document.createElement("td");
                td.textContent = result[i].prenom_user + " " + result[i].nom_user;
                tr.appendChild(td);
                contact.appendChild(tr);                
            }
        }
    })
}

function getRoomsGroups(option){
    if(option == 1){
        $.ajax({
            type: "POST",
            url: "/getRoomsGroups",
            success: function(result){
                let listRoomsGroups = document.getElementById("listRoomsGroups");
                listRoomsGroups.innerHTML = "<option value=''></option>";
                for(let i = 0; i < result.length; i++){
                    let opt = document.createElement('option');
                    opt.value = result[i].id_groupe;
                    opt.text = result[i].nom_groupe;
                    listRoomsGroups.append(opt);
                }
            }
        })
    }else if(option == 2){
        $.ajax({
            type: "POST",
            url: "/getRoomsGroups",
            success: function(result){
                let groupName = document.getElementById('groupeName').value;
                let check = false;
                for(let i = 0; i < result.length; i++){
                    if(groupName == result[i].nom_groupe){
                        check = true;
                        alert("Rentrez un nom de groupe qui n'existe pas déjà"); 
                    }
                }
                if(!check){
                    createNewGroup(groupName);
                }
            }
        })
    }else if(option == 3){
        $.ajax({
            type: "POST",
            url: "/getRoomsGroups",
            success: function(result){
                let listDeleteRoomsGroups = document.getElementById("listDeleteRoomsGroups");
                listDeleteRoomsGroups.innerHTML = "<option value=''></option>";
                for(let i = 0; i < result.length; i++){
                    let opt = document.createElement('option');
                    opt.value = result[i].id_groupe;
                    opt.text = result[i].nom_groupe;
                    listDeleteRoomsGroups.append(opt);
                }
            }
        })
    }
}

function getRooms(idRoomGroup, option){
    if(option == 1){
        $.ajax({
            type: "POST",
            url: "/getRooms",
            data: { 
                id_groupe_salle: idRoomGroup,
                option: option
            },
            success: function(result){
                let tableRooms = document.getElementById("roomsTable");
                let rows = document.getElementById("roomsTable").rows;
                while(rows.length > 0){
                    rows[0].parentNode.removeChild(rows[0]);
                }
                for(let i = 0; i < result.length; i++){
                    let tr = document.createElement("tr");
                    let td1 = document.createElement("td");
                    let td2 = document.createElement("td");
                    let cb = document.createElement("input");
                    cb.type = "checkbox";
                    cb.value = result[i].id_salle;
                    td2.textContent = result[i].nom;
                    td1.appendChild(cb);
                    tr.appendChild(td1);
                    tr.appendChild(td2);
                    tableRooms.appendChild(tr);
                }
            }
        })
    }else if(option == 2){
        $.ajax({
            type: "POST",
            url: "/getRooms",
            data: { 
                id_groupe_salle: idRoomGroup,
                option: option
            },
            success: function(result){
                let listRooms = document.getElementById("listRooms");
                listRooms.innerHTML = "";
                if(idRoomGroup != ""){
                    for(let i = 0; i < result.length; i++){
                        let opt = document.createElement('option');
                        opt.value = result[i].id_salle;
                        opt.text = result[i].nom;
                        listRooms.append(opt);
                    }
                }
            }
        })
    }
}

function getRoomSpecificDay(rooms, date, result, lessonNumber, planningLine){
    let totalRoom = 0;
    let week = date.getWeek().toString();
    let day = date.toLocaleDateString("fr-FR", { weekday: 'long' });
    let roomsNotAvailable = [];
    for(let i = 0; i < rooms.length; i++){
        if(result[week][correspondingDayTable[day]][correspondingLessonTable[lessonNumber]].includes(rooms[i])){
            roomsNotAvailable.push(rooms[i]);
            totalRoom++;
        }
    }
    planningLine[planningLine.length] = roomsNotAvailable;
    return totalRoom;
}

Date.prototype.getWeek = function() {
    var date = new Date(this.getTime());
    date.setHours(0, 0, 0, 0);
    // Thursday in current week decides the year.
    date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
    // January 4 is always in week 1.
    var week1 = new Date(date.getFullYear(), 0, 4);
    // Adjust to Thursday in week 1 and count number of weeks from date to week1.
    return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
}

function getRoomsSchedule(timeStart, timeStop, dateStart, dateStop, rooms) {
    $.ajax({
        type: "POST",
        url: "/getRoomsSchedule",
        success: function(result) {
            buildTable(result, timeStart, timeStop, dateStart, dateStop, rooms);
        }
    })
}

function buildTable(result, timeStart, timeStop, dateStart, dateStop, rooms){
    let headTable = document.getElementById("headTable");
    let bodyTable = document.getElementById("bodyTable");
    let rowsHead = document.getElementById("headTable").childNodes;
    let rowsBody = document.getElementById("bodyTable").rows;
    while(rowsHead.length > 0){
        rowsHead[0].parentNode.removeChild(rowsHead[0]);
    }
    while(rowsBody.length > 0){
        rowsBody[0].parentNode.removeChild(rowsBody[0]);
    }
    let startDate = new Date(dateStart);
    let endDate = new Date(dateStop);
    let difference = endDate.getTime() - startDate.getTime();
    let daysCount = Math.ceil(difference / (1000 * 3600 * 24)) + 1;
    let thSchedule = document.createElement("th");
    thSchedule.textContent = "Horaire";
    headTable.appendChild(thSchedule);
    for(let i = 0; i < daysCount; i++)
    {
        let dateTemp = new Date();
        dateTemp.setMonth(startDate.getMonth());
        dateTemp.setDate(startDate.getDate() + i);
        let thHead = document.createElement('th');
        thHead.textContent = "" + dateTemp.toLocaleDateString("fr-FR", { weekday: 'long' }) + " " + dateTemp.getDate() + "/" + (dateTemp.getMonth()+1).toString();
        headTable.appendChild(thHead);
    }
    let lessonHours = [{start: '08:00', end: '09:30'},{start: '09:45', end: '11:15'},{start: '11:30', end: '13:00'},{start: '13:00', end: '14:30'},{start: '14:45', end: '16:15'},{start: '16:30', end: '18:00'},{start: '18:15', end: '19:45'}];
    let startTimeTemp = new Date('2020-01-01 ' + timeStart);
    let endTimeTemp = new Date('2020-01-01 ' + timeStop);
    let endTimeFound = false;
    let startTimeFound = false;
    let lessonCount = -1;
    let startLesson = 0;
    let endLesson = 0;
    while((!endTimeFound || !startTimeFound)){
        lessonCount++;
        let timeLessonEndTemp = new Date('2020-01-01 ' + lessonHours[lessonCount].end);
        let timeLessonStartTemp = new Date('2020-01-01 ' + lessonHours[lessonCount].start);
        if(startTimeTemp.getTime() < timeLessonEndTemp.getTime() && !startTimeFound){
            startLesson = lessonCount;
            startTimeFound = true;
        }
        if(endTimeTemp.getTime() < timeLessonEndTemp.getTime() && !endTimeFound){
            if(endTimeTemp.getTime() < timeLessonStartTemp.getTime()){
                endLesson = lessonCount - 1;
            }
            else{
                endLesson = lessonCount;
            }
            endTimeFound = true;
        }
        if(!endTimeFound && lessonCount == 6){
            endLesson = lessonCount;
            endTimeFound = true;
        }
        if(startTimeFound){
            slot[slot.length] = correspondingLessonTable[lessonCount];
        }
    }
    for(let i = startLesson; i < endLesson+1; i++){
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.textContent = lessonHours[i].start + " - " + lessonHours[i].end;
        tr.appendChild(td);
        let planningLine = [];
        for(let j = 0; j < daysCount; j++){
            let tdLesson = document.createElement('td');
            let buttonLesson = document.createElement('button');
            let dateTemp = new Date();
            dateTemp.setMonth(startDate.getMonth());
            dateTemp.setDate(startDate.getDate() + j);
            if(i == startLesson){
                days[days.length] = dateTemp;
            }
            buttonLesson.id = "caseRoom";
            buttonLesson.onclick = showRooms;
            let numberRooms = getRoomSpecificDay(rooms, dateTemp, result, i, planningLine);
            buttonLesson.textContent = numberRooms;
            if(numberRooms/rooms.length < mediumTreshold){
                buttonLesson.style.backgroundColor = 'green';
            }
            else if(numberRooms/rooms.length < maximumTreshold){
                buttonLesson.style.backgroundColor = 'orange';
            }
            else{
                buttonLesson.style.backgroundColor = 'red';
            }
            tdLesson.appendChild(buttonLesson);
            tr.appendChild(tdLesson);
        }
        planning[planning.length] = planningLine;
        bodyTable.appendChild(tr);
    }
}

function createJSONFile(json, title, dayStart, dayEnd){
    $.ajax({
        type: "POST",
        url: "/createJSON",
        data: { 
            data: JSON.stringify(json), 
            title: title,
            dayStart: dayStart,
            dayEnd: dayEnd
        },
        success: function(result) {
            makeExcel(result[0], result[1]);
        }
    })
}

function makeExcel(dayStart, dayEnd) {
    $.ajax({
        type: "POST",
        url: "/makeExcel",
        data: {
            dayStart: dayStart,
            dayEnd: dayEnd,
            maximumTreshold: maximumTreshold,
            mediumTreshold: mediumTreshold,
            numberRooms: numberRoomsSelected
        },
        success:function(result) {
            console.log(result);
        }
    })
}

function createNewGroup(name){
    $.ajax({
        type: "POST",
        url: "/createGroup",
        data: {
            name: name
        },
        success:function(result) {
            console.log(result);
            loadRoomsGroups();
        }
    })
}

function insertRoomInGroup(group, room){
    $.ajax({
        type: "POST",
        url: "/addRoomToGroup",
        data:{
            group: group,
            room: room
        },
        success: function(result){
            console.log(result);
        }
    })
}

function deleteGroupDB(id){
    $.ajax({
        type: "POST",
        url: "/deleteGroup",
        data:{
            id_groupe: id
        },
        success: function(result){
            loadRoomsGroups();
            let listRoomsGroups = document.getElementById("listRoomsGroups");
            listRoomsGroups.value = "";
            listRoomsGroups.dispatchEvent(new Event('change'));
        }
    })
}

function forceParseDB() {
    $.ajax({
        type: "POST",
        url: "/forceParse",
        success:function(result) {
            console.log(result);
        }
    })
}


function updateRoleDB(mail, role){
    /*for(let i = 0; i < users.length; i++){
        if (textMail.value == users[i].mail){*/
            $.ajax({
                type: "POST",
                url: "/updateRole",
                data:{
                    mail:mail,
                    //id: users[i].id_user,
                    role: role
                },
                success:function(result) {
                    console.log(result);
                }
            })
            /*return;
        }
    }*/
}

function getSession(){
    $.ajax({
        type: "POST",
        url: "/session",
        success:function(result) {
            let mail = document.getElementById("mail");
            let administration = document.getElementById("administration");
            let user = document.getElementById("user");
            user.children[0].textContent = result['prenom_user'] + " " + result['nom_user'] + " : " + result['role'] ;
            user.style.display= "initial";
            if(result['role'] == "administrateur"){
                administration.style.display = "initial";
                mail.style.display = "initial";
            }else if (result['role'] == "superviseur"){
                mail.style.display = "initial";
            }
        }
    })
}

function updateTaux(tauxAlerte, nom){
    $.ajax({
        type: "POST",
        url: "/insertTaux",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        data:{
            tauxAlerte: tauxAlerte,
            nom: nom
        },
        success:function(result) {
            console.log(result);
        }
    })
}


