from http import client
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import requests
import csv

class StatsView(APIView):
    def get(self, request, *args, **kwargs):
        clients_count=self._get_clients_count()
        invoices_count=self._get_invoices_count()
        total_profit=self._get_total_profit()
        products_count=self._get_products_count()
        return Response({"clients_count":clients_count,
                         "invoices_count":invoices_count,
                        "total_profit":total_profit,
                         "products_count":products_count,
                         },)
    def _get_clients_count(self):

        daftra_api_key = os.getenv("DAFTRA_API_KEY")
        url = f'{os.getenv("DAFTRA_API_BASE_URL")}/clients'

        headers = {
            "APIKEY": daftra_api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.get(url, headers=headers)
            return response.json().get('pagination').get('total_results')
        except Exception as e:
            raise e
    def _get_invoices_count(self):

        daftra_api_key = os.getenv("DAFTRA_API_KEY")
        url = f'{os.getenv("DAFTRA_API_BASE_URL")}/invoices'

        headers = {
            "APIKEY": daftra_api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.get(url, headers=headers)
            return response.json().get('pagination').get('total_results')
        except Exception as e:
            raise e

    def _get_total_profit(self):
        csv_file_path = '/home/tarik/repos/excel-scrapper/app/resources/generated/products_profit/.com.google.Chrome.TOAtT4'
        with open(csv_file_path, encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            a=list(csv_reader)[-1]
            total_profit=float(a[2].replace('ر', '').replace('س', '').replace('\xa0', '').replace('\u2060','').replace(',', '').replace('.', ''))
            return "{:,.2f}".format(total_profit / 100)

    def _get_products_count(self):
        
        csv_file_path = '/home/tarik/repos/excel-scrapper/app/resources/generated/low_inventory/.com.google.Chrome.9g5tvE'
        with open(csv_file_path, encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            a=list(csv_reader)
            return len(a)

