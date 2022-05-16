
"""
# Type (Attack Pattern), Speed, Attack Speed, Bullet Count, Bullet Type, Bullet Displacement, Hp, Movement Pattern,
# Starting Pos, Destination Pos (4 arguments for M. Pat. 1), Time
# Enemy(0, 15, 30, 1, 1, 0, 2, 1, (0, 100), (180, 150, 40, 200), 60)
"""
Level1 = [
    # first wave shooting to player
    [0, 15, 30, 1, 1, 0, 2, 1, (0, 100), (180, 150, 40, 200), 60],
    [0, 15, 30, 1, 1, 0, 2, 1, (0, 100), (140, 130, 40, 200), 80],
    [0, 15, 30, 1, 1, 0, 2, 1, (0, 100), (100, 110, 40, 200), 100],
    [0, 15, 30, 1, 1, 0, 2, 1, (0, 100), (60, 90, 40, 200), 120],

    [0, 15, 30, 1, 1, 0, 2, 1, (400, 100), (220, 150, 360, 200), 60],
    [0, 15, 30, 1, 1, 0, 2, 1, (400, 100), (260, 130, 360, 200), 80],
    [0, 15, 30, 1, 1, 0, 2, 1, (400, 100), (300, 110, 360, 200), 100],
    [0, 15, 30, 1, 1, 0, 2, 1, (400, 100), (340, 90, 360, 200), 120],

    # 2 high hp nova attack
    [3, 3, 45, 10, 1, 0, 30, 0, (100, 0), (100, 120), 300],
    [3, 3, 45, 10, 1, 0, 30, 0, (300, 0), (300, 120), 300],

    # 3 bullets to player
    [1, 5, 47, 3, 0, 3, 2, 1, (0, 0), (-70, 400, 250, 275), 600],
    [1, 5, 47, 3, 0, 3, 2, 1, (0, 0), (-70, 400, 250, 275), 620],
    [1, 5, 47, 3, 0, 3, 2, 1, (0, 0), (-70, 400, 250, 275), 640],
    [1, 5, 47, 3, 0, 3, 2, 1, (0, 0), (-70, 400, 250, 275), 660],
    [1, 5, 47, 3, 0, 3, 2, 1, (0, 0), (-70, 400, 250, 275), 680],

    [1, 5, 47, 3, 0, 3, 2, 1, (400, 0), (470, 400, 250, 275), 600],
    [1, 5, 47, 3, 0, 3, 2, 1, (400, 0), (470, 400, 250, 275), 620],
    [1, 5, 47, 3, 0, 3, 2, 1, (400, 0), (470, 400, 250, 275), 640],
    [1, 5, 47, 3, 0, 3, 2, 1, (400, 0), (470, 400, 250, 275), 660],
    [1, 5, 47, 3, 0, 3, 2, 1, (400, 0), (470, 400, 250, 275), 680],

    # "random" moving bunch of enemies
    [1, 8, 60, 5, 0, 10, 2, 0, (110, 0), (110, 150), 800],
    [1, 8, 60, 5, 0, 10, 2, 0, (240, 0), (240, 85), 880],
    [1, 8, 60, 5, 0, 10, 2, 0, (45, 0), (45, 180), 960],
    [1, 8, 60, 5, 0, 10, 2, 0, (390, 0), (390, 130), 1040],
    [1, 8, 60, 5, 0, 10, 2, 0, (50, 0), (50, 150), 1120],
    [1, 8, 60, 5, 0, 10, 2, 0, (190, 0), (190, 170), 1200],
    [1, 8, 60, 5, 0, 10, 2, 0, (220, 0), (220, 100), 1280],
    [1, 8, 60, 5, 0, 10, 2, 0, (70, 0), (70, 50), 1360],

    # 2 arrays of dangerous enemies shooting to player
    [0, 8, 20, 1, 4, 0, 2, 1, (90, 0), (470, 150, 50, 270), 1500],
    [0, 8, 20, 7, 4, 10, 2, 1, (110, 0), (490, 130, 70, 250), 1500],
    [0, 8, 20, 1, 4, 0, 2, 1, (90, 0), (470, 150, 50, 270), 1510],
    [0, 8, 20, 7, 4, 10, 2, 1, (110, 0), (490, 130, 70, 250), 1510],
    [0, 8, 20, 1, 4, 0, 2, 1, (90, 0), (470, 150, 50, 270), 1520],
    [0, 8, 20, 7, 4, 10, 2, 1, (110, 0), (490, 130, 70, 250), 1520],
    [0, 8, 20, 1, 4, 0, 2, 1, (90, 0), (470, 150, 50, 270), 1530],
    [0, 8, 20, 7, 4, 10, 2, 1, (110, 0), (490, 130, 70, 250), 1530],
    [0, 8, 20, 1, 4, 0, 2, 1, (90, 0), (470, 150, 50, 270), 1540],
    [0, 8, 20, 7, 4, 10, 2, 1, (110, 0), (490, 130, 70, 250), 1540],

    [0, 8, 20, 1, 4, 0, 2, 1, (310, 0), (-70, 150, 350, 270), 1600],
    [0, 8, 20, 7, 4, 10, 2, 1, (290, 0), (-90, 130, 330, 250), 1600],
    [0, 8, 20, 1, 4, 0, 2, 1, (310, 0), (-70, 150, 350, 270), 1610],
    [0, 8, 20, 7, 4, 10, 2, 1, (290, 0), (-90, 130, 330, 250), 1610],
    [0, 8, 20, 1, 4, 0, 2, 1, (310, 0), (-70, 150, 350, 270), 1620],
    [0, 8, 20, 7, 4, 10, 2, 1, (290, 0), (-90, 130, 330, 250), 1620],
    [0, 8, 20, 1, 4, 0, 2, 1, (310, 0), (-70, 150, 350, 270), 1630],
    [0, 8, 20, 7, 4, 10, 2, 1, (290, 0), (-90, 130, 330, 250), 1630],
    [0, 8, 20, 1, 4, 0, 2, 1, (310, 0), (-70, 150, 350, 270), 1640],
    [0, 8, 20, 7, 4, 10, 2, 1, (290, 0), (-90, 130, 330, 250), 1640],

    # 1 thick "mini boss"
    [2, 5, 15, 25, 2, 0, 200, 0, (200, 0), (200, 100), 1800],

    # just another bunch of enemies
    [0, 10, 10, 1, 4, 0, 2, 1, (90, 0), (470, 370, 50, 270), 2300],
    [0, 10, 10, 1, 4, 0, 2, 1, (280, 0), (-70, 250, 270, 270), 2320],
    [0, 10, 10, 1, 4, 0, 2, 1, (200, 0), (470, 80, 270, 270), 2340],
    [0, 10, 10, 1, 4, 0, 2, 1, (130, 0), (-200, 400, 600, 200), 2380],

    [0, 10, 10, 1, 4, 0, 2, 1, (90, 0), (470, 370, 50, 270), 2400],
    [0, 10, 10, 1, 4, 0, 2, 1, (280, 0), (-70, 250, 270, 270), 2420],
    [0, 10, 10, 1, 4, 0, 2, 1, (200, 0), (470, 80, 270, 270), 2440],
    [0, 10, 10, 1, 4, 0, 2, 1, (130, 0), (-200, 400, 600, 200), 2480],

    [0, 10, 10, 5, 4, 10, 2, 1, (-10, 100), (300, 500, 260, -210), 2500],
    [0, 10, 10, 5, 4, 10, 2, 1, (410, 100), (100, 500, 140, -210), 2520],

    # 2 novas
    [4, 5, -70, 30, 3, 0, 9999, 1, (0, 0), (-70, 250, 400, 250), 2600],
    [4, 5, -70, 30, 3, 0, 9999, 1, (400, 0), (470, 250, 0, 250), 2600],

    # 2 random shooting enemies
    [5, 3, 10, 0, 4, 0, 9999, 0, (80, 430), (80, -70), 2850],
    [5, 3, 10, 0, 4, 0, 9999, 0, (320, -30), (320, 500), 2850],

    # 2 enemies shooting to player
    [1, 4, 40, 9, 4, 15, 9999, 1, (120, 0), (100, -70, 120, 380), 3100],
    [1, 4, 40, 9, 4, 15, 9999, 1, (280, 0), (300, -70, 280, 380), 3100]
]