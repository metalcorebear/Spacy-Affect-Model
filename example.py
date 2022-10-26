#!/usr/bin/env python
"""
@author: metalcorebear
"""

# Model use example
# Function to build affect dictionary

import spacy
from collections import Counter

# Load affect model path
nlp_affect = spacy.load('affect_ner')

def measure_affect_score(sentence : str, nlp_affect):
    affect_percent = {'fear': 0.0, 'anger': 0.0, 'anticipation': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0,
                      'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
    emotions = []
    doc = nlp_affect(sentence)
    if len(doc.ents) != 0:
        for ent in doc.ents:
            emotions.append(ent.label_.lower())
        affect_counts = Counter()
        for emotion in emotions:
            affect_counts[emotion] += 1
        sum_values = sum(affect_counts.values())
        for key in affect_counts.keys():
            affect_percent.update({key: float(affect_counts[key]) / float(sum_values)})
    return affect_percent