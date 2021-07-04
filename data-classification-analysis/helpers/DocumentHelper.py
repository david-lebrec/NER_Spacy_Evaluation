from config.conf import OPEN_PARENTHESIS, END_PARENTHESIS, COMMA, DOT, SLASH, QUOTE, NEW_LINE, EMPTY, LINE_START, \
    LINE_END, DOCUMENT_START


class DocumentsHelper:

    def remove_last_char(self, value: str) -> str:
        return value.rstrip(self.get_last_char(value))

    def get_last_char(self, value: str) -> str:
        if len(value) > 0:
            return value[-1]
        return ''

    def is_parenthesis(self, value: str) -> bool:
        return value == OPEN_PARENTHESIS or value == END_PARENTHESIS

    def is_special_char_without_left_space(self, value: str) -> bool:
        return value == COMMA or value == DOT or value == SLASH or value == QUOTE or value == END_PARENTHESIS

    def is_special_char_without_right_space(self, value: str) -> bool:
        return value == OPEN_PARENTHESIS or value == SLASH

    def clean_string(self, value: str) -> str:
        return value.replace(NEW_LINE, EMPTY).replace('\'', "'")

    def is_string_start_line(self, line: str) -> bool:
        return line.__contains__(LINE_START)

    def is_string_end_line(self, line: str) -> bool:
        return line.__contains__(LINE_END)

    def is_string_not_start_or_end_line(self, line: str) -> bool:
        return not (self.is_string_start_line(line) or self.is_string_end_line(line))

    def is_string_not_document_start(self, line: str) -> bool:
        return not line.__contains__(DOCUMENT_START)

    def is_string_not_empty_or_none(self, value: str) -> bool:
       return not (value is None or value == '')

    def is_valid_token(self, line: str) -> bool:
        return self.is_string_not_empty_or_none(line) and self.is_string_not_document_start(line) and self.is_string_not_start_or_end_line(line)

    def is_documents_property_empty(self, documents: list) -> bool:
        return self.get_documents_size(documents) == 0

    def get_documents_size(self, documents: list) -> int:
        return len(documents)