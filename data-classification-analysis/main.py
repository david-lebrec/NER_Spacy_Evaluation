import spacy

from config.conf import TEST_FILE_NAME, SPACY_FILE_NAME
from service.DocumentsReader import DocumentsReader

if __name__ == "__main__":
    print('test.txt')
    file_reader = DocumentsReader()
    file_reader.load_documents(TEST_FILE_NAME)
    #file_reader.print_documents()
    #file_reader.print_available_entities()
    file_reader.print_my_counts()

    print('spacy.txt')
    file_reader_spacy = DocumentsReader()
    file_reader_spacy.load_documents(SPACY_FILE_NAME)
    file_reader_spacy.print_my_counts()
    #file_reader.print_documents()
    #file_reader_spacy.print_available_entities()

    file_reader_spacy.compute_and_print_ratios(file_reader)

    #nlp = spacy.load("en_core_web_sm")
    #for document in file_reader.documents:
        #doc = nlp(document)
        #print(document)

        #    for token in doc.ents:
    #        print(token.text, token.start_char, token.end_char, token.label_)