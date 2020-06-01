import enum


class BatStats(enum.Enum):
    runs = 0
    balls = 1
    fours = 2
    six = 3
    played = 4
    not_out = 5


class BowlStats(enum.Enum):
    balls = 0
    maidens = 1
    runs = 2
    wickets = 3
