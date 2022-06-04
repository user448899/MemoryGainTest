"""
This module is for managing cards. It contains functions for manipulating cards.txt.
"""

import tempfile
import re
import datetime
import os


temp_path = tempfile.gettempdir()


def cards_on_device():
    """
    Checks if cards.txt is on device, if not it is added. decks.decks_on_device() must be called first to make
    the MemoryGain dir.
    """
    cards_found = os.path.exists(f"{temp_path}\\..\\MemoryGain\\decks.txt")

    if not cards_found:
        os.system(f"n > {temp_path}\\..\\MemoryGain\\cards.txt")


def get_num_to_study():
    """
    Find out how many cards need to be studied today. Returns int.
    """
    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "r")
    cards_parts = re.split("DUE\^\^\$=|INTERVAL\^\^\$=", cards_text.read())
    cards_text.close()
    cards_parts.pop(0)
    amt_to_study = 0
    today = str(datetime.datetime.now())
    end_of_today = datetime.datetime(int(today[:4]), int(today[5:7]), int(today[8:10]), 23, 59, 59, 999999)
    for idx, part in enumerate(cards_parts):
        if idx % 2 == 0 and datetime.datetime.strptime(part, "%Y-%m-%d %H:%M:%S.%f") <= end_of_today:
            amt_to_study += 1

    return amt_to_study


