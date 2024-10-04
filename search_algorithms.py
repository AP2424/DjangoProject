import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from fantasy.models import Player

keyboard_ru_en = {'й':'q', 'ц':'w', 'у':'e', 'к':'r', 'е':'t', 'н':'y', 'г':'u', 'ш':'i',
                 'щ':'o', 'з':'p', 'ф':'a', 'ы':'s', 'в':'d', 'а':'f', 'п':'g', 'р':'h', 'о':'j',
                 'л':'k', 'д':'l', 'я':'z', 'ч':'x', 'с':'c', 'м':'v', 'и':'b', 'т':'n', 'ь':'m'}

def check_for_same(squadlist, player):
    i = 0
    found = False
    while found == False:
        compared = squadlist[i]
        if compared.name.startswith(player[0]) or compared.name.endswith(player[-1]):
            found = True
            break
        i += 1
    return found, compared


def delete_duplicates(club):
    squadlist = Player.objects.filter(club=club)
    for player in squadlist:
        playerlist = player.split()
        found, compared = check_for_same(squadlist, playerlist)
        if found:
            if player.position == compared.position and player.birthdate == compared.birthdate:
                Player.objects.delete(name=compared.name)

# algorithm for parsing from other websites
def compare_with_existing(textlist, playerlist):
    # differences from ascii table
    ascii_diff = 0
    # differences which are not in the ascii table (letters with hyphens etc.)
    not_ascii_diff = 0
    # default values
    matched_characters = 0
    less_words = textlist
    more_words = playerlist
    words_lengths_comparison_indicator = 0
    extra_words = 0
    # checking for extra word (ex. Real Betis <-> Betis)
    words_diff = len(textlist) - len(playerlist)
    # deciding which object has more words
    if words_diff > 0:
        less_words = playerlist
        more_words = textlist
        words_lengths_comparison_indicator = 1
    elif words_diff < 0:
        less_words = textlist
        more_words = playerlist
        words_lengths_comparison_indicator = -1
    for i in range(len(less_words)):
        # checking for extra character (ex. Valladolid <-> Valadolid)
        letters_diff = len(more_words[i]) - len(less_words[i])
        # deciding which object has more letters
        if letters_diff >= 0:
            bigger_word = textlist[i]
            smaller_word = playerlist[i]
        else:
            bigger_word = playerlist[i]
            smaller_word = textlist[i]
        for k in range(len(smaller_word)):
            # defining two letters to compare
            pl_letter = playerlist[i][k]
            text_letter = textlist[i][k]
            # if the letters are different
            if pl_letter != text_letter:
                # if the letters are different and in ascii table
                if pl_letter.isascii() and text_letter.isascii():
                    ascii_diff += 1
                    """ if the words lengths are not equal and the next character of the bigger word 
                    equals current character of the smaller word """
                    if len(bigger_word) != len(smaller_word) and smaller_word[k] == bigger_word[k+1]:
                        # pop current character of the bigger word
                        bigger_word.pop(k)
                    # if the words lengths are the same, we cannot do anything here
                else:
                    not_ascii_diff += 1

                if ascii_diff >= 2 and words_lengths_comparison_indicator != 0:
                    
                    extra_words += 1
                    more_words.pop(i)
                    break
            else:
                matched_characters += 1

    points = matched_characters - 2*extra_words - ascii_diff - 0.5*not_ascii_diff
    return points


#delete_duplicates(Club.objects.filter(name='Real Madrid').first())
print(compare_with_existing('Real Betis', 'Real Betis Balompie'))


