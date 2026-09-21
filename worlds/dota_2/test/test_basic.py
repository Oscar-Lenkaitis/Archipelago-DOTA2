from .bases import Dota2TestBase

class BasicTestLogic(Dota2TestBase):
    options = {
        "goal_type": 1,
        "TotalWinsToWin": 3,
        "PrimordialFragmentsToWin":5,
        "PrimordialFragmentsToUnlockFinal":5
        # Options you don't specify will use their default values.
        # It is good practice to specify every option that has an impact on your test, even when it's the default value.
    }

    def test_basic_access(self) -> None:
        with self.subTest("Test checks accessible with nothing"):
            blood_grenade = self.world.get_location("Blood Grenade")
            itron_branch = self.world.get_location("Iron Branch")

            # Since access rules have a "state" argument, we must pass our current CollectionState.
            # Helpfully, since we're in a WorldTestBase, we can just use "self.multiworld.state".
            self.assertTrue(blood_grenade.can_reach(self.multiworld.state))
            self.assertTrue(itron_branch.can_reach(self.multiworld.state))