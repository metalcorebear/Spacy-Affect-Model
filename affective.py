#!/usr/bin/env python
"""
@author: metalcorebear
"""

# Class to wrap the model.
# Default condition: model directory should live in present working directory.
# Measure sentiment of a larger body of text.  Return sentiment for each sentence.

from nltk.tokenize import sent_tokenize
from collections import Counter
import spacy

class Affective():
    '''
    The Affective class will measure emotional affect of text using the affect_ner Spacy model.
    
    Attributes:
    self.text (str) - loaded text.
    self.sentences (list) - list of tokenized sentences.
    self.affects (dict) - affect scores for each sentence.
    self.body_affects (dict) - overall affect scores for the entire text.
    self.affect_score (dict) - sum(positive_affects) - sum(negative_affects) for each sentence.
    self.body_affect_score (dict) - sum(positive_affects) - sum(negative_affects) for the overall body of text.
    self.model_path (str) - location of affect model (default is the current directory)
    self.model (object) - Spacy model.
    
    Methods:
    self.add_text(text : str) - loads text for analysis and tokenizes sentences.
    self.emote() - generates affect scores for each sentence and for the entire body of text
    '''
    def __init__(self, model_path = 'affect_ner'):
        self.text = None
        self.sentences = None
        self.affects = dict()
        self.body_affects = dict()
        self.affect_score = dict()
        self.body_affect_score = dict()
        self.model_path = model_path
        self.model = spacy.load(self.model_path)
        
    def add_text(self, text : str):
        '''
        Method to add text to the object instance.
        '''
        self.text = text.lower()
        self.sentences = sent_tokenize(self.text)
        
    def emote(self):
        '''
        Measure affect of individual sentences or the entire body of text.
        '''
        positive_affects = ['anticipation', 'trust', 'surprise', 'positive', 'joy']
        negative_affects = ['negative', 'sadness', 'disgust', 'fear', 'anger']
        # Build affect dict.
        for i in range(len(self.sentences)):
            affect_percent = {'fear': 0.0, 'anger': 0.0, 'anticipation': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0,
                      'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
            emotions = []
            sentence = self.sentences[i]
            doc = self.model(sentence)
            if len(doc.ents) != 0:
                for ent in doc.ents:
                    emotions.append(ent.label_.lower())
                affect_counts = Counter()
                for emotion in emotions:
                    affect_counts[emotion] += 1
                sum_values = sum(affect_counts.values())
                for key in affect_counts.keys():
                    affect_percent.update({key: float(affect_counts[key]) / float(sum_values)})
            self.affects.update({i:affect_percent})
            positive = [affect_percent[i] for i in positive_affects]
            negative = [affect_percent[i] for i in negative_affects]
            score = sum(positive) - sum(negative)
            self.affect_score.update({i:score})
            
        affect_percent = {'fear': 0.0, 'anger': 0.0, 'anticipation': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0,
                      'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
        emotions = []
        doc = self.model(self.text)
        if len(doc.ents) != 0:
            for ent in doc.ents:
                emotions.append(ent.label_.lower())
            affect_counts = Counter()
            for emotion in emotions:
                affect_counts[emotion] += 1
            sum_values = sum(affect_counts.values())
            for key in affect_counts.keys():
                affect_percent.update({key: float(affect_counts[key]) / float(sum_values)})
        self.body_affects.update({0:affect_percent})
        positive = [affect_percent[i] for i in positive_affects]
        negative = [affect_percent[i] for i in negative_affects]
        score = sum(positive) - sum(negative)
        self.body_affect_score.update({0:score})
