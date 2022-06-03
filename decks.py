"""
This module is for managing decks. It contains functions for manipulating decks.txt.
"""

import tempfile
import re


temp_path = tempfile.gettempdir()


def get_deck_lines():
    """
    Returns a list with all the lines in decks.txt (each line corresponds to a deck).
    """
    with open(f"{temp_path}\\..\\MemoryGain\\decks.txt", "r") as decks_text:
        return decks_text.readlines()


def get_deck_name(i):
    with open(f"{temp_path}\\..\\MemoryGain\\decks.txt", "r") as decks_text:
        return decks_text.readlines()[i].replace("\n", "")


def del_deck(deck):
    """
    Deletes a deck from decks.txt and the cards belonging to that deck in cards.txt. No return.
    """
    decks_text = open(f"{temp_path}\\..\\MemoryGain\\decks.txt", "r")
    decks_lines = decks_text.readlines()
    index = decks_lines.index(deck + "\n")
    decks_lines.pop(index)
    decks_text.close()

    decks_text = open(f"{temp_path}\\..\\MemoryGain\\decks.txt", "w")
    decks_text.writelines(decks_lines)
    decks_text.close()

    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "r")
    cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=|DUE\^\^\$=|INTERVAL\^\^\$=|PHASE\^\^\$=", cards_text.read())
    cards_parts.pop(0)
    cards_text.close()

    # Removes \n.
    for i in range(len(cards_parts)):
        if i % 7 == 6:
            cards_parts[i] = cards_parts[i][:-1]

    cards = []
    for i in range(len(cards_parts)):
        if i % 7 == 6:
            store_list = [cards_parts[i - 6], cards_parts[i - 5], cards_parts[i - 4], cards_parts[i - 3], cards_parts[i - 2], cards_parts[i - 1], cards_parts[i]]
            cards.append(store_list)

    # Writes.
    cards_to_write = []
    for card in cards:
        if card[0] != deck:
            cards_to_write.append(
                f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "w")
    cards_text.writelines(cards_to_write)
    cards_text.close()


def add_deck(deck):
    decks_text = open(f"{temp_path}\\..\\MemoryGain\\decks.txt", "a")
    decks_text.write(deck + "\n")
    decks_text.close()

    # Writes the decks in alphabetical order so the deck buttons will also be in order and have their index.
    # match to the corresponding line in decks.txt.
    decks_text = open(f"{temp_path}\\..\\MemoryGain\\decks.txt", "r")
    decks_sorted = decks_text.readlines()
    decks_sorted.sort(key=str.lower)
    decks_text.close()

    decks_text = open(f"{temp_path}\\..\\MemoryGain\\decks.txt", "w")
    decks_text.writelines(decks_sorted)
    decks_text.close()
