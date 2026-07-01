from excel_parser import WorkbookParser
from excel_writer import WorkbookWriter


class ExcelIO:

    @staticmethod
    def load(path=None):

        return WorkbookParser(path).load()

    @staticmethod
    def save(result):

        WorkbookWriter().save(result)
