import fgarcade as ge
from arcade import SpriteList, Sprite
from fgarcade.assets import get_sprite_path 
from random import randint
import arcade


class Game(ge.Platformer):
    """
    Simple game my_level
    """

    final = 80

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
        self.spikes = SpriteList()
        # Criei uma função para criar os espinhos. Ela recebe 3 argumentos: o "comprimento" dos espinhos, o X inicial e o Y
        self.create_spike(7, 17, 1)
        self.create_spike(13, 29, 1)
        self.create_spike(14, 49, 1)

        self.background_near = SpriteList(use_spatial_hash=False)
        self.background_fixed = SpriteList(use_spatial_hash=False)
        self.background_fixed.append(Sprite(get_sprite_path('background/bg1')))

    def init_enemies(self):
        self.enemies = SpriteList(is_static=True)
        enemy = self.create_object('enemy/enemyFloating_1', (10, 5), at=self.enemies)
        self.enemies.append(enemy)

    def init_items(self):
        self.coins = SpriteList()
        # Criei uma função para criar as moedas. Ela recebe 3 argumentos:
        # o X, o Y e, caso precise, para plataformas, etc..., a quantidade de moedas

        #Coins
        self.items = SpriteList()
        self.create_coin(6, 4, 3)
        self.create_coin(9, 7, 3)
        self.create_coin(12, 3, 2)
        self.create_coin(14, 5, 3)
        self.create_coin(12, 10, 3)
        self.create_coin(20, 10, 3)
        self.create_coin(24, 3, 2)

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

    def collide_spikes(self, dt):
        self.spikes.update()
        spikes_hit_list = arcade.check_for_collision_with_list(self.player, self.spikes)
        for spike in spikes_hit_list:
            self.player_die()

    def collide_enemies(self, dt):
        pass

    # Função para quando o player morrer
    # É chamada quando o player colide com um espinho ou um inimigo
    def player_die(self):
        pass

    def on_update(self, dt):
        super().on_update(dt)
        self.collide_coins(dt)
        self.collide_spikes(dt)
        self.collide_enemies(dt)
            
    def draw_elements(self):
        super().draw_elements()
        self.enemies.draw()
        self.coins.draw()

        output = f"Score: {self.score_coins}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 20)


if __name__ == "__main__":
    Game().run()
