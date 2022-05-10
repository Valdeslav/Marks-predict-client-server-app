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