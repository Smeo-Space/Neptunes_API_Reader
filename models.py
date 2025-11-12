from __future__ import annotations
from copy import deepcopy


class Star:
    _stars_by_id = {}

    @classmethod
    def register(cls, star):
        cls._stars_by_id[star.id] = star

    @classmethod
    def get(cls, star_id) -> Star:
        return cls._stars_by_id.get(star_id)

    @classmethod
    def get_all(cls) -> dict[Star]:
        return deepcopy(cls._stars_by_id)

    def __init__(self, data, register=True):
        self.id = data['uid']
        self.visible = bool(data['v'])
        self._owning_player_id = data['puid']

        self.name = data['n']
        self.x = data['x']
        self.y = data['y']

        self.ships_stationed = data.get('st')
        self.experience = data.get('exp')
        self.resources = data.get('r')

        self.economy = data.get('s')
        self.industry = data.get('i')
        self.science = data.get('s')

        self.ship_build_progress = data.get('yard')

        #TODO: nr (resources based off terraforming?), ga

        if register:
            self.__class__.register(self)

    def owning_player(self):
        return Player.get(self._owning_player_id)

class Player:
    _players_by_id = {}

    @classmethod
    def register(cls, player):
        cls._players_by_id[player.id] = player

    @classmethod
    def get(cls, player_id) -> Player:
        return cls._players_by_id.get(player_id)

    @classmethod
    def get_all(cls) -> dict[Player]:
        return deepcopy(cls._players_by_id)

    def __init__(self, data, register=True):
        self.id = data['uid']
        self.name = data['alias']
        self.avatar = data['avatar']
        self.colour = data['color']
        self.shape = data['shape']
        self._home_id = data['home']

        self.total_stars = data['totalStars']
        self.total_fleets = data['totalFleets']
        self.total_ships = data['totalStrength']
        self.total_economy = data['totalEconomy']
        self.total_industry = data['totalIndustry']
        self.total_science = data['totalScience']

        # Attributes of current player
        self.credits = data.get('cash')
        self.ledger = data.get('ledger')
        self.researching = data.get('researching')
        self.researching_next = data.get('researchingNext')

        self.conceded = bool(data['conceded'])
        self.ai = bool(data['ai'])
        self.regard = data['regard']
        self.tech = data['tech'] #TODO: Tech class?

        #TODO: war + countdown_to_war (current player), race, acceptedVassal, offersOfFealty, vassals, karmaToGive, ready, missedTurns

        if register:
            self.__class__.register(self)

    def home(self):
        return Star.get(self._home_id)


class Fleet:
    _fleets_by_id = {}

    @classmethod
    def register(cls, fleet):
        cls._fleets_by_id[fleet.id] = fleet

    @classmethod
    def get(cls, fleet_id) -> Fleet:
        return cls._fleets_by_id.get(fleet_id)

    @classmethod
    def get_all(cls) -> dict[Fleet]:
        return deepcopy(cls._fleets_by_id)

    def __init__(self, data, register=True):
        self.id = data['uid']
        self._owning_player_id = Player.get(data['puid'])

        self.x = data['x']
        self.y = data['y']
        self.lx = data['lx']
        self.ly = data['ly']
        self.exp = data['exp']
        self.speed = data['speed']

        self.ship_count = data['st']

        self.lsuid = data.get('lsuid')
        self.ouid = data['ouid']
        self.action = data['o']
        self.loop = bool(data['l'])

        if register:
            self.__class__.register(self)

    def owning_player(self):
        return Player.get(self._owning_player_id)
