import fgarcade as ge
from arcade import SpriteList, Sprite
from fgarcade.assets import get_sprite_path 
from random import randint
import arcade


class Game(ge.Platformer):
    """
    Simple game my_level
    """

    title = 'Candy Shop'
    player_initial_tile = 4, 1
    final = 80
    world_theme = 'green'
    player_theme = 'grey'
    #background_theme = 'brown'

    def init_world(self):
        # Inicio, Fim e chão
        self.create_tower(10, 2, coords=(0, 1))
        self.create_arrow('right', (3, 1))
        self.create_ground(self.final, coords=(0, 0), smooth_ends=True)
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

        self.create_platform(3, coords=(33, 3))

        self.create_tower(2, 3, coords=(42, 1))
        self.create_fence('left', (42, 3))
        self.create_fence('right', (43, 3))
        self.create_tower(2, 3, coords=(46, 1))
        self.create_fence('left', (47, 3))
        self.create_fence('left', (48, 3))
        self.create_tower(5, 3, coords=(44, 1))

        self.create_platform(3, coords=(52, 5))

        self.create_platform(3, coords=(57, 3))        

        self.create_tower(2, 3, coords=(65, 1))
        self.create_tower(5, 3, coords=(63, 1))
        
            
        # Spikes 
        self.spike = self.create_object('other/spikes/spikes-high', (20, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (17, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (18, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (19, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (21, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (22, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (23, 1))
        
        
        self.spike = self.create_object('other/spikes/spikes-high', (40, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (41, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (39, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (38, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (37, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (36, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (35, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (34, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (33, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (32, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (31, 1))
        self.spike = self.create_object('other/spikes/spikes-low', (30, 1))
        self.spike = self.create_object('other/spikes/spikes-high', (29, 1))

        self.spike = self.create_object('other/spikes/spikes-high', (53, 6))

        self.spike = self.create_object('other/spikes/spikes-high', (58, 4))

        self.background_near = SpriteList(use_spatial_hash=False)
        self.background_fixed = SpriteList(use_spatial_hash=False)
        self.background_fixed.append(Sprite(get_sprite_path('background/bg1')))

    def init_enemies(self):
        self.enemies = SpriteList(is_static=True)
        enemy = self.create_object('enemy/enemyFloating_1', (10, 5), at=self.enemies)
        self.enemies.append(enemy)

    def init_items(self):
<<<<<<< HEAD
        self.coins = SpriteList()
        def add_coin(pos):
            coin = self.create_object('other/items/yellowGem', pos, at=self.coins)
            self.coins.append(coin)
=======

        #Coins
        self.items = SpriteList()
        self.item = self.create_object('other/items/greenCrystal', (1, 11), at=self.items)
>>>>>>> a5086164275cee7c8e25ecefa6e92fed2ea7e18e

        for pt in [(6, 4), (7, 4), (8, 4), (9, 7), (10, 7), (11, 7),
                   (12, 3), (13, 3), (14, 5), (15, 5), (16, 5), (12, 10),
                   (13,10), (14,10), (20, 10), (21, 10), (22, 10), (24, 3),
                   (25, 3)]:
            add_coin(pt)

        self.item = self.create_object('other/items/yellowGem', (44, 6), at=self.items)
        self.item = self.create_object('other/items/yellowGem', (45, 6), at=self.items)
        self.item = self.create_object('other/items/yellowGem', (46, 6), at=self.items)

        self.item = self.create_object('other/items/yellowGem', (52, 6), at=self.items)
        self.item = self.create_object('other/items/yellowGem', (54, 6), at=self.items)

        self.item = self.create_object('other/items/yellowGem', (57, 4), at=self.items)
        self.item = self.create_object('other/items/yellowGem', (59, 4), at=self.items)

        self.item = self.create_object('other/items/yellowGem', (63, 6), at=self.items)
        self.item = self.create_object('other/items/yellowGem', (64, 6), at=self.items)
        self.item = self.create_object('other/items/yellowGem', (65, 6), at=self.items)
        
        self.item = self.create_object('other/items/yellowGem', (66, 3), at=self.items)
        self.item = self.create_object('other/items/yellowGem', (67, 3), at=self.items)

    def init(self):
        self.init_world()
        self.init_items()
        self.init_enemies()
        self.score_coins = int(0)

    def collide_coins(self, dt):
        self.coins.update()

        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coins)

        i = 0
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            i += 1
            if i == 2:
                self.score_coins += 1
                i = 0

    def collide_enemies(self, dt):
        pass

    def on_update(self, dt):
        super().on_update(dt)
        self.collide_coins(dt)
        self.collide_enemies(dt)
    
    def draw_elements(self):
        super().draw_elements()
        self.enemies.draw()
        self.coins.draw()

        output = f"Score: {self.score_coins}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 20)


if __name__ == "__main__":
<<<<<<< HEAD
    Game().run()
=======
    Game().run() 
    
>>>>>>> a5086164275cee7c8e25ecefa6e92fed2ea7e18e
