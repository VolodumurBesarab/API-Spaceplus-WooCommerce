from modules.Excel.excel_hendler import ExcelHandler


class CreateAdverts:
    def __init__(self):
        self.excel_handler = ExcelHandler()
        self.file_name = "sklad.xlsx"

    def create_advert(self):
        file_content = self.excel_handler.get_exel_file(self.file_name)
        self.excel_handler.create_file_on_data(file_content=file_content, file_name=self.file_name)


create_adverts = CreateAdverts()
create_adverts.create_advert()
