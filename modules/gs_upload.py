# coding: utf-8
from __future__ import print_function

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GSUploader(object):
    _scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    def __init__(self, csv_recipes):
        self._creds = ServiceAccountCredentials.from_json_keyfile_name(".secret.json", self._scope)
        self._client = gspread.authorize(self._creds)
        self._worksheet = self._client.open("Team 4 Recipe Report")
        self._payload = csv_recipes

    def upload(self):
        try:
            self._client.import_csv(self._worksheet.id, data=self._payload)
        except UnicodeEncodeError:
            self._client.import_csv(self._worksheet.id, data=self._payload.encode("utf-8"))
