from test.bases import WorldTestBase

from worlds.dota_2 import DOTA2World

# Tests are a big topic.
# The testing API and the core code in general empower you to test all kinds of complicated custom behavior.
# However, for APQuest, we'll stick to some of the more basic tests.


# Most of your testing will probably be done using the generic WorldTestBase.
# WorldTestBase is a class that performs a set of generic tests on your world using a given set of options.
# It also enables you to write custom tests with a slew of generic helper functions.
# The first thing you'll want to do is subclass it. You'll want to override "game" And "world" like this.
class Dota2TestBase(WorldTestBase):
    game = "DOTA 2"
    world = DOTA2World


# The actual tests you write should be in files whose names start with "test_".
# Ideally, you should group similar tests together in one file, where each file has some overarching significance.
