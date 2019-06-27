import fgarcade as ge


class Game(ge.Platformer):
    """
    Simple platformer example
    """

    title = 'Candy Shop'
    player_initial_tile = 4, 1
    final = 50

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

        #self.create_block('green', (5, 8))
        #self.create_block('red', (6, 8))
        #self.create_block('grey', (7, 8))
        #self.create_block('brown', (8, 8))
        #self.create_block('red-lock', (9, 8))

        #self.create_arrow('right', (3, 1))


        #self.create_fence('left', (10, 1))
        #self.create_fence('middle', (11, 1))
        #self.create_fence('middle', (12, 1))
        #self.create_fence('right', (13, 1))

        #self.create_foreground('other/plant/blue-3', (4, 1))
        #self.create_foreground('other/plant/blue-1', (7, 2))
        #self.create_foreground('other/plant/blue-5', (9, 2))

    def init_enemies(self):
        pass

    def init_items(self):
        pass


    def init(self):
        self.init_world()
        self.init_items()
        self.init_enemies()


if __name__ == "__main__":
    Game().run()
