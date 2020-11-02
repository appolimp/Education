import requests
import json


class Asteroid:

    BASE_API_URL = 'https://api.nasa.gov/neo/rest/v1/neo/{}'
    params = {'api_key': 'XHL3o0M2IqQz65E2p9yvLNKbyxkHu25FAiZEUGk8'}

    def __init__(self, spd_id):
        self.api_url = self.BASE_API_URL.format(spd_id)

    def get_data(self):
        return requests.get(self.api_url, params=self.params).json()

    @property
    def name(self):
        return self.get_data()['name']

    @property
    def diameter(self):
        return int(self.get_data()['estimated_diameter']['meters']['estimated_diameter_max'])


def main():
    apophis = Asteroid(2099942)
    print(f'Name: {apophis.name}')
    print(f'Diameter: {apophis.diameter}m')
    with open('apothis_fixture.txt', 'w') as f:
        json.dump(apophis.get_data(), f, indent=4)


if __name__ == '__main__':
    main()
