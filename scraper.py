import requests
import re
import time

class WebScraper:

    def __init__(self, base_url, exclude):
        self.base_url = base_url
        self.set_dict = {"ODY": "OD", "PCY": "PR", "WTH": "WL", "TMP": "TE", "ULG": "UL", "USG": "UZ", "INV": "IN",
                         "7ED": "7E", "MIR": "MI", "UDS": "UD", "NMS": "NE", "STH": "ST", "MMQ": "MM", "APC": "AP",
                         "EXO": "EX", "MPS": "MS2", "MPS_AKH": "MS3", "FRF_UGIN": "PRM-UGF", "HOP": "PC1", "VIS": "VI",
                         "PLS": "PS", "pMEI": "PRM-MED", "DD3_GVL": "DDD", "DD3_DVD": "DDC", "DD3_EVG": "EVG"}

        self.a_printings = [3011, 3040, 3159, 2985, 2988, 2992, 2994, 3097, 3043, 3099, 3013, 3162, 3101, 2963, 3190,
                            2913, 2939, 3129, 2916, 3000, 3132, 3169, 3192, 3105, 2918, 3073, 3075, 2967, 3018, 3135,
                            2942, 3138, 3140, 3142, 3173, 3175, 2969, 3198, 3201, 2946, 3110, 3082, 3203, 2949, 3021,
                            3205, 3085, 3087, 3053, 2954, 3207, 3209, 3212, 3025, 2929, 2979, 3090, 3114, 3116, 3059,
                            3061, 3092, 3119, 3183, 3095, 3149, 2932, 3032, 3152, 3185, 3188, 3125, 3154, 3219, 2982,
                            3156, 1842, 1937, 1970, 1944, 1904, 1909, 1912, 1975, 1947, 1951, 1955, 1872, 1875, 1881,
                            1849, 1981, 1985, 1989, 1994, 1853, 1884, 1856, 1071, 1859, 1917, 1961, 1939, 2000, 1862,
                            1920, 1076, 1924, 1933, 1891, 2888, 1080, 2892, 1084, 2896, 1088, 1896, 1899, 3164, 3108]

        self.b_printings = [x + 1 for x in self.a_printings]

        # brothers yamazi
        self.a_printings.append(78968)
        self.b_printings.append(85106)

        self.online_only = ['MED', 'ME2', 'ME3', 'ME4', 'VMA', 'TPR', 'VAN']
        self.split_cards = {"Alive": "Well", "Appeal": "Authority", "Armed": "Dangerous", "Far": "Away", "Beck": "Call",
                            "Reason": "Believe", "Flesh": "Blood", "Boom": "Bust", "Bound": "Determined", "Wear": "Tear",
                            "Breaking": "Entering", "Catch": "Release", "Leave": "Chance", "Order": "Chaos",
                            "Claim": "Fame", "Commit": "Memory", "Failure": "Comply", "Consign": "Oblivion",
                            "Refuse": "Cooperate", "Turn": "Burn", "Crime": "Punishment", "Cut": "Ribbons",
                            "Dawn": "Dusk", "Life": "Death", "Supply": "Demand", "Driven": "Despair", "Destined": "Lead",
                            "Research": "Development", "Down": "Dirty", "Heaven": "Earth", "Odds": "Ends", "Rise": "Fall",
                            "Feast": "Famine", "Farm": "Market", "Mouth": "Feed", "Prepare": "Fight", "Start": "Finish",
                            "Fire": "Ice", "Give": "Take", "Grind": "Dust", "Hide": "Seek", "Hit": "Run",
                            "Insult": "Injury", "Profit": "Loss", "Spite": "Malice", "Spring": "Mind", "Rags": "Riches",
                            "Never": "Return", "Pain": "Suffering", "Protect": "Serve", "Pure": "Simple", "Wax": "Wane",
                            "Reduce": "Rubble", "Ready": "Willing", "Rough": "Tumble", "Stand": "Deliver",
                            "Struggle": "Survive", "Toil": "Trouble", "Trial": "Error", "Onward": "Victory",
                            "Illusion": "Reality", "Night": "Day", "Assault": "Battery", "Dead": "Gone"}

        self.split_cards_reverse = {}
        self.double_faced = {"Archdemon of Greed": "Ravenous Demon", "Autumn-Tail, Kitsune Sage": "Kitsune Mystic",
                             "Azamuki, Treachery Incarnate": "Cunning Bandit", "Bane of Hanweir": "Hanweir Watchkeep",
                             "Chalice of Death": "Chalice of Life", "Erayo's Essence": "Erayo, Soratami Ascendant",
                             "Garruk, the Veil-Cursed": "Garruk Relentless", "Gatstaf Howler": "Gatstaf Shepherd",
                             "Ghastly Haunting": "Soul Seizer", "Goka the Unjust": "Initiate of Blood",
                             "Homicidal Brute": "Civilized Scholar", "Homura's Essence": "Homura, Human Ascendant",
                             "Howlpack Alpha": "Mayor of Avabruck", "Howlpack of Estwald": "Villagers of Estwald",
                             "Insectile Aberration": "Delver of Secrets", "Ironfang": "Village Ironsmith",
                             "Kaiso, Memory of Loyalty": "Faithful Squire", "Krallenhorde Killer": "Wolfbitten Captive",
                             "Krallenhorde Wantons": "Grizzled Outcasts", "Kuon's Essence": "Kuon, Ogre Ascendant",
                             "Ludevic's Abomination": "Ludevic's Test Subject", "Lord of Lineage": "Bloodline Keeper",
                             "Markov's Servant": "Chosen of Markov", "Merciless Predator": "Reckless Waif",
                             "Moonscarred Werewolf": "Scorned Villager", "Nighteyes the Desecrator": "Nezumi Graverobber",
                             "Nightfall Predator": "Daybreak Ranger", "Rampaging Werewolf": "Tormented Pariah",
                             "Ravager of the Fells": "Huntmaster of the Fells", "Rune-Tail's Essence": "Rune-Tail, Kitsune Ascendant",
                             "Sasaya's Essence": "Sasaya, Orochi Ascendant", "Silverpelt Werewolf": "Lambholt Elder",
                             "Stalking Vampire": "Screeching Bat", "Terror of Kruin Pass": "Kruin Outlaw",
                             "Thraben Militia": "Thraben Sentry", "Tobita, Master of Winds": "Student of Elements",
                             "Tomoya the Revealer": "Jushi Apprentice", "Ulvenwald Primordials": "Ulvenwald Mystics",
                             "Unholy Fiend": "Cloistered Youth", "Werewolf Ransacker": "Afflicted Deserter",
                             "Wildblood Pack": "Instigator Gang", "Withengar Unbound": "Elbrus, the Binding Blade",
                             "Hinterland Scourge": "Hinterland Hermit", "Tovolar's Magehunter": "Mondronen Shaman",
                             "Unhallowed Cathar": "Loyal Cathar", }

        for key, val in self.split_cards.items():
            self.split_cards_reverse[val] = key

        self.exclude_ids = exclude.union({184585, 198073, 423590, 382835, 397564, 233299, 201098, 184599, 409653,
                                          417495, 417494, 401718, 401719, 401720, 417497, 25510, 25502, 386322,
                                          409654, 10490, 394383, 25540, 10713, 401722, 417498, 25529, 394407, 25543,
                                          409655, 25504, 25515, 409656, 417496, 401721, 25526, 423583, 423584, 423585,
                                          97050, 423586, 423587, 423588, 423589})

    def fix_set_id(self, set_id):
        if set_id in self.set_dict.keys():
            return self.set_dict[set_id]
        else:
            return set_id

    def fix_split_card(self, card_name):
        if card_name in self.split_cards.keys():
            return card_name + " %2F%2F " + self.split_cards[card_name]
        elif card_name in self.split_cards_reverse.keys():
            return self.split_cards_reverse[card_name] + " %2F%2f " + card_name
        elif card_name in self.double_faced.keys():
            return self.double_faced[card_name]
        else:
            return card_name

    def fix_card_name(self, card_name, multiverse_id):
        # split cards - awkward
        fixed = self.fix_split_card(card_name)
        fixed = fixed.replace(' ', '+')
        fixed = fixed.replace(':.', '')

        # Cards with two arts (A and B printings)
        if multiverse_id in self.a_printings:
            fixed += '+<A>'
        if multiverse_id in self.b_printings:
            fixed += '+<B>'

        return fixed

    def download_csv(self, cards):
        payload = {
            'commit': 'Log+In',
            'auth_key': 'rtullybarr@gmail.com',
            'password': 'Yz405&lHr#m!bYd&'
        }

        failed_urls = []

        with requests.session() as c:

            c.post('https://www.mtggoldfish.com/auth/identity/callback', data=payload)

            for card in cards:
                # skip schemes
                if "scheme" in card['types'] or "conspiracy" in card['types'] or "plane" in card['types']:
                    continue

                # duplicates of cards with the 'AE' / 'ae' character
                if 'Æ' in card['name'] or 'æ' in card['name']:
                    continue

                for edition in card['editions']:
                    # skip printings with multiverse_id = 0
                    if edition['multiverse_id'] == 0 or edition['multiverse_id'] in self.exclude_ids:
                        continue

                    if edition['set_id'] in self.online_only:
                        continue

                    card_name = self.fix_card_name(card['name'], edition['multiverse_id'])
                    set_id = edition['set_id']
                    set_id = self.fix_set_id(set_id)

                    term = requests.utils.quote(card_name + '+[' + set_id + ']')

                    url = self.base_url + term

                    response = c.get(url)
                    print(response.url)

                    if response.status_code != 200:
                        print('Failed to get prices.')
                        failed_urls.append(url)
                    elif len(response.content) > 0:
                        with open("prices_3.csv", 'a') as f:
                            for line in response.iter_lines():
                                line = line.decode("utf-8")
                                # add multiverse_id
                                f.write(str(edition["multiverse_id"]))
                                f.write(",")
                                f.write(line)
                                f.write("\n")
                    else:
                        with open("failed_cards.csv", 'a') as f:
                            f.write(str(edition["multiverse_id"]) + "," + edition["set_id"] + "," + card_name + "\n")
                        failed_urls.append(url)

                    time.sleep(1)

    def scrape_all(self, cards):

        prices = []
        not_found = []
        for card in cards:
            # make sure set and card name are in the right format
            for edition in card['editions']:
                price, url = self.scrape(edition['set'], card['name'])
                if price:
                    prices.append({'multiverse_id': edition['multiverse_id'], 'price': price})
                else:
                    not_found += url

        return prices, not_found

    def scrape(self, set, card):
        set = set.replace(' ', '+')
        card = card.replace(' ', '+')

        set = set.replace(':.', '')
        card = card.replace(':.', '')

        # exceptions
        if set == "Celebration":
            set = "Special+Occasion"

        print(set)
        print(card)

        # match
        match = "<div class='price-box-type'>PAPER</div>\s+<div class='price-box-price'>([0-9]+\.[0-9]+)</div>"
        response = requests.get(self.base_url + set + '/' + card + '#paper')
        print(response.url)
        #print(response.text)
        matches = re.findall(match, response.text)

        # expect single match
        if len(matches) > 1:
            print("Warning: matched more than one price.")
            return None, response.url
        elif len(matches) < 1:
            print("Warning: price not found on page.")
            return None, response.url
        else:
            # float
            price = float(matches[0])
            return price, None