def get_card():
    """
    Out of all cards due today (at any time), finds a card to study according to the following (in order):
    1. Over-dues (most overdue to least overdue) (over-dues are cards due before current time).
    2. "l" and "b" due in 30 sec + "g" and "B" due in 3 min, in date order.
    3. "L" in date order.
    4. "G" in date order.
    5. Rest of "l", "b", "g", and "B" in reverse date order.
    Returns false if no cards are due sometime today. Else it returns a list with the details of the card.
    """
    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "r")
    if len(cards_text.read()) == 0:
        return False
    else:
        cards_text.seek(0)
        cards_parts = re.split("DECK\^\^\$=|QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=|DUE\^\^\$=|INTERVAL\^\^\$=|PHASE\^\^\$=", cards_text.read())
        cards_parts.pop(0)
        cards_text.close()
        # Removes those not due today.
        today = str(datetime.datetime.now())
        end_of_today = datetime.datetime(int(today[:4]), int(today[5:7]), int(today[8:10]), 23, 59, 59, 999999)
        i = 0
        while i < len(cards_parts):
            if i % 7 == 4 and datetime.datetime.strptime(cards_parts[i], "%Y-%m-%d %H:%M:%S.%f") > end_of_today:
                for j in range(7):
                    cards_parts.pop(i - 4)
                i = i - 4
            else:
                i += 1

        if len(cards_parts) == 0:
            return False
        else:
            # Removes \n.
            for i in range(len(cards_parts)):
                if i % 7 == 6:
                    cards_parts[i] = cards_parts[i][:-1]

            cards = []
            for i in range(len(cards_parts)):
                if i % 7 == 6:
                    store_list = [cards_parts[i - 6], cards_parts[i - 5], cards_parts[i - 4], cards_parts[i - 3],
                                  cards_parts[i - 2], cards_parts[i - 1], cards_parts[i]]
                    cards.append(store_list)

            # Over-dues in order (most over-due to least) using bubble sort.
            over_dues = []
            for card in cards:
                if datetime.datetime.strptime(card[4], "%Y-%m-%d %H:%M:%S.%f") < datetime.datetime.now():
                    over_dues.append(card)

            length = len(over_dues)
            while length > 1:
                for i in range(length - 1):
                    if datetime.datetime.strptime(over_dues[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(over_dues[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                        smaller = over_dues[i + 1]
                        over_dues[i + 1] = over_dues[i]
                        over_dues[i] = smaller
                length -= 1

            if len(over_dues) != 0:
                return over_dues[0]
            else:
                # "l" and "b" due in 30 sec + "g" and "B" due in 3 min, in order, using bubble sort. THIS IS IF NO OVER-DUES.
                l_b_list = []
                g_B_list = []
                for card in cards:
                    if (card[6] == "l" or card[6] == "b") and (datetime.datetime.strptime(card[4], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.now() < datetime.timedelta(seconds=30)):
                        l_b_list.append(card)

                for card in cards:
                    if (card[6] == "g" or card[6] == "B") and (datetime.datetime.strptime(card[4], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.now() < datetime.timedelta(seconds=180)):
                        g_B_list.append(card)

                l_b_g_B_list = l_b_list + g_B_list

                length = len(l_b_g_B_list)
                while length > 1:
                    for i in range(length - 1):
                        if datetime.datetime.strptime(l_b_g_B_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(l_b_g_B_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                            smaller = l_b_g_B_list[i + 1]
                            l_b_g_B_list[i + 1] = l_b_g_B_list[i]
                            l_b_g_B_list[i] = smaller
                    length -= 1

                if len(l_b_g_B_list) != 0:
                    return l_b_g_B_list[0]
                else:
                    # "L" in order. This is for "l", and/or "b"s due in 30 sec and no "g", or "B"s due in 3 min.
                    L_list = []
                    for card in cards:
                        if card[6] == "L":
                            L_list.append(card)

                    length = len(L_list)
                    while length > 1:
                        for i in range(length - 1):
                            if datetime.datetime.strptime(L_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(L_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                                smaller = L_list[i + 1]
                                L_list[i + 1] = L_list[i]
                                L_list[i] = smaller
                        length -= 1

                    if len(L_list) != 0:
                        return L_list[0]
                    else:
                        # "G" in order. This is if there are no over-dues; "l" or "b"s due in 30 sec and no "g", or "B"s due in 3 min; and no "L"s.
                        G_list = []
                        for card in cards:
                            if card[6] == "G":
                                G_list.append(card)

                        length = len(G_list)
                        while length > 1:
                            for i in range(length - 1):
                                if datetime.datetime.strptime(G_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(G_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                                    smaller = G_list[i + 1]
                                    G_list[i + 1] = G_list[i]
                                    G_list[i] = smaller
                            length -= 1

                        if len(G_list) != 0:
                            return G_list[0]
                        else:
                            # "l", "b", "g", and "B" in reverse order. This is if there are no over-dues; "l" or "b"s due in 30 sec and no "g" or "B"s due in 3 min; "L"s; or "G"s.
                            l_b_g_B_rev_list = []
                            for card in cards:
                                if card[6] == "l" or card[6] == "b" or card[6] == "g" or card[6] == "B":
                                    l_b_g_B_rev_list.append(card)

                            # This sorts from earliest to latest but takes the last one.
                            length = len(l_b_g_B_rev_list)
                            while length > 1:
                                for i in range(length - 1):
                                    if datetime.datetime.strptime(l_b_g_B_rev_list[i][4], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.strptime(l_b_g_B_rev_list[i + 1][4], "%Y-%m-%d %H:%M:%S.%f"):
                                        smaller = l_b_g_B_rev_list[i + 1]
                                        l_b_g_B_rev_list[i + 1] = l_b_g_B_rev_list[i]
                                        l_b_g_B_rev_list[i] = smaller
                                length -= 1
                            if len(l_b_g_B_rev_list) != 0:
                                return l_b_g_B_rev_list[-1]


def write_card_ac(card_to_write):
    """
    Writes card to cards.txt when the again or correct button is pressed. No return.
    """
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

    for card in cards:
        # EASE, DUE, INTERVAL, PHASE.
        if card[0] == card_to_write[0] and card[1] == card_to_write[1]:
            card[3] = card_to_write[3]
            card[4] = card_to_write[4]
            card[5] = card_to_write[5]
            card[6] = card_to_write[6]
            break

    # Writes
    cards_to_write = []
    for card in cards:
        cards_to_write.append(f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "w")
    cards_text.writelines(cards_to_write)
    cards_text.close()


def del_card(deck, qst):
    """
    Finds and deletes a card from cards.txt. No return.
    """
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

    # Only has to check that the deck and question match, as there cannot be a duplicate question in a deck.
    for idx, card in enumerate(cards):
        if (card[0] == deck) and (card[1] == qst):
            cards.pop(idx)

    cards_to_write = []
    for card in cards:
        cards_to_write.append(
            f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "w")
    cards_text.writelines(cards_to_write)
    cards_text.close()


def write_card_edit_save(deck, qst, new_qst, new_ans):
    """
    When the save button is clicked from the edit page, this function updates the card in cards.txt. No return.
    """
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

    for card in cards:
        if (card[0] == deck) and (card[1] == qst):
            card[1] = new_qst
            card[2] = new_ans
            break

    cards_to_write = []
    for card in cards:
        cards_to_write.append(f"DECK^^$={card[0]}QUESTION^^$={card[1]}ANSWER^^$={card[2]}EASE^^$={card[3]}DUE^^$={card[4]}INTERVAL^^$={card[5]}PHASE^^$={card[6]}\n")

    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "w")
    cards_text.writelines(cards_to_write)
    cards_text.close()


def search_query_exists(query):
    """
    Checks if the query parameter is found is any of the cards in cards.txt. Returns either True or False.
    """
    with open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "r") as cards_text:
        cards = re.split("QUESTION\^\^\$=|ANSWER\^\^\$=|EASE\^\^\$=", cards_text.read())

    cards.pop(0)

    for i in range(len(cards)):
        if i % 3 == 0 or i % 3 == 1:
            if query in cards[i]:
                return True

    return False


def search_for_cards(deck, query, search_upto):
    """
    Searches cards.txt for cards that contain the query in either the question or answer. After finding all the cards
    with the query it returns the question and answer of the one at index [search_upto], it also returns the number
    of cards with the query.
    """
    qst = ""
    ans = ""

    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "r")
    search_card_idxs = []
    cards = cards_text.read().split("DECK^^$=")
    cards.pop(0)
    cards_deck_and_rest = []
    # Gets deck, rest: 0, 1
    for i in range(len(cards)):
        cards_deck_and_rest.append(cards[i][:cards[i].index("QUESTION^^$=")])
        cards_deck_and_rest.append(cards[i][cards[i].index("QUESTION^^$="):])

    # Adds indexes of query-containing cards to search_card_idxs.
    for i in range(len(cards)):
        if deck == cards_deck_and_rest[i * 2]:
            qst_onwards = cards_deck_and_rest[i * 2 + 1].split("QUESTION^^$=")
            qst = qst_onwards[1].split("ANSWER^^$=")[0]
            ans = qst_onwards[1].split("ANSWER^^$=")[1].split("EASE^^$=")[0]
            if query in qst or query in ans:
                search_card_idxs.append(i)

    # Gets qst and ans. Uses search_upto for specific card.
    if len(search_card_idxs) != 0:
        qst_onwards = cards[search_card_idxs[search_upto]].split("QUESTION^^$=")
        qst = qst_onwards[1].split("ANSWER^^$=")[0]
        ans = qst_onwards[1].split("ANSWER^^$=")[1].split("EASE^^$=")[0]

    cards_text.close()

    return qst, ans, len(search_card_idxs)


def del_searched_card(deck, query, search_upto):
    """
    Finds the card the user is currently viewing and deletes it.
    """
    qst, ans, amt_cards = search_for_cards(deck, query, search_upto)
    del_card(deck, qst)


def save_searched_card(deck, query, search_upto, new_qst, new_ans):
    """
    Finds the card the user is currently viewing and saves their changes.
    """
    qst, ans, amt_cards = search_for_cards(deck, query, search_upto)
    write_card_edit_save(deck, qst, new_qst, new_ans)


def check_qst_exists(qst):
    """
    Checks if a question already exists in a card. Returns True is it does, and returns False if it does not.
    """
    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "r")
    cards = cards_text.read().split("QUESTION^^$=")
    cards.pop(0)
    cards_text.close()

    qsts = []

    for card in cards:
        qsts.append(card.split("ANSWER^^$=")[0])

    if qst in qsts:
        return True

    return False


def add_card(deck, qst, ans):
    """
    Appends a card to cards.txt.
    """
    cards_text = open(f"{temp_path}\\..\\MemoryGain\\cards.txt", "a")
    cards_text.write(f"DECK^^$={deck}QUESTION^^$={qst}ANSWER^^$={ans}EASE^^$=2.3DUE^^$={datetime.datetime.now()}INTERVAL^^$=0PHASE^^$=L\n")
    cards_text.close()





