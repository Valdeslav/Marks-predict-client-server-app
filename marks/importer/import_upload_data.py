from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd

from groups_app.models import Group
from marks.models import Student, Subject, Mark
from .exceptions import UnsupportedFileTypeException

supported_files = {'.csv': ',', '.tsv': '\t', '.psv': '|', '.ssv': ';'}
FILE_DIRECTORY_PREFIX = 'marks/importer/files/'
FIO = 'ФИО'


def import_data_from_file(data_file: InMemoryUploadedFile, group_id):
    file_extention = save_getting_file(data_file)
    file_data = pd.read_csv(
        f'{FILE_DIRECTORY_PREFIX}{data_file.name}',
        supported_files[file_extention]
    )
    parse_into_db(file_data, group_id)


def save_getting_file(data_file: InMemoryUploadedFile):
    file_name = data_file.name
    file_extention = file_name[file_name.rfind('.'):]
    try:
        supported_files[file_extention]
    except KeyError:
        raise UnsupportedFileTypeException(file_extention)
    with open(f'{FILE_DIRECTORY_PREFIX}{file_name}', 'wb') as dest:
        for chunk in data_file.chunks():
            dest.write(chunk)
    return file_extention


def parse_into_db(file_data: pd.DataFrame, group_id):
    fio = file_data.get(FIO)
    file_data.drop(FIO, axis=1, inplace=True)
    file_subjects = []
    # parse subject
    for subject_name in file_data:
        subject = Subject.objects.filter(name=subject_name)
        if not subject:
            subject = Subject(name=subject_name, semester=0)
            subject.save()
        else:
            subject = subject[0]

    # add subject to speciality
        subject_specialities = subject.specialities.all()
        group = Group.objects.get(pk=group_id)
        if group.speciality not in subject_specialities:
            subject.specialities.add(group.speciality)

        file_subjects.append(subject)

    # parse students and marks
    student_row = 0
    for student_name in fio:
        student = Student.objects.filter(fullname=student_name, group=group)
        if not student:
            student = Student(fullname=student_name, group=group)
            student.save()
        else:
            student = student[0]

        subject_index = 0
        for file_mark in file_data.iloc[student_row]:
            mark = Mark.objects.filter(student=student, subject=file_subjects[subject_index])
            if not mark:
                try:
                    Mark(student=student, subject=file_subjects[subject_index], mark=file_mark).save()
                except ValueError:
                    pass
            else:
                mark = mark[0]
                mark.mark = file_mark
                mark.save()
            subject_index += 1

        student_row += 1


    return None
