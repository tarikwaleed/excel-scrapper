from django.core.management.base import BaseCommand
import logging
import inspect
import time
from shared.models import CommandException
import os
from scrapper.utils import Scrapper


class Command(BaseCommand):

    def handle(self, *args, **options):
        exception_count = 0
        start_time = time.time()

        logger = logging.getLogger(__name__)
        exceptions_logger = logging.getLogger("exceptions")

        logger.info(
            "----------------------------------------------------------------------------------------------------------------------------------------------------"
        )

        current_function_name = inspect.currentframe().f_code.co_name

        try:
            scraper = Scrapper(headless=True)
            products_profit_path=os.getenv('PRODUCTS_PROFIT')
            # if the download path does not exist create it
            scraper.download_file(
                'https://al-afaq20.daftra.com/owner/products/products_profit.xlsx?date_range_selector=lastmonth&sort=2&sort_order=desc',
                products_profit_path
            )

            # scraper.download_file(
            #     'https://example.com/path/to/file2.csv',
            #     '/path/to/download/location2'
            # )
        except Exception as e:
            exception_count += 1
            exceptions_logger.error(
                f"exception happened in Package:{__package__} Module:{__name__} Function:{current_function_name}(): {e}"
            )

        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Synced in {duration:.2f} seconds")
        if exception_count > 0:
            self.stdout.write(
                self.style.ERROR(
                    f"Synced with {exception_count} exceptions in {duration:.2f} seconds"
                )
            )

            command_exception = CommandException(
                command=__name__, count=exception_count
            )
            command_exception.save()
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Synced without exception in {duration:.2f} seconds"
                )
            )
