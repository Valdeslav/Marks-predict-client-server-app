'''module for reading from db and handling training and test data'''
from abc import ABC, abstractmethod

import numpy as np

from marks.models import Student, Speciality, Mark, Subject
from groups_app.models import Faculty
from prediction.predictor_module.exceptions import EmptyListOfSubjectsWithMark


class DataLoader(ABC):
    '''reading and handling data'''

    def __init__(self, student_ids, subject_ids):
        self.target_students_ids = student_ids
        self.target_subjects_ids = subject_ids
        self.subjects_with_marks_ids = None
        self.student_have_marks_ids = None

        self.train_all_subj_marks = None
        self.predicted_count = 0

    def has_data_to_predict(self):
        return self.predicted_count != len(self.target_subjects_ids)

    @staticmethod
    def get_students_with_marks(subject_id):
        students_have_mark = Student.objects.filter(
            mark__subject_id=subject_id).distinct('pk')

        return [i.pk for i in students_have_mark]

    @staticmethod
    def get_subjects_with_marks(students_ids):
        common_subjects = list(Subject.objects.filter(mark__student_id=students_ids.pop(0)).distinct('pk'))

        for stud_id in students_ids:
            subjects = Subject.objects.filter(mark__student_id=stud_id).distinct('pk')
            subjects_to_remove = []
            for sbj in common_subjects:
                if sbj not in subjects:
                    subjects_to_remove.append(sbj)

            for sbj in subjects_to_remove:
                common_subjects.remove(sbj)

        return [i.pk for i in common_subjects]

    @abstractmethod
    def prepare_prediction_data(self):
        pass


class NeuralDataLoader(DataLoader):
    def prepare_train_all_subj_marks(self):
        train_all_subj_marks = []
        for st_id in self.student_have_marks_ids:
            marks = Mark.objects.filter(student_id=st_id, subject_id__in=self.subjects_with_marks_ids).order_by('pk').values('mark')
            train_all_subj_marks.append([i['mark'] for i in marks])
        self.train_all_subj_marks = np.array(train_all_subj_marks)

    def prepare_test_data(self):
        test_all_subj_marks = []
        for st_id in self.target_students_ids:
            marks = Mark.objects.filter(student_id=st_id, subject_id__in=self.subjects_with_marks_ids).order_by('pk').values('mark')
            test_all_subj_marks.append([i['mark'] for i in marks])
        return np.array(test_all_subj_marks)

    def prepare_prediction_data(self):
        train_targ_subj_marks = []
        targ_subject_id = self.target_subjects_ids[self.predicted_count]

        self.student_have_marks_ids = self.get_students_with_marks(targ_subject_id)
        self.subjects_with_marks_ids = self.get_subjects_with_marks(self.target_students_ids + self.student_have_marks_ids)

        if len(self.subjects_with_marks_ids)==0:
            raise EmptyListOfSubjectsWithMark()

        for st_id in self.student_have_marks_ids:
            mark = Mark.objects.filter(student_id=st_id, subject_id=targ_subject_id)[0]
            train_targ_subj_marks.append(mark.mark)
        train_targ_subj_marks = np.array(train_targ_subj_marks)
        self.predicted_count += 1

        self.prepare_train_all_subj_marks()

        return self.train_all_subj_marks, train_targ_subj_marks, self.prepare_test_data()
