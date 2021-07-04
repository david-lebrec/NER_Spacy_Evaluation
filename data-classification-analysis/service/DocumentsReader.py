from typing import AnyStr

import pandas as pd
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
                'B-PER\n': 'PERSON\n',
                'B-LOC\n': 'LOC\n',
                'B-ORG\n': 'ORG\n',
                'B-MISC\n': 'NORP\n',
            }
        self.my_counts = {
            'PERSON\n': 0,
            'LOC\n': 0,
            'ORG\n': 0,
            'NORP\n': 0
        }
        self.my_entities_count = 0

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
                    #last_char = sample_str[length - 1]
                    #print('Last character : ', last_char)
                    if sample_str[-1] == '\n':
                        if entity != 'O\n':
                            self.my_entities_count += 1
                        if file_name == SPACY_FILE_NAME:
                            # spacy a bien classifie avec une sous classe
                            if entity == 'GPE\n':
                                entity = 'LOC\n'
                            self.my_counts[entity] += 1
                        else:
                            if entity in self.entity_matrix.keys():
                                converted_entity = self.entity_matrix[entity]
                                self.my_counts[converted_entity] += 1

                        if entity not in self.available_entities and not entity.isdigit():
                            #and sample_str[-1] == "'n'":
                            #entity = entity.replace(NEW_LINE, '')
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

    def compute_and_print_ratios(self, reference) -> None:
        print('ratios')
        result: dict = {}
        global_ratio = 0
        for key in self.my_counts:
            my_value = self.my_counts[key]
            ref_value = reference.my_counts[key]
            ratio_numeric_value = round((my_value / ref_value), 2)*100
            ratio = f'{ratio_numeric_value}%'
            result.update({key: ratio})
            global_ratio += ratio_numeric_value
        global_ratio /= len(result)

        print('my ratios against reference')
        print(result)

        print('classification ratio against reference > 100 better than reference < 100 baddest than reference')
        ratio_count_entities_numeric_value = round((self.my_entities_count / reference.my_entities_count) * 100, 2)
        ratio_count_entities = f'{ratio_count_entities_numeric_value}%'
        print(ratio_count_entities)

        print('my global ratio against reference')
        print(f'{global_ratio}%')