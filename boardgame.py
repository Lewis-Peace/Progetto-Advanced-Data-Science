import re

class boardgame:

    def __init__(self, id: int, title: str) -> None:
        self.id = id
        self.title = re.sub(r'[^a-zA-Z0-9.!?]+', ' ', title)
        pass
    
    def set_rating(self, rating: float):
        self.rating = rating
        return self
    
    def set_publishers(self, publishers: list[str]):
        self.publishers = re.sub(r'[^a-zA-Z0-9.!?]+', ' ','. '.join(publishers))
        return self
        
    def set_artists(self, artists: list[str]):
        self.artists = re.sub(r'[^a-zA-Z0-9.!?]+', ' ','. '.join(artists))
        return self
    
    def set_designer(self, designer: list[str]):
        self.designer = re.sub(r'[^a-zA-Z0-9.!?]+', ' ','. '.join(designer))
        return self
        
    def set_mechanics(self, mechanics: list[str]):
        self.mechanics = re.sub(r'[^a-zA-Z0-9.!?]+', ' ','. '.join(mechanics))
        return self
        
    def set_category(self, category: list[str]):
        self.category = re.sub(r'[^a-zA-Z0-9.!?]+', ' ','. '.join(category))
        return self
        
    def set_min_players(self, min_players: int):
        self.min_players = min_players
        return self
        
    def set_max_players(self, max_players: int):
        self.max_players = max_players
        return self
        
    def set_year_of_publishing(self, year_of_publishing: int):
        self.year_of_publishing = year_of_publishing
        return self

    def set_owned(self, owned: int):
        self.owned = owned
        return self

    def set_wanting(self, wanting: int):
        self.wanting = wanting
        return self

    def set_trading(self, trading: int):
        self.trading = trading
        return self

    def set_wishing(self, wishing: int):
        self.wishing = wishing
        return self
    
    def set_description(self, description: int):
        self.description = re.sub(r"[^a-zA-Z0-9?!.]+", ' ', description)
        return self
    
    def csvize(self):
        entryes = [self.id, self.title, self.description, self.rating, self.min_players, self.max_players,
                   self.year_of_publishing, self.artists, self.category, self.designer, self.mechanics,
                   self.publishers, self.owned, self.wanting, self.trading, self.wishing]
        return ', '.join(entryes)
            
        
    def __str__(self):
        return self.title + ' ' + self.id
