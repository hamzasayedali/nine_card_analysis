import sys, random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt


# --- Card class ---
class Card:
    def __init__(self, rank, suit, open=True):
        self.rank = rank
        self.suit = suit
        self.open = open

    def __str__(self):
        return f"{self.rank}{self.suit}" if self.open else "🂠"


# --- Constants ---
RANK_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["♠", "♥", "♦", "♣"]

def rank_value(rank):
    return RANK_ORDER.index(rank)


# --- GUI ---
class NineCardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nine Card Game")
        self.setFixedSize(650, 750)

        # Create deck and initial grid
        self.deck = self._make_deck()
        self.game_state = self._draw_initial_grid()

        self.card_widgets = []

        layout = QVBoxLayout()
        grid = QGridLayout()
        layout.addLayout(grid)

        self.status_label = QLabel("Guess if the next card will be higher, equal, or lower.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.deck_label = QLabel(f"Deck: {len(self.deck)} cards left")
        self.deck_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.deck_label)

        self.setLayout(layout)

        # Build grid with cards + buttons
        for r in range(3):
            row_widgets = []
            for c in range(3):
                card = self.game_state[r][c]
                cell_layout = QVBoxLayout()

                # Card label
                card_label = QLabel(str(card))
                card_label.setFixedSize(100, 140)
                card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self._style_card_label(card_label, card)

                # Guess buttons
                btn_layout = QHBoxLayout()
                for guess in ["H", "=", "L"]:
                    btn = QPushButton(guess)
                    btn.setFixedWidth(30)
                    btn.clicked.connect(lambda _, r=r, c=c, g=guess: self.make_guess(r, c, g))
                    btn_layout.addWidget(btn)

                cell_layout.addWidget(card_label)
                cell_layout.addLayout(btn_layout)
                grid.addLayout(cell_layout, r, c)

                row_widgets.append(card_label)
            self.card_widgets.append(row_widgets)

    # --- Deck setup ---
    def _make_deck(self):
        deck = [Card(rank, suit, open=True) for suit in SUITS for rank in RANK_ORDER]
        for c in deck:
            print(c.rank)
        random.shuffle(deck)
        return deck

    def _draw_initial_grid(self):
        grid = []
        for _ in range(3):
            row = []
            for _ in range(3):
                row.append(self.deck.pop())  # draw 9 cards
            grid.append(row)
        return grid

    # --- Card styling ---
    def _style_card_label(self, label, card):
        if not card.open:
            label.setStyleSheet("font-size: 22px; color: gray; border: 1px solid gray; background-color: #ddd;")
        else:
            color = "red" if card.suit in ["♥", "♦"] else "black"
            label.setStyleSheet(f"font-size: 22px; color: {color}; border: 1px solid gray; background-color: white;")

    # --- Gameplay logic ---
    def make_guess(self, row, col, guess):
        if len(self.deck) == 0:
            self.status_label.setText("No more cards in deck!")
            return

        card = self.game_state[row][col]
        if not card.open:
            self.status_label.setText("That card is already closed.")
            return

        current_val = rank_value(card.rank)
        next_card = self.deck.pop()
        next_val = rank_value(next_card.rank)

        result = (
            "H" if next_val > current_val else
            "L" if next_val < current_val else
            "="
        )

        # Check result
        if guess == result:
            self.status_label.setText(f"✅ Correct! {next_card} replaces {card}.")
            self.game_state[row][col] = next_card
            self.card_widgets[row][col].setText(str(next_card))
            self._style_card_label(self.card_widgets[row][col], next_card)
        else:
            self.status_label.setText(f"❌ Wrong! {next_card} was drawn. Card flipped.")
            card.open = False
            self.card_widgets[row][col].setText(str(card))
            self._style_card_label(self.card_widgets[row][col], card)

        # Update deck counter
        self.deck_label.setText(f"Deck: {len(self.deck)} cards left")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NineCardWindow()
    window.show()
    sys.exit(app.exec())
