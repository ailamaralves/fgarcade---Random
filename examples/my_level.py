import fgarcade as ge
from arcade import SpriteList, Sprite
from fgarcade.assets import get_sprite_path 


class Game(ge.Platformer):
    """
    Simple platformer example
    """

    title = 'Candy Shop'
    player_initial_tile = 4, 1
    final = 50
    world_theme = 'green'
    player_theme = 'grey'
    #background_theme = 'brown'
    

    def init_world(self):
        # Inicio Fim e chão
        self.create_tower(10, 2, coords=(0, 1))
        self.create_ground(self.final, coords=(0, 0), smooth_ends=False)
        self.create_platform(1, coords=(20, 90))
        self.create_tower(10, coords=(self.final - 1, 1))

        # Cenário
        self.create_platform(3, coords=(6, 3))
        self.create_platform(3, coords=(9, 6))
        self.create_platform(3, coords=(12, 9))

        self.create_tower(2, 3, coords=(12, 1))
        self.create_tower(4, 3, coords=(14, 1))

        self.create_platform(3, coords=(20, 9))

        self.create_tower(2, 3, coords=(24, 1))
        self.create_tower(5, 3, coords=(26, 1))

        self.create_platform(3, coords=(34, 3))

        self.create_tower(2, 3, coords=(42, 1))
        self.create_tower(5, 3, coords=(44, 1))

        self.enemies = SpriteList()
        self.enemy = self.create_object('enemy/enemyFloating_1', (10, 5), at=self.enemies)
        
        self.background_near = SpriteList(use_spatial_hash=False)
        self.background_fixed = SpriteList(use_spatial_hash=False)
        self.background_fixed.append(Sprite(get_sprite_path('background/bg1')))

    def init_enemies(self):
        pass

    def collide_enemies(self):
        pass

    def init_items(self):
        pass

    def init(self):
        self.init_world()
        self.init_items()
        self.init_enemies()
        
    
    def on_draw(self):
        super().on_draw()
        self.enemies.draw()


if __name__ == "__main__":
    Game().run()
