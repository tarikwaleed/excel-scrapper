import csv
import random
from rest_framework.views import APIView
from rest_framework.response import Response


class TopClientsView(APIView):
    def get(self, request, *args, **kwargs):
        csv_file_path = '/home/tarik/repos/excel-scrapper/app/resources/generated/clients_sales/.com.google.Chrome.tCq8Re'

        clients = []

        with open(csv_file_path, encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            _ = next(csv_reader)  
            _ = next(csv_reader)  

            for row in csv_reader:
                client_name = row[2]
                total_value = float(row[9].replace('ر⁠.س', '').replace(',', ''))

                clients.append({
                    "id": client_name,
                    "label": client_name,
                    "value": total_value
                })

        top_clients = sorted(clients, key=lambda x: x["value"], reverse=True)[1:7]

        return Response(top_clients[1:])

class TopProductsView(APIView):
    def get(self, request, *args, **kwargs):
        csv_file_path = '/home/tarik/repos/excel-scrapper/app/resources/generated/products_profit/.com.google.Chrome.TOAtT4'

        products = []
        filter_type = request.GET.get('filter', 'top')  # Default to 'top' if no filter is provided

        with open(csv_file_path, encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            _ = next(csv_reader)  
            _ = next(csv_reader)

            for row in csv_reader:
                product_name = row[0]
                sales_value = int(row[2].replace('.', '')
                                  .replace('ر', '')
                                  .replace('س', '')
                                  .replace('\xa0', '')
                                  .replace('\u2060','')
                                  .replace(',', ''))
                
                products.append({
                    "id": product_name,
                    "label": product_name,
                    "value": sales_value,
                    "color": f"hsl({random.randint(0, 360)}, 70%, 50%)"
                })

        if filter_type == 'lowest':
            sorted_products = sorted(products, key=lambda x: x["value"])[:5]
            return Response(sorted_products)
        else:  # Default to top products
            sorted_products = sorted(products, key=lambda x: x["value"], reverse=True)[:6]
            return Response(sorted_products[1:])



class SimpleView(APIView):
    def get(self, request, *args, **kwargs):
        # Path to the CSV file
        csv_file_path = '/home/tarik/repos/excel-scrapper/app/resources/generated/products_profit/.com.google.Chrome.TOAtT4'

        # Initialize an empty list to hold the rows
        data = []

        # Open the CSV file and read its content
        with open(csv_file_path, encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            _=next(csvfile)
            _=next(csvfile)

            for row in csv_reader:
                cleaned_row = {
                    "productName": row[0],
                    "salesQuantity": row[1],
                    "salesValue": row[2].replace('.','').replace('ر','').replace('س','').replace('\xa0', ''),
                    "returnQuantity": row[3],
                    "returnValue": row[4].split(' ')[0].replace('ر','').replace('س','').replace('\xa0', ''),
                    "netSalesQuantity": row[5],
                    "netSalesValue": row[6].split(' ')[0].replace('ر','').replace('س','').replace('\xa0', '').replace('.',''),
                    "totalCost": row[7].split(' ')[0].replace('ر','').replace('س','').replace('\xa0', '').replace('.',''),
                    "profitValue": row[8].split(' ')[0].replace('ر','').replace('س','').replace('\xa0', '').replace('.',''),
                    "profitPercentage": row[9],
                    "profitPercentageToSales": row[10],
                    "profitPercentageToCost": row[11],
                }
                data.append(cleaned_row)

        # Return the first row of the data as a JSON response
        return Response(data)
