import pandas as pd
from simpletransformers.classification import ClassificationModel


train_df = pd.read_csv('data/train.csv', header=None)
train_df['text'] = train_df.iloc[:, 1] + " " + train_df.iloc[:, 2]
train_df = train_df.drop(train_df.columns[[1, 2]], axis=1)
train_df.columns = ['label', 'text']
train_df = train_df[['text', 'label']]
train_df['text'] = train_df['text'].apply(lambda x: x.replace('\\', ' '))
train_df['label'] = train_df['label'].apply(lambda x:x-1)

eval_df = pd.read_csv('data/test.csv', header=None)
eval_df['text'] = eval_df.iloc[:, 1] + " " + eval_df.iloc[:, 2]
eval_df = eval_df.drop(eval_df.columns[[1, 2]], axis=1)
eval_df.columns = ['label', 'text']
eval_df = eval_df[['text', 'label']]
eval_df['text'] = eval_df['text'].apply(lambda x: x.replace('\\', ' '))
eval_df['label'] = eval_df['label'].apply(lambda x:x-1)


# Create a ClassificationModel
model = ClassificationModel('roberta', 'roberta-base', num_labels=4, use_cuda=True, cuda_device=0)
# Train the model
model.train_model(train_df)

from sklearn.metrics import f1_score, accuracy_score


def f1_multiclass(labels, preds):
    return f1_score(labels, preds, average='micro')

result, model_outputs, wrong_predictions = model.eval_model(eval_df, f1=f1_multiclass, acc=accuracy_score)


predictions, raw_outputs = model.predict(['Some arbitary sentence'])
print(f'Prediction is {predictions}')