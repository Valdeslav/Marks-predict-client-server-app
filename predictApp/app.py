import data_handling
import prediction
from neural_network.neural_network import NeuralNetworkPredictor
from regr.regression import RegressionPrediction
from data_handling import NeuralDataLoader, RegrDataLoader


def app(predictor: prediction.Predictor, data_loader: data_handling.DataLoader, subj):
    data = data_loader.load_data_pd('data/marks.tsv')
    test_data = data_loader.load_data_pd('data/test.tsv')
    # names = test_data['ФИО']

    train_all_subj_scores, train_targ_subj_scores = data_loader.prepare_to_predict_subject(
        data, subj)
    test_all_subj_scores, test_targ_subj_scores = data_loader.prepare_to_predict_subject(
        test_data, subj)


    predictor.create_model(train_all_subj_scores, train_targ_subj_scores)
    pred = predictor.predict(test_all_subj_scores)
    print("прогноз - реальная оценка")
    for i in range(len(test_targ_subj_scores)):
        print(f'{pred[i]}: \t{test_targ_subj_scores[i]}')


def console_interface():
    predictors = {1: NeuralNetworkPredictor(), 2: RegressionPrediction()}
    data_loaders = {1: NeuralDataLoader(), 2: RegrDataLoader()}
    pred_id = None
    while 1:
        pred_id = input("С помощью чего сделать прогноз?\n"
                        "1 - нейросеть\n"
                        "2 - регрессия\n"
                        )
        if pred_id.strip() == "1" or pred_id == "2":
            break
    predictor = predictors[int(pred_id)]
    data_loader = data_loaders[int(pred_id)]
    while 1:
        subject = input("Предмет, для тестирования прогноза:\n"
                        "Базы данных,\tДГИ,\tМоиАПР,\tПЧМ,\n"
                        "Философия,\tАктуарная математика,\tНПО,\tООТПиСП,\n"
                        "ОсиСП,\tСГВМ,\tТРИС.\n")
        try:
            app(predictor, data_loader, subject)
        except KeyError:
            continue
        else:
            break

