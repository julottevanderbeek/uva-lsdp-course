# this code is authored by by Hang Jiang
import numpy as np
import glob, os, sys
import re
import pickle

import keras
from keras.layers import Dropout
from keras.datasets import imdb
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D, Conv2D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.losses import categorical_crossentropy
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer
from keras.callbacks import ModelCheckpoint
from keras.callbacks import History 
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix
from personalities.attention import AttLayer
import numpy
import pandas as pd 
from collections import Counter
import personalities.models as models
import fasttext
from nltk.corpus import stopwords
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import hamming_loss

class Preprocessing:

    # handle attributes and attribute
    def preprocess(self, docs, labels, attribute):
        # delete '_' because I want name to be concatenated 
        t = Tokenizer(num_words = 20000, filters='!"#$%&()*+,-./:;<=>?@[\\]^`{|}~\t\n')
        t.fit_on_texts(docs)
        encoded_docs = t.texts_to_sequences(docs)
        print("BEFORE Pruning:")
        self.get_statistics(encoded_docs, labels, attribute)
        idx2word = {v:k for k,v in t.word_index.items()}
        
        # stopwords 
        stopwrd = set(stopwords.words('english'))
        
        # handle abbreviation
        def abbreviation_handler(text):
            ln = text.lower()
            # case replacement
            ln = ln.replace(r"'t"," not")
            ln = ln.replace(r"'s"," is")
            ln = ln.replace(r"'ll"," will")
            ln = ln.replace(r"'ve"," have")
            ln = ln.replace(r"'re"," are")
            ln = ln.replace(r"'m"," am")

            # delete single '
            ln = ln.replace(r"'"," ")

            return ln
        
        # handle stopwords
        def stopwords_handler(text):
            words = text.split()
            new_words = [w for w in words if w not in stopwrd]
            return ' '.join(new_words)
                
        # get post-tokenized docs
        def sequence_to_text(listOfSequences):
            tokenized_list = []
            for text in listOfSequences:
                newText = ''
                for num in text:
                    newText += idx2word[num]+' '
                newText = abbreviation_handler(newText)
                newText = stopwords_handler(newText)
                tokenized_list.append(newText)
            return tokenized_list
        
        newLists = sequence_to_text(encoded_docs)
        
        return newLists

    # handle single and multiple attributes
    def get_statistics(self, encoded_docs, Ys, attributes):

        # explore encoded docs: find sequence length distribution
        result = [len(x) for x in encoded_docs]
        print("Min=%d, Mean=%d, Max=%d" % (numpy.min(result),numpy.mean(result),numpy.max(result)))
        data_max_seq_length = numpy.max(result)+1

        # explore Y for each attribute
        if type(attributes) == list:
            for idx, attribute in enumerate(attributes):
                Y = Ys[ : , idx]
                self.get_single_statistics(Y, attribute)
        elif type(attributes) == str:
            self.get_single_statistics(Ys, attributes)

        return data_max_seq_length

    # get statistics of a single attribute
    def get_single_statistics(self, Y, attribute):

        # find majority distribution
        ct = Counter(Y)
        majorityDistribution = max([ct[k]*100/float(Y.shape[0]) for k in ct])
        print("Total majority is {0} for {1}.".format(majorityDistribution, attribute))


    def load_data(self, attribute):

        # read the data 
        df = pd.read_csv(config.FILENAME)

        print("The size of data is {0}".format(df.shape[0]))
        docs = df[config.column_to_read].astype(str).values.tolist()
        labels = df[attribute].values # attribute is either string or a list of strings
        # preprocess data before feeding into tokenizer
        docs = self.preprocess(docs, labels, attribute)

        # tokenize the data 
        t = Tokenizer(num_words = config.MAX_NUM_WORDS)
        t.fit_on_texts(docs)
        encoded_docs = t.texts_to_sequences(docs)
        print("Real Vocab Size: %d" % (len(t.word_index)+1))
        print("Truncated Vocab Size: %d" % config.MAX_NUM_WORDS)
        self.word_index = t.word_index

        # perform Bag of Words
        print("AFTER Pruning:")
        data_max_seq_length = self.get_statistics(encoded_docs, labels, attribute) # can be used to replace MAX_SEQ_LENGTH
        self.X = sequence.pad_sequences(encoded_docs, maxlen=config.MAX_SEQ_LENGTH) # use either a fixed max-length or the real max-length from data
        
        # for use with categorical_crossentropy
        self.Y = labels
        if config.multilabel:
            self.onehot_Y = self.Y
        else:
            self.onehot_Y = keras.utils.to_categorical(labels, config.ClassNum)

        self.attribute = attribute if type(attribute) == str else 'all_attributes' # self.attribute is always a string
    

    def load_fasttext(self, use_word_embedding):

        # if not use it, 
        if not use_word_embedding:
            self.embedding_matrix = []
            self.EMBEDDING_DIM = 100
            return 

        # if exists
        if os.path.exists("fastMatrix.pkl"):
            print("FastText Embedding EXISTS!")
            with open("fastMatrix.pkl", 'rb') as f:
                embedding_matrix = pickle.load(f)
            self.embedding_matrix = embedding_matrix
            self.EMBEDDING_DIM = len(embedding_matrix[0])
            return 

        # read the fastText Embedding
        count_oov = 0
        fastModel = fasttext.load_model(config.PATH_EMBEDDING)

        # create a weight matrix for words in training docs
        embedding_matrix = np.zeros((config.MAX_NUM_WORDS, config.EMBEDDING_DIM))
        word2idx = {k:v for k,v in self.word_index.items() if v < config.MAX_NUM_WORDS} # ??? explore word_index, how to eliminate stop words directly from it if it ranks words in frequency
        for word, i in word2idx.items():
            embedding_matrix[i] = fastModel[word] # a vector is giving oov words anyway
            if word not in fastModel.words:
                count_oov += 1
        print("Finished Vectorization.\n {} / {} Not in FastText Bin.".format(count_oov, config.MAX_NUM_WORDS))

        # update the variables
        self.embedding_matrix = embedding_matrix
        self.EMBEDDING_DIM = config.EMBEDDING_DIM

        # dump the matrix 
        with open("fastMatrix.pkl", "wb") as f:
            pickle.dump(embedding_matrix, f)
            
        return

    # generater, returns indices for train and test data  
    def cross_validation(self, X, Y, seed):
        kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
        kfolds = kfold.split(self.X, self.Y)
        return kfolds

