from dataclasses import dataclass

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from game.controller import Card, Controller


@dataclass
class ButtonController:  # pragma: no cover
    button: Button
    card: Card
    grid_index: int
    grid: GridLayout
    controller: Controller

    def setup(self):
        def flip_hook():
            self.button.text = self.card.name

        def unflip_hook():
            self.button.text = ""

        def disable_hook():
            self.button.text = self.card.name
            self.button.disabled = True

        def card_pressed(_):
            self.controller.make_move(self.grid_index)

        self.card.flip_hook = flip_hook
        self.card.unflip_hook = unflip_hook
        self.card.disable_hook = disable_hook
        self.button.bind(on_press=card_pressed)
        self.grid.add_widget(self.button)


class Game(App):
    def build(self):  # pragma: no cover
        self.load_kv()
        self.controller = Controller()

        def game_over():
            self.root.ids.game_over_widget.opacity = 1

        self.controller.game_over_hook = game_over

        self.controller.setup()
        for i, card in enumerate(self.controller.grid):
            bc = ButtonController(
                Button(), card, i, self.root.ids.grid, self.controller
            )
            bc.setup()


def main():
    Game().run()


if __name__ == "__main__":
    main()
