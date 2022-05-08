from .data_handling import NeuralDataLoader

from marks.models import Student
from predictApp.neural_network.neural_network import NeuralNetworkPredictor


def predict_marks(group_id, student_ids, subject_ids):
    dataloader = NeuralDataLoader()
    dataloader.select_predict_data(group_id, student_ids, subject_ids)
    dataloader.prepare_train_all_subj_marks()
    predictor = NeuralNetworkPredictor()
    predictions = []

    while dataloader.has_data_to_predict():
        train_all_subj_scores, train_targ_subj_scores = dataloader.prepare_train_data()
        test_all_subj_scores = dataloader.prepare_test_data()
        predictor.create_model(train_all_subj_scores, train_targ_subj_scores)
        pred = predictor.predict(test_all_subj_scores)
        predictions.append(pred)

    rev_predictions = [[0 for i in range(len(predictions))] for j in range(len(predictions[0]))]
    for i in range(len(predictions)):
        for j in range(len(predictions[0])):
            rev_predictions[j][i] = predictions[i][j]

    students = Student.objects.filter(pk__in=student_ids).order_by('pk')
    predictions = []
    for i in range(len(rev_predictions)):
        prediction = Prediction(students[i], rev_predictions[i])
        predictions.append(prediction)

    return predictions


class Prediction:
    def __init__(self, student, marks):
        self.student = student
        self.marks = marks