# need to update its attribute handling 
def train_cross_validation(attribute, ModelName):

    # preprocess set up
    preprocessObj = Preprocessing()
    paramsObj = config.Params()
    preprocessObj.load_data(attribute)
    preprocessObj.load_fasttext(paramsObj.use_word_embedding)

    # set seed and cross validation (??? the value of seed)
    seed = 7
    numpy.random.seed(seed)
    kfolds = preprocessObj.cross_validation(preprocessObj.X, preprocessObj.onehot_Y, seed)
    cv_acc = []
    cv_records = []
    count_iter = 1

    prev_best = 0

    # loop the kfolds
    for train, test in kfolds:

        # create objects for each fold of 10-fold CV
        modelObj = models.DeepModel()

        # build the model
        model = modelObj.chooseModel(config.ModelName, paramsObj=paramsObj, weight=preprocessObj.embedding_matrix)
        # print(model.summary())

        # save the best model & history
        filepath = f"models/{attribute}_cur.h5"
        checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=0, save_best_only=True, mode='max')
        history = History()
        callbacks_list = [history, checkpoint]

        # fit the model
        model.fit(preprocessObj.X[train], preprocessObj.onehot_Y[train], 
                validation_data = (preprocessObj.X[test], preprocessObj.onehot_Y[test]),
                epochs=paramsObj.n_epoch, 
                batch_size=paramsObj.batch_size, 
                verbose=0, 
                callbacks=callbacks_list)

        # record
        ct = Counter(preprocessObj.Y)
        print("working on =={}==".format(attribute))
        print("----%s: %d----" % (preprocessObj.attribute, count_iter))
        print("----highest evaluation accuracy is %f" % (100*max(history.history['val_accuracy'])))
        print("----dominant distribution in data is %f" % max([ct[k]*100/float(preprocessObj.Y.shape[0]) for k in ct]))
        cv_acc.append(max(history.history['val_accuracy']))
        cv_records.append(history.history['val_accuracy'])
        count_iter += 1

        if (100*max(history.history['val_accuracy'])) > prev_best:
            prev_best = (100*max(history.history['val_accuracy']))
            os.rename(filepath, f"models/{attribute}_best.h5")
            print(f"New best evaluation, saving model to models/{attribute}_best.h5")

    print("The 10-fold CV score is %s" % np.nanmean(cv_acc))
    
    return np.nanmean(cv_acc)

def train_persona(configuration):
    global config
    config = configuration

    # model 
    ModelName = config.ModelName

    cv_acc = 0

    # choose multiclass or multilabel
    if config.multilabel:
        dim = config.dims
        cv_acc = train_cross_validation(dim, ModelName)
    else:
        dims = config.dims
        for dim in dims:
            cv_acc += train_cross_validation(dim, ModelName)
        cv_acc /= len(dims)
    
    return cv_acc