class GSheets:

    def __init__(self, service, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.service = service

    def load_values(self, range, major_dimension='ROWS', start_with=0):
        document = self.service.spreadsheets().values()\
            .get(spreadsheetId=self.spreadsheet_id,
                 range=range,
                 majorDimension=major_dimension,
                 valueRenderOption='FORMATTED_VALUE')\
            .execute()
        new_doc = document.get('values')
        return new_doc[0][start_with:] if len(new_doc) == 1 else document.get('values')[start_with:]