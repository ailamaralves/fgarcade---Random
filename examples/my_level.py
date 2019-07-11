import fgarcade as ge
from arcade import SpriteList, Sprite
from fgarcade.assets import get_sprite_path 
from random import randint
import arcade
from time import sleep
from fgarcade.enums import Role
import pyglet


class Game(ge.Platformer):
    """
    Simple game my_level
    """

    final = 90
    SCORE = 2
    viewport_margin_horizontal = 400
    viewport_margin_vertical = 300
    LIMIT = 3
    cal = False

    # SOUNDS
    # start_sound = pyglet.media.load('examples/sounds/start_sound.mp3')
    coin_sound = arcade.load_sound('examples/sounds/coin.wav')
    jump_sound = arcade.load_sound('examples/sounds/jump.wav')
    disc_sound = arcade.load_sound('examples/sounds/disc.wav')
    death_sound = arcade.load_sound('examples/sounds/death.wav')

    level_sound = pyglet.media.Player()
    level_sound.loop = True
    # level_sound.queue(start_sound)

    def init_world(self):

        self.level_sound.play()

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
                   (3, (67, 3)), (3, (30, 6))]:
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
        create_disc(31, 5)
        create_disc(21, 10)
        create_disc(20, 4)
        create_disc(40, 4)
        create_disc(40, 8)

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

    # Limite da Plataforma que anda
    def limit_of_platforms(self):
        self.limit_of_platform_moving = SpriteList(is_static=True)
        limit = self.create_object('other/block/brown', (30, 3), at=self.limit_of_platform_moving)
        limit = self.create_object('other/block/brown', (50, 3), at=self.limit_of_platform_moving)

    # Limite do inimigo que anda
    def limit_of_enemies(self):
        self.limit_of_enemies_moving_in_x = SpriteList(is_static=True)
        limit = self.create_object('other/block/brown', (30, 7), at=self.limit_of_enemies_moving_in_x)
        limit = self.create_object('other/block/brown', (50, 7), at=self.limit_of_enemies_moving_in_x)

    def limit_enemies(self):
        self.limit_of_enemies_moving_in_y = SpriteList(is_static=True)
        limit = self.create_object('other/block/green', (72, 10), at=self.limit_of_enemies_moving_in_y)
        limit = self.create_object('other/block/green', (72, 2), at=self.limit_of_enemies_moving_in_y)


    def init_enemies(self):
        self.enemies = SpriteList(is_static=True)
        self.moving_enemies_list_in_x = SpriteList(is_static=False)
        self.moving_enemies_list_in_y = SpriteList(is_static=False)

        def create_enemy(x, y, condition, direction_x):
            if condition:
                if direction_x:
                    enemy = self.create_object('enemy/enemySwimming_1', (x, y), at=self.moving_enemies_list_in_x)
                else:
                    enemy = self.create_object('enemy/enemyFlyingAlt_1', (x, y), at=self.moving_enemies_list_in_y)
            else:
                enemy = self.create_object('enemy/enemyFloating_1', (x, y), at=self.enemies)

        # Parâmetro True caso seja um Inimigo que se move
        create_enemy(35, 7, True, True)
        create_enemy(35, 10, True, True)
        create_enemy(35, 8, True, True)
        create_enemy(35, 9, True, True)
        #create_enemy(21, 10, False, False)
        create_enemy(34, 6, True, False)
        #create_enemy(40, 4, False, False)
        create_enemy(46, 6, True, False)
        create_enemy(72, 6, True, False)
        create_enemy(66, 6, True, False)
        create_enemy(18, 6, True, False)
        create_enemy(23, 6, True, False)
        create_enemy(60, 6, True, False)

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
        create_coin(14, 5, 3)
        create_coin(12, 10, 3)
        create_coin(20, 10, 3)
        create_coin(24, 3, 2)
        create_coin(26, 5, 3)
        create_coin(33, 4, 1)
        create_coin(35, 4, 1)
        create_coin(39, 4, 1)
        create_coin(41, 4, 1)
        create_coin(45, 4, 1)
        create_coin(47, 4, 1)
        create_coin(54, 6, 3)
        create_coin(62, 6, 3)
        create_coin(67, 4, 3)
        create_coin(78, 1, 3)
        create_coin(81, 1, 3)
        create_coin(84, 1, 3)

        self.items = SpriteList()

    def init(self):
        self.init_world()
        self.init_items()
        self.init_enemies()
        self.limit_of_platforms()
        self.limit_of_enemies()
        self.limit_enemies()
        self.score_coins = 0
        self.cont = 0
        self.player_life = 4
        self.move_platform = 3
        self.move_enemie = 5
        self.move_enemy = 5

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
            arcade.play_sound(self.coin_sound)

    def collide_spikes(self, dt):
        self.spikes.update()
        spikes_hit_list = arcade.check_for_collision_with_list(self.player, self.spikes)
    
        for spike in spikes_hit_list:
            self.cont += 1
            self.player_die()

    def collide_enemies(self, dt):
        self.enemies.update()
        enemies_hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)
        moving_enemies_in_x_hit_list = arcade.check_for_collision_with_list(self.player, self.moving_enemies_list_in_x)
        moving_enemies_in_y_hit_list = arcade.check_for_collision_with_list(self.player, self.moving_enemies_list_in_y)

        for enemie in enemies_hit_list:
            self.cont += 1
            self.player_die()

        for enemie in moving_enemies_in_x_hit_list:
            self.cont += 1
            self.player_die()

        for enemie in moving_enemies_in_y_hit_list:
            self.cont += 1
            self.player_die()

    def collide_discs(self, dt):
        self.discs.update()
        discs_hit_list = arcade.check_for_collision_with_list(self.player, self.discs)

        for disc in discs_hit_list:
            disc.remove_from_sprite_lists()
            self.player.jump += 50
            arcade.play_sound(self.disc_sound)

    def player_die(self):
        if self.cont == self.SCORE:
          arcade.play_sound(self.death_sound)
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

    def object_can_move(self, name, collision):
        check_hit = []

        for limit in name:
            hit = arcade.check_for_collision_with_list(limit, collision)
            check_hit.append(hit)

        for hit in check_hit:
            if hit:
                return True
        return False
        
    def move_platforms(self, dt):
        check = self.object_can_move(self.limit_of_platform_moving, self.moving_platform_list)
        cont = 3
        check_player = arcade.check_for_collision_with_list(self.player, self.moving_platform_list)

        if check_player or self.cal:
            self.cal = True
            for platform in self.moving_platform_list:
                if check and cont == self.LIMIT:
                    self.move_platform *= (-1)
                    cont = 0
                platform.center_x += self.move_platform
            cont = 3

    def move_enemies_in_x(self, dt):
        for enemie in self.moving_enemies_list_in_x:
            check_in_x = arcade.check_for_collision_with_list(enemie, self.limit_of_enemies_moving_in_x)

            if check_in_x:
                self.move_enemie *= (-1)
            enemie.center_x += self.move_enemie

    def move_enemies_in_y(self, dt):
        for enemy in self.moving_enemies_list_in_y:
            check_in_y = arcade.check_for_collision_with_list(enemy, self.limit_of_enemies_moving_in_y)

            if check_in_y:
                self.move_enemy *= (-1)
            enemy.center_y += self.move_enemy

    def on_update(self, dt):
        if self.player_life >= 0:
            super().on_update(dt)
            self.collide_coins(dt)
            # self.collide_spikes(dt)
            self.collide_enemies(dt)
            self.move_enemies_in_x(dt)
            self.move_enemies_in_y(dt)
            self.collide_discs(dt)
            self.move_platforms(dt)
            self.game_over(dt)
        else:
            self.game_over(dt)

        # JUMP SOUND
        if self.player.change_y > 0:
            if not self.jumping:
                arcade.play_sound(self.jump_sound)
            self.jumping = True
        else:
            self.jumping = False
            
    def draw_elements(self):
        super().draw_elements()
        self.enemies.draw()
        self.coins.draw()
        self.spikes.draw()
        self.moving_enemies_list_in_x.draw()
        self.moving_enemies_list_in_y.draw()
        self.moving_platform_list.draw()
        self.discs.draw()
        self.doorkey.draw()
        self.doortop.draw()
     
        #Placar de Contagem das moedas e vidas
        output_score = f"Score: {self.score_coins} ||"
        output_life = f"Life: {self.player_life}"
        arcade.draw_text(output_score, self.viewport_horizontal_start, self.viewport_vertical_start + 10, arcade.color.BLACK, 25)
        arcade.draw_text(output_life, self.viewport_horizontal_start + 250, self.viewport_vertical_start + 10, arcade.color.BLACK, 25)

if __name__ == "__main__":
    Game().run()
