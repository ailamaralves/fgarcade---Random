import fgarcade as ge
from arcade import SpriteList, Sprite
from fgarcade.assets import get_sprite_path 
from random import randint
import arcade


class Game(ge.Platformer):
    """
    Simple game my_level
    """

    final = 90

    def init_world(self):
        # Inicio, Fim e chão
        self.create_tower(10, 2, coords=(0, 1))
        self.create_ground(self.final, coords=(0, 0), smooth_ends=True)
        self.create_tower(10, coords=(self.final - 1, 1))

        # Plataforma para fazer a camera acompanhar o jogador em qualquer altura
        self.create_platform(1, coords=(20, 90))

        # Cenário
        def add_platform(size, cords):
            self.create_platform(size, coords=cords)

        def add_tower(x, y, cords):
            self.create_tower(x, y, coords=cords)

        for pt in [(3, (6, 3)), (3, (9,6)), (3, (12, 9)),
                   (3, (20, 9)), (1, (20, 3)), (3, (33, 3)),
                   (3, (62, 5)), (3, (67, 3))]:
            s, l = pt
            add_platform(s, l)

        for pt in [(2, 3, (12, 1)), (4, 3, (14, 1)), (2, 3, (24, 1)),
                   (4, 3, (26, 1)), (2, 3, (52, 1)), (2, 3, (56, 1)),
                   (5, 3, (54, 1)), (2, 3, (75, 1)), (5, 3, (73, 1))]:
            x, y, w = pt
            add_tower(x, y, w)

        # Spikes
        # Função para criar os espinhos. Ela recebe 3 argumentos: o "comprimento" dos espinhos, o X inicial e o Y
        self.spikes = SpriteList()
        self.create_spike(7, 17, 1)
        self.create_spike(23, 29, 1)
        self.create_spike(14, 59, 1)

        # Foreground
        self.create_arrow('right', (3, 1))
        self.create_fence('left', (52, 3))
        self.create_fence('right', (53, 3))
        self.create_fence('left', (57, 3))
        self.create_fence('left', (58, 3))

        # Background
        self.background_near = SpriteList(use_spatial_hash=False)
        self.background_fixed = SpriteList(use_spatial_hash=False)
        self.background_fixed.append(Sprite(get_sprite_path('background/bg1')))

    def init_enemies(self):
        self.enemies = SpriteList(is_static=True)

        # Função para criar os inimigos dado as coordenadas X e Y
        self.create_enemy(10, 7)
        self.create_enemy(21, 10)
        self.create_enemy(34, 4)
        self.create_enemy(40, 4)
        self.create_enemy(46, 4)
        self.create_enemy(72, 6)

    def init_items(self):
        self.coins = SpriteList()

        # Função para criar as moedas. Ela recebe 3 argumentos:
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
        self.player_life = int(4)
        self.cont = int(0)

    def collide_coins(self, dt):
        self.coins.update()
        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coins)
        i = 0
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            i += 1
            if i == 2:
                self.score_coins += 10
                i = 0

    def collide_spikes(self, dt):
        self.spikes.update()
        spikes_hit_list = arcade.check_for_collision_with_list(self.player, self.spikes)

        for spike in spikes_hit_list:
            self.cont += 1
            self.player_die(dt)

    def collide_enemies(self, dt):
        self.enemies.update()
        enemies_hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)

        for enemie in enemies_hit_list:
            self.cont += 1
            self.player_die(dt)

    # Função para quando o player morrer
    # É chamada quando o player colide com um espinho ou um inimigo
    def player_die(self, dt):
        if self.cont == 2:
            arcade.pause(0.5)
            super().player.player_initial_tile = 4, 1
            self.player_life -= 1
            self.cont = 0

    def game_over(self, dt):
        pass

    def on_update(self, dt):
        super().on_update(dt)
        self.collide_coins(dt)
        self.collide_spikes(dt)
        self.collide_enemies(dt)
        self.game_over(dt)
            
    def draw_elements(self):
        super().draw_elements()
        self.enemies.draw()
        self.coins.draw()

        #Placar de Contagem das moedas
        output_score = f"Score: {self.score_coins} ||"
        output_life = f"Life: {self.player_life}"
        arcade.draw_text(output_score, 10, 20, arcade.color.BLACK, 20)
        arcade.draw_text(output_life, 200, 20, arcade.color.BLACK, 20)
        arcade.draw_text(output_score, 1850, 20, arcade.color.BLACK, 20)
        arcade.draw_text(output_life, 2040, 20, arcade.color.BLACK, 20)
        arcade.draw_text(output_score, 3700, 20, arcade.color.BLACK, 20)
        arcade.draw_text(output_life, 3890, 20, arcade.color.BLACK, 20)
        arcade.draw_text(f"Score: {self.score_coins}", 5550, 980, arcade.color.BLACK, 20)
        arcade.draw_text(output_life, 5550, 940, arcade.color.BLACK, 20)


if __name__ == "__main__":
    Game().run()
