import re

# Utilities for handling unicode, unary numbers, mana costs, and special symbols.
# For convenience we redefine everything from utils so that it can all be accessed
# from the utils module.

# separators
cardsep = '\n\n'
fieldsep = '|'
bsidesep = '\n'
newline = '\\'

# special indicators
dash_marker = '~'
bullet_marker = '='
this_marker = '@'
counter_marker = '%'
reserved_marker = '\v'
reserved_mana_marker = '$'
choice_open_delimiter = '['
choice_close_delimiter = ']'
x_marker = 'X'
tap_marker = 'T'
untap_marker = 'Q'
rarity_free_marker = 'F'
rarity_common_marker = 'C'
rarity_rare_marker = 'R'
rarity_epic_marker = 'E'
rarity_legendary_marker = 'L'
rarity_no_rarity_marker = 'N'

# unambiguous synonyms
counter_rename = 'uncast'

# unary numbers
unary_marker = '&'
unary_counter = '^'
unary_max = 20
unary_exceptions = {
    25 : 'twenty' + dash_marker + 'five',
    30 : 'thirty',
    40 : 'forty',
    50 : 'fifly',
    100: 'one hundred',
    200: 'two hundred',
}

# field labels, to allow potential reordering of card format
field_label_name = '1'
field_label_rarity = '2'
field_label_cost = '3'
field_label_cardClass = '4'
field_label_type = '5'
field_label_ah = '6'
field_label_text = '7'

# additional fields we add to the json cards
json_field_bside = 'bside'
json_field_set_name = 'setName'
json_field_info_code = 'hearthstoneCardsInfoCode'
