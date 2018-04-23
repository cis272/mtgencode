import re

# Utilities for handling unicode, unary numbers and special symbols.
# For convenience we redefine everything from config so that it can all be accessed
# from the utils module.

import config

# special chunk of text that Magic Set Editor 2 requires at the start of all set files.
mse_prepend = 'mse version: 0.3.8\ngame: magic\nstylesheet: m15\nset info:\n\tsymbol:\nstyling:\n\tmagic-m15:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay:\n\tmagic-m15-clear:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-m15-extra-improved:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\tpt box symbols: magic-pt-symbols-extra.mse-symbol-font\n\t\toverlay: \n\tmagic-m15-planeswalker:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-m15-planeswalker-promo-black:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-m15-promo-dka:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-m15-token-clear:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-new-planeswalker:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-new-planeswalker-4abil:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-new-planeswalker-clear:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n\tmagic-new-planeswalker-promo-black:\n\t\ttext box mana symbols: magic-mana-small.mse-symbol-font\n\t\toverlay: \n'

# special chunk of text to start an HTML document.
import html_extra_data
segment_ids = html_extra_data.id_lables
html_prepend = html_extra_data.html_prepend
html_append = "\n</body>\n</html>"

# encoding formats we know about
formats = [
    'std',
    'named',
    'noname',
    'rfields',
    'old',
    'norarity',
    'vec',
    'custom',
]

# separators
cardsep = config.cardsep
fieldsep = config.fieldsep
bsidesep = config.bsidesep
newline = config.newline

# special indicators
dash_marker = config.dash_marker
bullet_marker = config.bullet_marker
this_marker = config.this_marker
counter_marker = config.counter_marker
reserved_marker = config.reserved_marker
choice_open_delimiter = config.choice_open_delimiter
choice_close_delimiter = config.choice_close_delimiter
x_marker = config.x_marker
tap_marker = config.tap_marker
untap_marker = config.untap_marker
rarity_free_marker = config.rarity_free_marker
rarity_common_marker = config.rarity_common_marker
rarity_rare_marker = config.rarity_rare_marker
rarity_epic_marker = config.rarity_epic_marker
rarity_legendary_marker = config.rarity_legendary_marker
rarity_no_rarity_marker = config.rarity_no_rarity_marker

json_rarity_map = {
	'FREE' : rarity_free_marker,
    'COMMON' : rarity_common_marker,
    'RARE' : rarity_rare_marker,
    'EPIC' : rarity_epic_marker,
    'LEGENDARY' : rarity_legendary_marker,
    'No Rarity' : rarity_no_rarity_marker,
}
json_rarity_unmap = {json_rarity_map[k] : k for k in json_rarity_map}

# unambiguous synonyms
counter_rename = config.counter_rename

# field labels
field_label_name = config.field_label_name
field_label_rarity = config.field_label_rarity
field_label_cost = config.field_label_cost
field_label_cardClass = config.field_label_cardClass
field_label_type = config.field_label_type
field_label_ah = config.field_label_ah
field_label_text = config.field_label_text

# additional fields we add to the json cards
json_field_bside = config.json_field_bside
json_field_set_name = config.json_field_set_name
json_field_info_code = config.json_field_info_code

# unicode / ascii conversion
unicode_trans = {
    u'\u2014' : dash_marker, # unicode long dash
    u'\u2022' : bullet_marker, # unicode bullet
    u'\u2019' : '"', # single quote
    u'\u2018' : '"', # single quote
    u'\u2212' : '-', # minus sign
	u'\u2026' : '...', #hozizontal ellipsis
    u'\xe6' : 'ae', # ae symbol
    u'\xfb' : 'u', # u with caret
    u'\xfa' : 'u', # u with accent
    u'\xe9' : 'e', # e with accent
	u'\xe8' : 'e', # e with grave
    u'\xe1' : 'a', # a with accent
    u'\xe0' : 'a', # a with accent going the other way
    u'\xe2' : 'a', # a with caret
    u'\xf6' : 'o', # o with umlaut
    u'\xed' : 'i', # i with accent
	u'\xf1' : 'n', # n with tilde
	u'\xa0' : ' ', # non-breaking space
}

# this one is one-way only
def to_ascii(s):
    for uchar in unicode_trans:
        s = s.replace(uchar, unicode_trans[uchar])
    return s

# unary numbers
unary_marker = config.unary_marker
unary_counter = config.unary_counter
unary_max = config.unary_max
unary_exceptions = config.unary_exceptions

def to_unary(s, warn = False):
    numbers = re.findall(r'[0123456789]+', s)
    # replace largest first to avoid accidentally replacing shared substrings
    for n in sorted(numbers, cmp = lambda x,y: cmp(int(x), int(y)), reverse = True):
        i = int(n)
        if i in unary_exceptions:
            s = s.replace(n, unary_exceptions[i])
        elif i > unary_max:
            i = unary_max
            if warn:
                print s
            s = s.replace(n, unary_marker + unary_counter * i)
        else:
            s = s.replace(n, unary_marker + unary_counter * i)
    return s

def from_unary(s):
    numbers = re.findall(re.escape(unary_marker + unary_counter) + '*', s)
    # again, largest first so we don't replace substrings and break everything
    for n in sorted(numbers, cmp = lambda x,y: cmp(len(x), len(y)), reverse = True):
        i = (len(n) - len(unary_marker)) / len(unary_counter)
        s = s.replace(n, str(i))
    return s

def to_symbols(s):
    jsymstrs = re.findall(json_symbol_regex, s)
    for jsymstr in sorted(jsymstrs, lambda x,y: cmp(len(x), len(y)), reverse = True):
        s = s.replace(jsymstr, json_symbol_trans[jsymstr])
    return s

def from_symbols(s, for_forum = False, for_html = False):
    symstrs = re.findall(symbol_regex, s)
    #for symstr in sorted(symstrs, lambda x,y: cmp(len(x), len(y)), reverse = True):
    # We have to do the right thing here, because the thing we replace exists in the thing
    # we replace it with...
    for symstr in set(symstrs):
        if for_html:
            s = s.replace(symstr, symbol_html_trans[symstr])
        elif for_forum:
            s = s.replace(symstr, symbol_forum_trans[symstr])
        else:
            s = s.replace(symstr, symbol_trans[symstr])
    return s

unletters_regex = r"[^abcdefghijklmnopqrstuvwxyz']"
