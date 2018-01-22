import requests
import json


class MTGLoader:

    def __init__(self, api_url):
        self.api_url = api_url

    def get_mtg_data(self, kind, bypass_cache=False):

        if bypass_cache:
            return self.get_data_from_api(kind)
        else:
            try:
                with open(kind + '.json', 'r') as json_file:
                    return json.load(json_file)

            except FileNotFoundError:
                return self.get_data_from_api(kind)

    def get_data_from_api(self, kind):

        next_url = self.api_url + kind
        data = []
        done = False

        while not done:
            response = requests.get(next_url)

            if response.status_code != 200:
                print(response.status_code)
                raise IOError

            current_data = response.json()

            if 'sets' in current_data:
                print(current_data)
                current_data = current_data['sets']

            print(current_data)
            data += current_data

            # get next link, if it exists
            if 'next' in response.links:
                next_url = response.links['next']['url']
            else:
                done = True

            if len(current_data) < 100:
                done = True

        # Store to avoid future calls to the API
        with open(kind + '.json', 'w') as json_file:
            json.dump(data, json_file)

        return data

if __name__ == "__main__":
    # test api using link rel
    loader = MTGLoader('https://api.deckbrew.com/mtg/')
