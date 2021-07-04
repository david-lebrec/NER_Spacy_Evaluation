from typing import AnyStr

import pandas as pd
import spacy
from pandas import DataFrame

from config.conf import TEST_FILE_NAME, INDEX_WORD, SPACE, INDEX_ENTITY, NEW_LINE, SPACY_FILE_NAME
from helpers.DocumentHelper import DocumentsHelper


class DocumentsReader:
    """
        DocumentsReaders loads its documents property at start
    """

    def __init__(self):
        self.h = DocumentsHelper()
        self.documents = []
        self.available_entities = []
        self.entity_matrix = \
            {
                'B-PER\n': ['PERSON\n'],
                'B-LOC\n': ['LOC\n', 'GPE\n'],
                'B-ORG\n': ['ORG\n'],
                'B-MISC\n': ['NORP\n'],
            }
        self.spacy_matrix = \
            {
                'PERSON\n': 'PERSON\n',
                'LOC\n': 'LOC\n',
                'GPE\n': 'LOC\n',
                'ORG\n': 'ORG\n',
                'NORP\n': 'NORP\n',
            }
        self.my_counts = {
            'PERSON\n': 0,
            'LOC\n': 0,
            'ORG\n': 0,
            'NORP\n': 0
        }
        self.my_entities_count = 0
        self.my_counts_correct = {
            'PERSON\n': 0,
            'LOC\n': 0,
            'ORG\n': 0,
            'NORP\n': 0
        }
        self.nlp = spacy.load("en_core_web_sm")
        self.person_count = 0

    def load_documents(self, file_name: str) -> None:
        file = open(file_name, 'r')
        lines: [AnyStr] = file.readlines()

        current_document: str = ''
        for line in lines:
            if self.h.is_valid_token(line):
                split_line: [str] = line.split(SPACE)
                word: str = split_line[INDEX_WORD]
                try:
                    entity: str = split_line[INDEX_ENTITY]
                    sample_str = entity
                    length = len(entity)
                    # Get last character of string i.e. char at index position len -1
                    # last_char = sample_str[length - 1]
                    # print('Last character : ', last_char)

                    if sample_str[-1] == '\n':

                        if file_name == TEST_FILE_NAME:
                            doc = self.nlp(word)
                            # print(word)
                            tokens = doc.ents
                            if len(tokens) != 0:
                                if 'PERSON' in tokens[0].label_:
                                    self.person_count += 1
                                spacy_converted_entity = self.spacy_matrix[tokens[0].label_ + '\n']
                                self.my_counts_correct[spacy_converted_entity] += 1

                        if entity != 'O\n':
                            self.my_entities_count += 1
                        if file_name == SPACY_FILE_NAME:
                            # spacy a bien classifie avec une sous classe
                            spacy_converted_entity = self.spacy_matrix[entity]
                            self.my_counts[spacy_converted_entity] += 1
                        else:
                            if entity in self.entity_matrix.keys():
                                converted_entity = self.entity_matrix[entity][0]
                                self.my_counts[converted_entity] += 1

                        if entity not in self.available_entities and not entity.isdigit():
                            # and sample_str[-1] == "'n'":
                            # entity = entity.replace(NEW_LINE, '')
                            self.available_entities.append(entity)
                except Exception as e:
                    pass
                last_char: str = self.h.get_last_char(word)

                if self.h.is_special_char_without_left_space(last_char):
                    current_document = self.h.remove_last_char(current_document)

                current_document += word

                if not self.h.is_special_char_without_right_space(last_char):
                    current_document += SPACE

            if self.h.is_string_end_line(line):
                current_document = self.h.remove_last_char(current_document)
                current_document += '.'

            if not self.h.is_string_not_document_start(line):
                if self.h.is_string_not_empty_or_none(current_document):
                    current_document = self.h.clean_string(current_document)
                    self.documents.append(current_document)
                current_document = ''

    def print_documents(self) -> None:
        print('documents')
        print(self.documents)

    def print_available_entities(self) -> None:
        print('available_entities')
        print(self.available_entities)

    def print_my_counts(self) -> None:
        print('self.my_counts')
        print(self.my_counts)

    def print_my_counts_correct(self) -> None:
        print('self.my_counts_correct')
        print(self.my_counts_correct)

    def compute_and_print_ratios(self, reference) -> None:
        counts_spacy = {
            'LOC\n': 96 + 1418,
            'PERSON\n': 1298,
            'ORG\n': 979,
            'NORP\n': 384
        }

        my_counts = {
            'LOC\n': 1668,
            'PERSON\n': 1617,
            'ORG\n': 1661,
            'NORP\n': 702
        }
        # due to bug dirty fix by semi manual counting

        print('precision ratio')
        precision_result: dict = {}
        global_ratio_precision = 0

        for key in self.my_counts:
            my_value = self.my_counts_correct[key]
            ref_value = my_counts[key]
            ratio_numeric_value = round((my_value / ref_value) * 100, 2)
            ratio = ratio_numeric_value
            precision_result.update({key: ratio})
            global_ratio_precision += ratio_numeric_value
        global_ratio_precision /= len(precision_result)

        print('rappel')
        rappel_result: dict = {}
        global_ratio_rappel = 0

        for key in self.my_counts:
            my_value = counts_spacy[key]
            ref_value = my_counts[key]
            ratio_numeric_value = round((my_value / ref_value) * 100, 2)
            ratio = ratio_numeric_value
            rappel_result.update({key: ratio})
            global_ratio_rappel += ratio_numeric_value
        global_ratio_rappel /= len(rappel_result)

        print('spacy precision')
        print(precision_result)

        print('spacy rappel')
        print(rappel_result)

        print('spacy global precision')
        print(f'{global_ratio_precision}%')

        print('spacy global rappel')
        print(f'{global_ratio_rappel}%')

        f_score_for_each_entity = {}
        for key, value in precision_result.items():
            ratio_precision_each_entity = value
            ratio_rappel_each_entity = rappel_result[key]
            f_score_for_each_entity_numerator = (
                    2 * ((ratio_precision_each_entity / 100) * (ratio_rappel_each_entity / 100)))
            f_score_for_each_entity_denominator = (
                    (ratio_precision_each_entity / 100) + (ratio_rappel_each_entity / 100))
            f_score = round(f_score_for_each_entity_numerator / f_score_for_each_entity_denominator, 2)
            f_score_for_each_entity.update({key: f_score})

        print('F_Score for each entity')
        print(f_score_for_each_entity)

        print('F-score')
        f_score_numerator = (2 * ((global_ratio_precision / 100) * (global_ratio_rappel / 100)))
        f_score_denominator = ((global_ratio_precision / 100) + (global_ratio_rappel / 100))
        f_score = f_score_numerator / f_score_denominator
        print(round(f_score, 2))