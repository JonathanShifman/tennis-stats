from SetHistory import SetHistory
import GameParser


def cross_merge_lists(list1, list2):
    merged_list = []
    for i in range(len(list1)):
        merged_list.append(list1[i])
        if i < len(list2):
            merged_list.append(list2[i])
    return merged_list


def get_game_tr_elements(set_div_element):
    game_tr_elements_odd = set_div_element.findAll('tr', attrs={'class': 'odd fifteen'})
    game_tr_elements_even = set_div_element.findAll('tr', attrs={'class': 'even fifteen'})
    return cross_merge_lists(game_tr_elements_odd, game_tr_elements_even)


def get_set_history(set_div_element):
    set_history = SetHistory()
    game_tr_elements = get_game_tr_elements(set_div_element)
    for game_tr_element in game_tr_elements:
        game_text = game_tr_element.findChildren('td')[0].text
        game_history = GameParser.get_game_history(game_text)
        set_history.add_game_history(game_history)
    return set_history
