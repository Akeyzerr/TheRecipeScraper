from __future__ import print_function
import os
from time import sleep
from builtins import input
from modules.handlers import string_handler_unicode_to_byte


class MainMenu(object):
    def __init__(self, fulfilled_inquiry):
        self._fi = fulfilled_inquiry
        self._choice = None
        self._exit_choice = None
        self._exit_state = False
        self._reverse_sort = False

    def _query_reverse_sort(self):
        sort_ask = input('Select sorting option:\n(A) - ascending\n(D) - descending\n')
        assert isinstance(self._choice, str)
        if sort_ask.lower() == "a":
            self._reverse_sort = False
        elif sort_ask.lower() == "d":
            self._reverse_sort = True
        else:
            pass

    @staticmethod
    def _console_clear():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def main_menu(self):
        self._console_clear()

        while not self._exit_state:
            print(
                """
                1. Printout recipes
                2. Sort by Title
                3. Sort by Ingredients (Total Count)
                4. Sort by Ingredients (Unique) 
                5. Sort by Chef's Popularity
                6. Sort by Recipe Rating
                7. Sort by Times Cooked
                8. Export json report
                9. Send to GSheets
                0. Exit
                """
            )
            self._choice = input('Select option: ')
            assert isinstance(self._choice, str)

            if self._choice == "1":
                self._console_clear()
                for r in self._fi.result_storage:
                    print("{}, Times cooked: {}, Rating: {}\n"
                          "\tProducts Count: {}, Unique: {}\n"
                          "\tChef name: {}, Chef's popularity: {}".format(
                            r,
                            r.times_cooked,
                            r.rating,
                            len(r.ingredients),
                            r.ingredients.get_unique_count(),
                            string_handler_unicode_to_byte(r.chef.name),
                            string_handler_unicode_to_byte(r.chef.popularity)))
                    print(r.ingredients)
            elif self._choice == "2":
                self._console_clear()
                self._query_reverse_sort()
                self._fi.result_storage.sort_by_title(reversed_flag=self._reverse_sort)
                self._console_clear()
            elif self._choice == "3":
                self._console_clear()
                self._query_reverse_sort()
                self._fi.result_storage.sort_by_total_ingredients_count(reversed_flag=self._reverse_sort)
                self._console_clear()
            elif self._choice == "4":
                self._console_clear()
                self._query_reverse_sort()
                self._fi.result_storage.sort_by_unique_ingredients_count(reversed_flag=self._reverse_sort)
                self._console_clear()
            elif self._choice == "5":
                self._console_clear()
                self._query_reverse_sort()
                self._fi.result_storage.sort_by_chef_popularity(reversed_flag=self._reverse_sort)
                self._console_clear()
            elif self._choice == "6":
                self._console_clear()
                self._query_reverse_sort()
                self._fi.result_storage.sort_by_recipe_rating(reversed_flag=self._reverse_sort)
                self._console_clear()
            elif self._choice == "7":
                self._console_clear()
                self._query_reverse_sort()
                self._fi.result_storage.sort_by_times_cooked(reversed_flag=self._reverse_sort)
                self._console_clear()
            elif self._choice == "8":
                self._fi.result_storage.export_json()
            elif self._choice == "9":
                from modules.gs_upload import GSUploader
                gs = GSUploader(self._fi.
                                result_storage.
                                get_csv)
                gs.upload()
            elif self._choice == "0":
                self._exit_choice = input("Are you sure you want to exit? [y/N]")
                assert isinstance(self._exit_choice, str)
                if self._exit_choice.lower() == "y":
                    self._exit_state = True
                else:
                    self._exit_state = False
            else:
                print("not valid choice")
                sleep(1)
                self._console_clear()
                self._choice = False

