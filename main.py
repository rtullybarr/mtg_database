from database_writer import DatabaseWriter
from mtg_loader import MTGLoader
from scraper import WebScraper
import csv

# Checks whether a particular card is from an un set
def un_set(card):
    for edition in card['editions']:
        if edition['set'] == 'Unhinged' or edition['set'] == 'Unglued':
            return True

    return False

def load_mtg_data():
    deckbrew_loader = MTGLoader('https://api.deckbrew.com/mtg/')
    colours = deckbrew_loader.get_mtg_data('colors')
    supertypes = deckbrew_loader.get_mtg_data('supertypes')
    types = deckbrew_loader.get_mtg_data('types')
    subtypes = deckbrew_loader.get_mtg_data('subtypes')
    #sets = deckbrew_loader.get_mtg_data('sets')
    cards = deckbrew_loader.get_mtg_data('cards')

    # Filter out unhinged / unglued; contain a lot of pesky edge cases that aren't important.
    print(len(cards))
    cards = [card for card in cards if not un_set(card)]
    print(len(cards))
    # get datatype sizes
    text_len = 0
    flavour_len = 0
    cost_len = 0
    card_id_len = 0
    card_name_len = 0

    for card in cards:
        if len(card['id']) > card_id_len:
            card_id_len = len(card['id'])

        if len(card['name']) > card_name_len:
            card_name_len = len(card['name'])

        if len(card['text']) > text_len:
            text_len = len(card['text'])

        if len(card['cost']) > cost_len:
            cost_len = len(card['cost'])

        for edition in card['editions']:
            if 'flavor' in edition and len(edition['flavor']) > flavour_len:
                flavour_len = len(edition['flavor'])

    # 33
    print("Longest card name: %d" % card_name_len)

    # 33
    print("Longest card id: %d" % card_id_len)

    # 656
    print("Longest text: %d" % text_len)

    # 30
    print("Longest cost: %d" % cost_len)

    # 313
    print("Longest flavour text: %d" % flavour_len)

    # Fill some gaps in the data using a second API
    mtgio_loader = MTGLoader('https://api.magicthegathering.io/v1/')
    # release_date
    sets = mtgio_loader.get_mtg_data('sets')

    return supertypes, types, subtypes, sets, cards, colours

def populate_database(supertypes, types, subtypes, sets, cards, colours):
    # Add all sets and cards to the db
    dbwriter = DatabaseWriter()
    dbwriter.add_supertypes(supertypes)
    dbwriter.add_types(types)
    dbwriter.add_subtypes(subtypes)
    dbwriter.add_sets(sets)
    dbwriter.add_cards(cards)
    dbwriter.add_card_colours(cards, colours)
    dbwriter.add_card_supertypes(cards)
    dbwriter.add_card_types(cards)
    dbwriter.add_card_subtypes(cards)
    dbwriter.add_editions(cards)
    dbwriter.add_legalities(cards)

def scrape_for_prices(cards):

    #prices, not_found = scraper.scrape_all(cards)
    #print(prices)
    #print(not_found)
    multiverse_ids = set()
    try:
        for filename in ["prices_abc.csv", "prices_2.csv", "prices_3.csv"]:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                for line in reader:
                    multiverse_ids.add(int(line[0]))

    except FileNotFoundError:
        pass

    scraper = WebScraper('https://www.mtggoldfish.com/price-download/paper/', multiverse_ids)
    scraper.download_csv(cards)

if __name__ == "__main__":
    supertypes, types, subtypes, sets, cards, colours = load_mtg_data()
    #dbwriter = DatabaseWriter()
    #dbwriter.add_editions(cards)

    scrape_for_prices(cards)
