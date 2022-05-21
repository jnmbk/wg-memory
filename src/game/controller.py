import random
from collections import UserList
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from kivy.logger import Logger


@dataclass
class Card:
    name: str
    flip_hook: Callable[[], None] = lambda: None
    unflip_hook: Callable[[], None] = lambda: None
    disable_hook: Callable[[], None] = lambda: None
    is_disabled: bool = False
    is_flipped: bool = False
    is_matched: bool = False

    def flip(self):
        Logger.debug(f"App: Flipping {self.name}")
        self.is_flipped = True
        self.flip_hook()

    def unflip(self):
        Logger.debug(f"App: Unflipping {self.name}")
        self.is_flipped = False
        self.unflip_hook()

    def disable(self):
        Logger.debug(f"App: Disabling {self.name}")
        self.is_disabled = True
        self.disable_hook()

    def __eq__(self, obj):
        return obj.name == self.name


if TYPE_CHECKING:  # pragma: no cover
    BaseUserList = UserList[Card]
else:
    BaseUserList = UserList


class CardBox(BaseUserList):
    def __contains__(self, obj):
        return any(obj.name == i.name for i in self.data)


class Controller:
    def __init__(self):
        self.game_over_hook: Callable[[], None] = lambda: None
        self._reset()

    def _reset(self):
        self.grid = CardBox()
        self.hand = CardBox()
        self.move_count = 0

    def _generate_grid(self):
        self.grid = CardBox(Card(i) for i in "ABCDEFGHJKLMNPR" * 2)
        random.shuffle(self.grid)
        Logger.debug(f"App: Generated grid={[i.name for i in self.grid]}")

    def setup(self):
        self._generate_grid()

    def restart(self):
        self._reset()
        self._generate_grid()

    def make_move(self, grid_index):
        card = self.grid[grid_index]
        self.move_count += 1

        Logger.debug(f"App: making move on {grid_index=} {card.name=}")

        if len(self.hand) == 2:
            for i in self.hand:
                i.unflip()
            Logger.debug("App: Emptying hand")
            self.hand.clear()

        if card in self.hand:
            Logger.debug("App: Found same card in hand")
            exact_card_in_hand = any(card is i for i in self.hand)
            if exact_card_in_hand:
                Logger.debug("App: Found exact card in hand")
                card.unflip()
                self.hand.clear()
            else:
                for i in self.hand:
                    i.disable()
                card.disable()
                if all(i.is_disabled for i in self.grid):
                    Logger.debug("App: All same cards were found!")
                    self.game_over_hook()
                else:
                    Logger.debug("App: Emptying hand")
                    self.hand.clear()
        else:
            if len(self.hand) < 2:
                Logger.debug("App: Adding card to hand")
                self.hand.append(card)
                card.flip()
