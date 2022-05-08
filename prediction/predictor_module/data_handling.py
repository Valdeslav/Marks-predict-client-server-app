'''module for reading from db and handling training and test data'''
from abc import ABC, abstractmethod

import numpy as np

from marks.models import Student, Speciality, Mark, Subject
from groups_app.models import Faculty


class DataLoader(ABC):
    '''reading and handling data'''

    def __init__(self):
        self.target_subjects_ids = None
        self.target_students_ids = None
        self.subjects_with_marks_ids = None
        self.student_have_marks_ids = None

        self.train_all_subj_marks = None
        self.predicted_count = 0

    def has_data_to_predict(self):
        return self.predicted_count != len(self.target_subjects_ids)

    def select_predict_data(self, group_id, student_ids, subject_ids):
        '''select needed data from db'''
        self.target_students_ids = student_ids
        self.target_subjects_ids = subject_ids
        self.student_have_marks_ids = DataLoader.get_students_with_marks(subject_ids)
        self.subjects_with_marks_ids = DataLoader.get_subjects_with_marks(student_ids + self.student_have_marks_ids)

    @staticmethod
    def get_students_with_marks(subject_ids):
        students_have_mark = Student.objects.filter(
            mark__subject_id__in=subject_ids).distinct('pk')

        students_have_all_marks = []
        for student in students_have_mark:
            graduated_subjects = Subject.objects.filter(mark__student=student).values('pk')
            graduated_subjects_ids = [sbj['pk'] for sbj in graduated_subjects]
            has_all_marks = True
            for sbj_id in subject_ids:
                if sbj_id not in graduated_subjects_ids:
                    has_all_marks = False
                    break
            if has_all_marks:
                students_have_all_marks.append(student)
        return [i.pk for i in students_have_all_marks]

    @staticmethod
    def get_subjects_with_marks(students_ids):
        common_subjects = Subject.objects.filter(mark__student_id=students_ids.pop(0)).distinct('pk')
        for stud_id in students_ids:
            subjects = Subject.objects.filter(mark__student_id=stud_id).distinct('pk')
            for sbj in common_subjects:
                if sbj not in subjects:
                    common_subjects.remove(sbj)
        return [i.pk for i in common_subjects]

    @abstractmethod
    def prepare_train_data(self):
        pass


class NeuralDataLoader(DataLoader):
    def prepare_train_all_subj_marks(self):
        train_all_subj_marks = []
        for st_id in self.student_have_marks_ids:
            marks = Mark.objects.filter(student_id=st_id, subject_id__in=self.subjects_with_marks_ids).order_by('pk').values('mark')
            train_all_subj_marks.append([i['mark'] for i in marks])
        self.train_all_subj_marks = np.array(train_all_subj_marks)

    def prepare_train_data(self):
        train_targ_subj_marks = []
        targ_subject_id = self.target_subjects_ids[self.predicted_count]
        for st_id in self.student_have_marks_ids:
            mark = Mark.objects.filter(student_id=st_id, subject_id=targ_subject_id)[0]
            train_targ_subj_marks.append(mark.mark)
        train_targ_subj_marks = np.array(train_targ_subj_marks)
        self.predicted_count += 1
        return self.train_all_subj_marks, train_targ_subj_marks

    def prepare_test_data(self):
        test_all_subj_marks = []
        for st_id in self.target_students_ids:
            marks = Mark.objects.filter(student_id=st_id, subject_id__in=self.subjects_with_marks_ids).order_by('pk').values('mark')
            test_all_subj_marks.append([i['mark'] for i in marks])
        return np.array(test_all_subj_marks)
