class Star:
    _stars_by_id = {}

    @classmethod
    def register(cls, star):
        cls._stars_by_id[star.id] = star

    @classmethod
    def get(cls, star_id):
        return cls._stars_by_id.get(star_id)

    def __init__(self, data, register=True):
        self.id = data['uid']
        self.visible = bool(data['v'])

        # TODO: Set to player object instead of PUID
        self.owning_player = data['puid']

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