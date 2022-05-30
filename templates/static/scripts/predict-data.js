window.onload = function (){
    setAllStudentCheckbox();
    setAllSubjectCheckbox();

    let studentCheckboxes = document.getElementsByName('student_id');
    let studentsAllCheckbox = document.getElementById('check_all_students');
    let subjectCheckboxes = document.getElementsByName('subject_id');
    let subjectAllCheckbox = document.getElementById('check_all_subjects');


    studentsAllCheckbox.onclick = handleAllCheckbox;
    studentCheckboxes.forEach(chbx => chbx.onclick = handleStCheckbox);
    subjectAllCheckbox.onclick = handleAllCheckbox;
    subjectCheckboxes.forEach(chbx => chbx.onclick = handleSbjCheckbox);
}

function setAllStudentCheckbox() {
    let studentCheckboxes = document.getElementsByName('student_id');
    let studentsAllCheckbox = document.getElementById('check_all_students');

    studentsAllCheckbox.checked = true;
    for (let i = 0; i < studentCheckboxes.length; i++) {
        if (!studentCheckboxes[i].checked){
            studentsAllCheckbox.checked = false;
            break;
        }
    }
}

function setAllSubjectCheckbox() {
    let subjectCheckboxes = document.getElementsByName('subject_id');
    let subjectAllCheckbox = document.getElementById('check_all_subjects');

    subjectAllCheckbox.checked = true;
    for (let i = 0; i < subjectCheckboxes.length; i++) {
        if (!subjectCheckboxes[i].checked){
            subjectAllCheckbox.checked = false;
            break;
        }
    }
}

function handleAllCheckbox(event) {
    let target = event.currentTarget;
    if (target.id === 'check_all_students'){
        let studentCheckboxes = document.getElementsByName('student_id');
        let val = target.checked;
        studentCheckboxes.forEach(chbx => chbx.checked=val);
    } else if(target.id === 'check_all_subjects') {
        let subjectCheckboxes = document.getElementsByName('subject_id');
        let val = target.checked;
        subjectCheckboxes.forEach(chbx => chbx.checked=val);
    }
}

function handleStCheckbox(event) {
    setAllStudentCheckbox();
}

function handleSbjCheckbox(event) {
    setAllSubjectCheckbox();
}

function createStudentsList() {
    let studentsCheckBoxes = document.getElementsByName("student_id");
    let students = "";
    for (let i=0; i<studentsCheckBoxes.length; i++){
        if (studentsCheckBoxes[i].checked) {
            students += studentsCheckBoxes[i].value + ",";
        }
    }
    students = students.substring(0, students.length - 1);
    let studentIdList = document.getElementById("student_id_list");
    studentIdList.value = students;

    let subjectsCheckBoxes = document.getElementsByName("subject_id");
    let subjects = "";
    for (let i=0; i<subjectsCheckBoxes.length; i++) {
        if (subjectsCheckBoxes[i].checked) {
            subjects += subjectsCheckBoxes[i].value + ",";
        }
    }
    subjects = subjects.substring(0, subjects.length - 1);
    let subjectIdList = document.getElementById("subject_id_list");
    subjectIdList.value = subjects;

    return true;
}
