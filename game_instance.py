# MIT License

# Copyright (c) 2024 Marko

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from nicegui import ui
import asyncio
import random as rnd


def color_card(e, color):
    e.sender.props('color=' + color)


class PairsGame:
    def __init__(self):
        self.buttons = []
        self.board = []
        self.uncovered_cards = []
        self.correct_cards = []
        self.player1_cards = []
        self.player2_cards = []
        self.player_current = 0
        self.player1_score = ui.label()
        self.player2_score = ui.label()
        self.testing = False

    def create_board(self):
        emojis = [
            "😀", "😁", "😂", "😃", "😄", "😅", "😆", "😇", "😈", "🙏",
            "😉", "😊", "😋", "😌", "😍", "😎", "😏", "😐", "😑", "😒", "😓",
            "😔", "😕", "😖", "😗", "😘", "😙", "😚", "😛", "😜", "😝", "😞",
            "😟", "😠", "😡", "😢", "😣", "😤", "😥", "😦", "😧", "😨", "😩",
            "😪", "😫", "😬", "😭", "😮", "😯", "😰", "😱", "😲", "😳", "😴",
            "😵", "😶", "😷", "😸", "😹", "😺", "😻", "😼", "😽", "😾", "😿",
            "🙀", "🙁", "🙂", "🙃", "🙄", "🙅", "🙆", "🙇", "🙈", "🙉", "🙊",
            "🙋", "🙌", "🙍", "🙎"]
        rnd.shuffle(emojis)
        for x in range(0, 36, 2):
            self.board.append(emojis[int((x/2)+1)])
            self.board.append(emojis[int((x/2)+1)])
        rnd.shuffle(self.board)

    def end_game(self):
        ui.notify('ENDGAME!')
        for btn in self.buttons:
            btn.props('color=black')

    def check_equality(self):
        if self.board[self.uncovered_cards[0][1]] == self.board[self.uncovered_cards[1][1]]:  # noqa: E501
            ui.notify("✅✅✅")
            if self.player_current == 0:
                if not self.testing:
                    color_card(self.uncovered_cards[0][0], 'red')
                    color_card(self.uncovered_cards[1][0], 'red')
                self.player1_cards.append(self.uncovered_cards[0][0])
                self.player1_cards.append(self.uncovered_cards[1][0])
            else:
                if not self.testing:
                    color_card(self.uncovered_cards[0][0], 'green')
                    color_card(self.uncovered_cards[1][0], 'green')
                self.player2_cards.append(self.uncovered_cards[0][0])
                self.player2_cards.append(self.uncovered_cards[1][0])
        else:
            ui.notify("❌❌❌")
            if not self.testing:
                self.uncovered_cards[0][0].sender.set_text(' ')
                self.uncovered_cards[1][0].sender.set_text(' ')
                color_card(self.uncovered_cards[0][0], 'grey-9')
                color_card(self.uncovered_cards[1][0], 'grey-9')
            if self.player_current == 0:
                self.player_current = 1
                if not self.testing:
                    self.player1_score.style('font-weight: normal')
                    self.player2_score.style('font-weight: 550;')
            else:
                self.player_current = 0
                if not self.testing:
                    self.player2_score.style('font-weight: normal;')
                    self.player1_score.style('font-weight: 550;')

        self.player1_score.set_text("Player 1: " + str(int(len(self.player1_cards)/2)))
        self.player2_score.set_text("Player 2: " + str(int(len(self.player2_cards)/2)))

        if (len(self.player1_cards) + len(self.player2_cards)) == 36:
            self.end_game()

        for btn in self.buttons:
            btn.enable()
        for i in range(len(self.correct_cards)):
            self.correct_cards[i].sender.disable()

        self.uncovered_cards.clear()

    async def press_button(self, e, i):
        self.uncovered_cards.append([e, i])

        if not self.testing:
            e.sender.set_text(self.board[i])
            color_card(e, 'white')
            e.sender.disable()

        if len(self.uncovered_cards) == 2:
            if not self.testing:
                for btn in self.buttons:
                    btn.disable()
                await asyncio.sleep(2)
            else:
                await asyncio.sleep(0)
            self.check_equality()

    def start_game(self):
        self.create_board()
        with ui.element('div').classes('flex column items-center absolute-center'):  # noqa: E501
            with ui.row().classes('justify-center'):
                self.player1_score = ui.label("Player 1: 0").classes('text-h2').style('margin-bottom: 20px; margin-right: 40px; color:red; font-weight: 550;')  # noqa: E501
                self.player2_score = ui.label("Player 2: 0").classes('text-h2').style('margin-bottom: 20px; color:green')  # noqa: E501
            with ui.grid(columns=6, rows=6).classes('justify-center'):
                for i in range(36):
                    # btn = ui.button(text=' ', color='grey-9', on_click=lambda e, i=i: self.press_button(e, i)).classes('text-h3').style("max-width: 100px; min-width: 100px; max-height: 100px; min-height: 100px")  # noqa: E501
                    self.buttons.append(ui.button(text=' ', color='grey-9', on_click=lambda e, i=i: self.press_button(e, i)).classes('text-h3').style("max-width: 100px; min-width: 100px; max-height: 100px; min-height: 100px"))  # noqa: E501
