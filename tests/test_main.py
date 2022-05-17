from kivy.logger import LOG_LEVELS, Logger

from game.controller import Card, CardBox, Controller
from game.main import Game


def cheat_to_win(c: Controller):
    done = CardBox()
    for i, card in enumerate(c.grid):
        if card in done:
            continue

        c.make_move(i)
        for j, card2 in enumerate(c.grid[i + 1 :]):
            if card2 == card:
                c.make_move(i + j + 1)
                break
        done.append(card)


def make_bad_moves(c: Controller):
    c.make_move(0)
    if c.grid[1] in c.hand:
        i = 2
    else:
        i = 1
    c.make_move(i)


def make_exact_moves(c: Controller):
    c.make_move(0)
    c.make_move(0)


def test_game():
    g = Game()


def test_controller():
    # Logger.setLevel(LOG_LEVELS["debug"])
    c = Controller()
    c.setup()
    assert len(c.grid) == 30
    c.restart()
    assert len(c.grid) == 30
    make_bad_moves(c)
    make_exact_moves(c)
    cheat_to_win(c)
    assert all(i.is_disabled for i in c.grid)


def test_card():
    c = Card("testing")
    c.flip()
    c.unflip()
    c.disable()
    assert c == Card("testing")
    assert c is not Card("testing")
    assert c != Card("testing2")


def test_cardbox():
    box = CardBox()
    card = Card("A")
    box.append(card)
    assert Card("A") in box
    assert any(card is i for i in box)
