#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import gspread
from gspread import Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials



FEEDS = 'https://spreadsheets.google.com/feeds'
DRIVE = 'https://www.googleapis.com/auth/drive'
SCOPES = 'https://www.googleapis.com/auth/realtime-bidding'


class GoogleSheetsApiClient:
    def __init__(self, filename: str):
        self.scope = [FEEDS, DRIVE]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            filename=filename,
            scopes=self.scope,
        )
        self.client = gspread.authorize(self.creds)

    async def get_tables(self) -> list[Spreadsheet]:
        return self.client.openall()

    async def get_table_by_name(self, name) -> Spreadsheet:
        tables = await self.get_tables()
        for table in tables:
            if table.title == name:
                return table
        raise Exception('Required table not found')

    @staticmethod
    async def get_sheets(table: Spreadsheet) -> list[str]:
        return [sheet.title for sheet in table.worksheets()]

    @staticmethod
    async def get_columns_by_name(column_name, worksheet: Worksheet):
        column_index = worksheet.row_values(1).index(column_name) + 1
        return worksheet.col_values(column_index)

    @staticmethod
    async def get_rows(sheet: Worksheet):
        data = sheet.get_all_values()
        return data


google_sheets_api_client = GoogleSheetsApiClient(
    filename='google_creds.json',
)
