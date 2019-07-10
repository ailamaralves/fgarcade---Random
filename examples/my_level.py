import fgarcade as ge
from arcade import SpriteList, Sprite
from fgarcade.assets import get_sprite_path 
from random import randint
import arcade
from time import sleep
from fgarcade.enums import Role


class Game(ge.Platformer):
    """
    Simple game my_level
    """

    final = 90
    SCORE = 2
    viewport_margin_horizontal = 500
    viewport_margin_vertical = 120
    LIMIT = 3
   
    def init_world(self):

        # Inicio e chão
        self.create_tower(10, 2, coords=(0, 1))
        self.create_ground(self.final, coords=(0, 0), smooth_ends=True)

        # Plataforma para fazer a camera acompanhar o jogador em qualquer altura
        self.create_platform(1, coords=(20, 90))

        # Cenário
        self.moving_platform_list = SpriteList()
        platform = self.create_object('tile/blue/gl', (34, 3), at=self.moving_platform_list, role=Role.OBJECT)
        platform = self.create_object('tile/blue/g', (35, 3), at=self.moving_platform_list, role=Role.OBJECT)
        platform = self.create_object('tile/blue/gr', (36, 3), at=self.moving_platform_list, role=Role.OBJECT)

        def create_spike(tam, x, y):
            for i in range(tam):
                spike = self.create_object('other/spikes/spikes-high', (x, y), at=self.spikes)
                # self.spikes.append(spike)
                x += 1
        
        self.discs = SpriteList()        

        def create_disc(x, y):
             disc = self.create_object('other/items/discGreen', (x, y), at=self.discs)
        
        def create_door_key(x, y):
            doorkey = self.create_object('other/door/doorRed_lock', (x, y), at=self.doorkey)

        def create_door_top(x, y):
            doortop = self.create_object('other/door/doorRed_top', (x, y), at=self.doortop)

        for pt in [(3, (6, 3)), (3, (9,6)), (3, (12, 9)),
                   (3, (20, 9)), (1, (20, 3)), (3, (62, 5)), 
                   (3, (67, 3))]:
            s, l = pt
            self.create_platform(s, l)

        for pt in [(2, 3, (12, 1)), (4, 3, (14, 1)), (2, 3, (24, 1)),
                   (4, 3, (26, 1)), (2, 3, (52, 1)), (2, 3, (56, 1)),
                   (5, 3, (54, 1)), (2, 3, (75, 1)), (5, 3, (73, 1)), (7, 3, (87, 1))]:
            x, y, w = pt
            self.create_tower(x, y, w)

        # Final tower
        self.create_tower(10, coords=(self.final - 1, 1))

        # Spikes
        self.spikes = SpriteList()

        create_spike(7, 17, 1)
        create_spike(23, 29, 1)
        create_spike(14, 59, 1)

        # Discs
        create_disc(8, 7)
        create_disc(11, 10)
        create_disc(20, 4)
        create_disc(86, 2)
        create_disc(86, 4)
        create_disc(86, 6)

        # Door key
        self.doorkey = SpriteList()  
        create_door_key(88, 8)

        # Door top
        self.doortop = SpriteList()
        create_door_top(88, 9)

        # Foreground
        self.create_arrow('right', (3, 1))
        self.create_fence('left', (52, 3))
        self.create_fence('right', (53, 3))
        self.create_fence('left', (57, 3))
        self.create_fence('left', (58, 3))
        self.create_fence('left', (58, 3))
        self.create_fence('left', (76, 3))
        self.create_fence('right', (77, 3))

        # Background
        self.background_near = SpriteList(use_spatial_hash=False)
        self.background_fixed = SpriteList(use_spatial_hash=False)
        self.background_fixed.append(Sprite(get_sprite_path('background/bg1')))

    def init_enemies(self):
        self.enemies = SpriteList(is_static=True)
        self.enemies_moving_list = SpriteList(is_static=False)

        def create_enemy(x, y, condition):
            if condition:
                enemy = self.create_object('enemy/enemySwimming_1', (x, y), at=self.enemies_moving_list)
                # self.enemies_moving_list.append(enemy)
            else:
                enemy = self.create_object('enemy/enemyFloating_1', (x, y), at=self.enemies)
                # self.enemies.append(enemy)

        create_enemy(10, 7, True)
        create_enemy(21, 10, False)
        create_enemy(34, 4, False)
        create_enemy(40, 4, False)
        create_enemy(46, 4, False)
        create_enemy(72, 6, False)

    def init_items(self):
        self.coins = SpriteList()

        def create_coin(x, y, *args):
            if args:
                for i in range(args[0]):
                    coin = self.create_object('other/items/yellowGem', (x, y), at=self.coins)
                    self.coins.append(coin)
                    x += 1
            else:
                coin = self.create_object('other/items/yellowGem', (x, y), at=self.coins)
                self.coins.append(coin)

        #Coins
        create_coin(6, 4, 3)
        create_coin(9, 7, 3)
        create_coin(12, 3, 2)
        create_coin(14, 5, 3)
        create_coin(12, 10, 3)
        create_coin(20, 10, 3)
        create_coin(24, 3, 2)
        create_coin(26, 5, 3)
        create_coin(33, 4, 3)
        create_coin(39, 4, 3)
        create_coin(45, 4, 3)
        create_coin(54, 6, 3)
        create_coin(78, 1, 3)
        create_coin(81, 1, 3)
        create_coin(84, 1, 3)

        self.items = SpriteList()

    def init(self):
        self.init_world()
        self.init_items()
        self.init_enemies()
        self.limit_of_platforms()
        self.score_coins = int(0)
        self.cont = int(0)
        self.player_life = int(4)
        self.move = int(2)

    def collide_coins(self, dt):
        self.coins.update()
        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coins)
        i = 0
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            i += 1
            if i == self.SCORE:
                self.score_coins += 10
                i = 0

    def collide_spikes(self, dt):
        self.spikes.update()
        spikes_hit_list = arcade.check_for_collision_with_list(self.player, self.spikes)
    
        for spike in spikes_hit_list:
            self.cont += 1
            self.player_die()

    def collide_enemies(self, dt):
        self.enemies.update()
        enemies_hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)
        moving_enemies_hit_list = arcade.check_for_collision_with_list(self.player, self.enemies_moving_list)

        for enemie in enemies_hit_list:
            self.cont += 1
            self.player_die()

        for enemie in moving_enemies_hit_list:
            self.cont += 1
            self.player_die()

    def collide_discs(self, dt):
        self.discs.update()
        discs_hit_list = arcade.check_for_collision_with_list(self.player, self.discs)

        for disc in discs_hit_list:
            disc.remove_from_sprite_lists()
            self.player.jump += 50

    def player_die(self):
        if self.cont == self.SCORE:
          sleep(0.5)
          super().player.player_initial_tile = 4, 1
          del self.physics_engine
          self.init_items()
          self.init_enemies()
          self.init_world()
          self.score_coins = 0
          self.player_life -= 1
          self.cont = 0

    def game_over(self, dt):
        pass

    def can_move(self, name, collision):
        check_hit = []

        for limit in name:
            hit = arcade.check_for_collision_with_list(limit, collision)
            check_hit.append(hit)

        for hit in check_hit:
            if hit:
                return True
        return False
        
    def move_platforms(self, dt):
        check = self.can_move(self.limit_of_moving, self.moving_platform_list)
        cont = 3

        for platform in self.moving_platform_list:
            if check and cont == self.LIMIT:
                self.move *= (-1)
                cont = 0
            platform.center_x += self.move
        cont = 3

    def move_enemies(self, dt):
        for enemie in self.enemies_moving_list:
            enemie.center_x += 2

    def on_update(self, dt):
        super().on_update(dt)
        self.collide_coins(dt)
        #self.collide_spikes(dt)
        self.collide_enemies(dt)
        self.move_enemies(dt)
        self.collide_discs(dt)
        self.move_platforms(dt)
        self.game_over(dt)
            
    def draw_elements(self):
        super().draw_elements()
        self.enemies.draw()
        self.coins.draw()
        self.spikes.draw()
        self.enemies_moving_list.draw()
        self.moving_platform_list.draw()
        self.discs.draw()
        self.doorkey.draw()
        self.doortop.draw()
     
        #Placar de Contagem das moedas e vidas
        output_score = f"Score: {self.score_coins} ||"
        output_life = f"Life: {self.player_life}"
        arcade.draw_text(output_score, self.viewport_horizontal_start, self.viewport_vertical_start + 20, arcade.color.BLACK, 20)
        arcade.draw_text(output_life, self.viewport_horizontal_start + 200, self.viewport_vertical_start + 20, arcade.color.BLACK, 20)

if __name__ == "__main__":
    Game().run()
