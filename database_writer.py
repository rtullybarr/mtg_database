class DatabaseWriter():

    def __init__(self):
        pass

    def add_supertypes(self, supertypes):
        with open('sql/supertypes.sql', 'w', encoding='utf-8') as sqlfile:
            sqlfile.write('DROP TABLE supertypes;\n')
            sqlfile.write('CREATE TABLE supertypes ('
                          'supertype VARCHAR(30) PRIMARY KEY);\n')

            sqlfile.write('INSERT INTO supertypes(supertype) VALUES\n')
            for i, supertype in enumerate(supertypes):
                if i != 0:
                    sqlfile.write(',\n')
                sqlfile.write('("' + supertype + '")')
            sqlfile.write(';\n')

    def add_types(self, types):
        with open('sql/types.sql', 'w', encoding='utf-8') as sqlfile:
            sqlfile.write('DROP TABLE card_types;\n')
            sqlfile.write('CREATE TABLE card_types ('
                          'card_type VARCHAR(30) PRIMARY KEY);\n')

            sqlfile.write('INSERT INTO card_types(card_type) VALUES\n')
            for i, type in enumerate(types):
                if i != 0:
                    sqlfile.write(',\n')
                sqlfile.write('("' + type + '")')
            sqlfile.write(';\n')

    def add_subtypes(self, subtypes):
        with open('sql/subtypes.sql', 'w', encoding='utf-8') as sqlfile:
            sqlfile.write('DROP TABLE subtypes;\n')
            sqlfile.write('CREATE TABLE subtypes ('
                          'subtype VARCHAR(30) PRIMARY KEY);\n')

            sqlfile.write('INSERT INTO subtypes(subtype) VALUES\n')
            for i, subtype in enumerate(subtypes):
                if i != 0:
                    sqlfile.write(',\n')
                sqlfile.write('("' + subtype + '")')
            sqlfile.write(';\n')

    def add_sets(self, sets):
        with open('sql/sets.sql', 'w', encoding='utf-8') as sqlfile:
            sqlfile.write('DROP TABLE sets;\n')
            sqlfile.write('CREATE TABLE sets ('
                          'set_id VARCHAR(10) PRIMARY KEY,'
                          'set_name VARCHAR(50),'
                          'release_date DATE,'
                          'set_type VARCHAR(30),'
                          'border ENUM(\'black\',\'white\',\'silver\'));\n')

            sqlfile.write('INSERT INTO sets(set_id,set_name,set_type,release_date,border) VALUES ')
            for i, set in enumerate(sets):
                if i != 0:
                    sqlfile.write(',\n')
                sqlfile.write('("' + set['code'] + '","' + set['name'].replace('"', r'\"') + '","' + set['type'] + '","'
                                    + set['releaseDate'] + '","' + set['border'] + '")')
            sqlfile.write(';\n')

    def add_cards(self, cards):
        with open('sql/cards.sql', 'w', encoding='utf-8') as sqlfile:
            # create tables
            # cards
            sqlfile.write('DROP TABLE cards;\n')
            sqlfile.write('CREATE TABLE cards ('
                          'card_id VARCHAR(50) NOT NULL PRIMARY KEY, '
                          'card_name VARCHAR(50), '
                          'cmc INT, '
                          'cost VARCHAR(50), '
                          'text VARCHAR(1000));\n')

            # insert data
            for card in cards:
                # card
                sqlfile.write('INSERT INTO cards(card_id,card_name,cmc,cost,text) '
                              'VALUES ("' + card['id'] + '","' + card['name'].replace('"', r'\"') + '",' +
                              str(card['cmc']) + ',"' + card['cost'] + '","' + card['text'].replace('"', r'\"') + '");\n')

    def add_card_colours(self, cards, colours):
        with open('sql/card_colours.sql', 'w', encoding='utf-8') as sqlfile:
            # card_colours
            sqlfile.write('DROP TABLE card_colour;\n')
            sqlfile.write('CREATE TABLE card_colour ('
                          'card_id VARCHAR(30), '
                          'colour ENUM(')

            for i, colour in enumerate(colours):
                if i != 0:
                    sqlfile.write(',')
                sqlfile.write("'" + colour + "'")

            sqlfile.write('), CONSTRAINT fk_card_colour FOREIGN KEY (card_id) REFERENCES cards(card_id));\n')

            for card in cards:
                # colour(s)
                # some cards are colorless
                if 'colors' in card:
                    sqlfile.write('INSERT INTO card_colour(card_id,colour) VALUES ')
                    for i, colour in enumerate(card['colors']):
                        if i != 0:
                            sqlfile.write(',')
                        sqlfile.write('("' + card['id'] + '","' + colour + '")')
                    sqlfile.write(';\n')

    def add_card_supertypes(self, cards):
        with open('sql/card_supertypes.sql', 'w', encoding='utf-8') as sqlfile:
            # card_supertype
            sqlfile.write('DROP TABLE card_supertype;\n')
            sqlfile.write('CREATE TABLE card_supertype ('
                          'card_id VARCHAR(30),'
                          'supertype VARCHAR(30),'
                          'CONSTRAINT fk_card_supertype FOREIGN KEY (card_id) REFERENCES cards(card_id),'
                          'CONSTRAINT fk_supertype FOREIGN KEY (supertype) REFERENCES supertypes(supertype),'
                          'CONSTRAINT pk_card_supertype PRIMARY KEY (card_id, supertype));\n')

            for card in cards:
                # supertype(s)
                # Not all cards have a supertype
                if 'supertypes' in card:
                    sqlfile.write('INSERT INTO card_supertype(card_id,supertype) VALUES ')
                    for i, supertype in enumerate(card['supertypes']):
                        if i != 0:
                            sqlfile.write(',')
                        sqlfile.write('("' + card['id'] + '","' + supertype + '")')
                    sqlfile.write(';\n')

    def add_card_types(self, cards):
        with open('sql/card_types.sql', 'w', encoding='utf-8') as sqlfile:
            # card_type
            sqlfile.write('DROP TABLE card_type;\n')
            sqlfile.write('CREATE TABLE card_type ('
                          'card_id VARCHAR(30),'
                          'card_type VARCHAR(30),'
                          'CONSTRAINT fk_card_type FOREIGN KEY (card_id) REFERENCES cards(card_id),'
                          'CONSTRAINT fk_type FOREIGN KEY (card_type) REFERENCES card_types(card_type),'
                          'CONSTRAINT pk_card_type PRIMARY KEY (card_id, card_type));\n')

            for card in cards:
                # type(s)
                if 'types' in card:
                    sqlfile.write('INSERT INTO card_type(card_id,card_type) VALUES ')
                    for i, type in enumerate(card['types']):
                        if i != 0:
                            sqlfile.write(',')
                        sqlfile.write('("' + card['id'] + '","' + type + '")')
                    sqlfile.write(';\n')

    def add_card_subtypes(self, cards):
        with open('sql/card_subtypes.sql', 'w', encoding='utf-8') as sqlfile:
            # card_subtype
            sqlfile.write('DROP TABLE card_subtype;\n')
            sqlfile.write('CREATE TABLE card_subtype ('
                          'card_id VARCHAR(50),'
                          'subtype VARCHAR(30),'
                          'CONSTRAINT fk_card_subtype FOREIGN KEY (card_id) REFERENCES cards(card_id),'
                          'CONSTRAINT fk_subtype FOREIGN KEY (subtype) REFERENCES subtypes(subtype),'
                          'CONSTRAINT pk_card_subtype PRIMARY KEY (card_id, subtype));\n')

            # subtype(s)
            # not all cards have a subtype
            for card in cards:
                if 'subtypes' in card:
                    sqlfile.write('INSERT INTO card_subtype(card_id,subtype) VALUES ')
                    for i, subtype in enumerate(card['subtypes']):
                        if i != 0:
                            sqlfile.write(',')
                        sqlfile.write('("' + card['id'] + '","' + subtype + '")')
                    sqlfile.write(';\n')

    def add_editions(self, cards):
        with open('sql/editions.sql', 'a', encoding='utf-8') as sqlfile:
            # editions
            sqlfile.write('DROP TABLE editions;\n')
            sqlfile.write('CREATE TABLE editions ('
                          'multiverse_id INT PRIMARY KEY,'
                          'card_id VARCHAR(50),'
                          'set_id VARCHAR(10),'
                          'rarity VARCHAR(10),'
                          'flavor_text VARCHAR(500),'
                          'artist VARCHAR(80),'
                          'CONSTRAINT fk_card_edition FOREIGN KEY (card_id) REFERENCES cards(card_id),'
                          'CONSTRAINT fk_set_edition FOREIGN KEY (set_id) REFERENCES sets(set_id));\n')

            # create prices table
            sqlfile.write('DROP TABLE prices;\n')
            sqlfile.write('CREATE TABLE prices ('
                          'multiverse_id INT,'
                          'date DATE,'
                          'low_price DECIMAL(19,4),'
                          'average_price DECIMAL(19,4),'
                          'high_price DECIMAL(19,4), '
                          'CONSTRAINT fk_price_edition FOREIGN KEY (multiverse_id) REFERENCES editions(multiverse_id));\n')

            for card in cards:
                # editions
                for edition in card['editions']:
                    # exclude printings with multiverse_id=0
                    if edition['multiverse_id'] == 0:
                        continue

                    sqlfile.write('INSERT INTO editions (multiverse_id,card_id,rarity,artist,set_id')
                    if 'flavor' in edition:
                        sqlfile.write(',flavor_text')
                    sqlfile.write(') VALUES (' + str(edition['multiverse_id']) + ',"' + card['id'] + '","'
                                       + edition['rarity'] + '","' + edition['artist'] + '",'
                                    '(SELECT set_id FROM sets WHERE set_name="' + edition['set'].replace('"', r'\"') + '")')
                    if 'flavor' in edition:
                        sqlfile.write(',"' + edition['flavor'].replace('"', r'\"').replace('\n', ' ') + '"')

                    sqlfile.write(');\n')


    def add_legalities(self, cards):
        formats = []
        with open('sql/card_legalities.sql', 'w', encoding='utf-8') as sqlfile:
            # card_legality
            sqlfile.write('DROP TABLE card_legality;\n')
            sqlfile.write('CREATE TABLE card_legality ('
                          'card_id VARCHAR(30),'
                          'mtg_format VARCHAR(30),'
                          'legality ENUM(\'legal\',\'restricted\',\'banned\'),'
                          'CONSTRAINT fk_card_legality FOREIGN KEY (card_id) REFERENCES cards(card_id),'
                          'CONSTRAINT fk_format FOREIGN KEY (mtg_format) REFERENCES formats(mtg_format),'
                          'CONSTRAINT pk_card_format PRIMARY KEY (card_id, mtg_format));\n')

            # legalities
            for card in cards:
                if 'formats' in card:
                    for format, legality in card['formats'].items():
                        sqlfile.write('INSERT INTO card_legality(card_id,mtg_format,legality) VALUES ')
                        sqlfile.write('("' + card['id'] + '","' + format + '","' + legality + '");\n')

                        if format not in formats:
                            formats.append(format)

        with open('sql/formats.sql', 'w', encoding='utf-8') as sqlfile:
            sqlfile.write('DROP TABLE formats;\n')
            sqlfile.write('CREATE TABLE formats ('
                          'mtg_format VARCHAR(30) PRIMARY KEY);\n')

            sqlfile.write('INSERT INTO formats(mtg_format) VALUES ')
            for i, format in enumerate(formats):
                if i != 0:
                    sqlfile.write(',')
                sqlfile.write('("' + format + '")')
            sqlfile.write(';\n')

    def add_prices(self, cards, date):

        # prices
        with open('sql/prices_' + date + '.sql', 'w') as sqlfile:
            for card in cards:
                for edition in card['editions']:
                    sqlfile.write('INSERT INTO prices (multiverse_id,date,low_price,average_price,high_price) '
                          'VALUES (' + str(edition['multiverse_id']) + ',' + date + ',' + str(edition['prices']['low']) + ','
                                        + str(edition['prices']['average']) + ',' + str(edition['prices']['high']) + ');\n')