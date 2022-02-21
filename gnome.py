#!/usr/bin/env python

# main screen turn on
# 1. list of items in pantry
# 2. shopping list
# 3. update wizard

import sys

from collections import defaultdict
from simple_term_menu import TerminalMenu

LIST_ITEMS = "1. List items in pantry"
VIEW_LIST = "2. View shopping list"
WIZARD = "3. Update wizard"
ADD_ITEM = "4. Add item"
EXIT = "Exit"

class Item(object):
    name = None
    stores = None
    perishable = False
    last_purchased = None
    count_purchased = 0
    wanted = False

    def __init__(self, name, store, perishable):
        self.name = name
        self.stores = [store]
        self.perishable = perishable

        pantry.append(self)


    def __str__(self):
        return f"Item {self.name} available from {self.stores}"







def show_menu(options):
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]

def show_main_menu():
    return show_menu([
        LIST_ITEMS,
        VIEW_LIST,
        WIZARD,
        ADD_ITEM,
        EXIT
    ])


pantry = []


def list_pantry():
    print("Listing pantry:")

    for item in pantry:
        print(item)


def list_shopping():
    print("Displaying shopping list")

    stores = defaultdict(list)
    for item in pantry:
        for s in item.stores:
            if item.wanted:
                stores[s].append(item)


    for k,v in stores.items():
        print(f"Store {k} has:")
        for i in v:
            print(i.name)



            
def add_item():
    name = input("Name: ")
    store = input("Store: ")
    pvalue = input("Perishable (y/n): ")
    perishable = (pvalue == "y" or pvalue == "yes") and True or False
    item = Item(name, store, perishable)

def update_wizard():
    print("Displaying update wizard")

    for item in pantry:
        wvalue = input(f"Do you need more {item.name}? (y/n)")
        item.wanted = (wvalue == "y" or wvalue == "yes") and True or False



if __name__ == '__main__':

    milk = Item("milk", "Safeway", True)
    milk.wanted = True
    Item("butter", "Safeway", True)
    Item("PB crackers", "Trader Joe's", False)


    while True:
        choice = show_main_menu()

        if choice == LIST_ITEMS:
            list_pantry()
        elif choice == VIEW_LIST:
            list_shopping()
        elif choice == WIZARD:
            update_wizard()
        elif choice == ADD_ITEM:
            add_item()
        else:
            sys.exit(0)
