import os
import time
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime, timedelta
from pydub import AudioSegment
from pydub.playback import play
from pyfiglet import figlet_format

# 'rich' replaces colorama and prettytable
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

# --- CONSTANTS (No changes) ---
DEFAULT_TICKER = 'ZEC'
DEFAULT_CONVERT = 'EUR'
DEFAULT_DELTA_TRIGGER = 0.03
DEFAULT_SOUNDFILE = 'alert.wav'
DEFAULT_DELTA_REFRESH_SECONDS = 15
MAX_ROWS_DISPLAYED = 15


class ZcashAlert():
    endpoint = 'https://api.binance.com/api/v3/avgPrice'

    @staticmethod
    def __getPercent(price, prev):
        return ((price - prev) * 100 / price)

    # --- __getLogo is no longer needed, art is built into the layout ---

    def __init__(self, ticker, convert, delta, sound_file, delta_refresh_seconds):
        self.ticker = ticker
        self.convert = convert
        self.delta = delta
        self.sound_file = sound_file
        self.delta_refresh_seconds = delta_refresh_seconds

    def build_layout(self) -> Layout:
        """Defines the TUI layout."""
        layout = Layout(name="root")
        
        # Generate the art and color it with 'rich'
        title = figlet_format("ZCASH ALERT", font="standard")
        subtitle = figlet_format("GENERATIONAL WEALTH", font="standard")
        logo_text = Text(f"{title}\n{subtitle}", style="bold blue") # <-- Color is set here
        
        layout.split_column(
            Layout(name="header"), # Size 15 fits the art
            Layout(name="body")
        )
        # Put the art in a Panel for a nice border
        layout["header"].update(Panel(logo_text, border_style="blue"))
        layout["body"].update(self.build_table([])) # Start with an empty table
        return layout

    def build_table(self, rows_data: list) -> Table:
        """Builds a new table from the current data."""
        table = Table(expand=True)
        table.add_column("Asset", style="cyan")
        table.add_column("Previous Value (" + self.convert + ")")
        table.add_column("New Value (" + self.convert + ")")
        table.add_column("Last Updated")
        table.add_column("Percentage (%)", justify="right")
        
        for row in rows_data:
            table.add_row(*row)
        return table

    def start(self):
        layout = self.build_layout()
        rows_data = [] # We will store data rows here
        previous = 0.0

        try:
            # 'Live' manages the screen updates
            with Live(layout, screen=True, refresh_per_second=4) as live:
                while True:
                    # --- Data Fetching (No change) ---
                    response_zec = requests.get(
                        f'{self.endpoint}?symbol={self.ticker}USDT').json()
                    price_zec_usdt = float(response_zec['price'])

                    response_usdt = requests.get(
                        f'{self.endpoint}?symbol=EURUSDT').json()
                    price_usdt_per_eur = float(response_usdt['price'])

                    price_usdt_eur = 1 / price_usdt_per_eur
                    price = price_zec_usdt * price_usdt_eur
                    
                    # --- Data Processing ---
                    if previous == 0.0: previous = price # Set initial price
                    
                    percent = self.__getPercent(price, previous)
                    
                    # Use 'rich' color markup
                    percent_str = (
                        f"[green]+{round(percent, 3)}" if percent > 0 
                        else f"[red]{round(percent, 3)}"
                    )
                    
                    # Add new data row
                    rows_data.append([
                        f'{self.ticker}', 
                        f'{round(previous, 2):,}',
                        f'{round(price, 2):,}', 
                        datetime.now().strftime("%H:%M:%S"),
                        percent_str
                    ])
                    
                    # Limit rows displayed
                    if len(rows_data) > MAX_ROWS_DISPLAYED:
                        rows_data = rows_data[-MAX_ROWS_DISPLAYED:]

                    # Re-build the table with new data
                    layout["body"].update(self.build_table(rows_data))
                    
                    # --- Alert (No change) ---
                    if (abs(percent) > self.delta):
                        try:
                            sound = AudioSegment.from_file(self.sound_file)
                            play(sound)
                        except Exception as e:
                            live.console.print(f"Sound playback failed: {e}")
                    
                    previous = price
                    time.sleep(self.delta_refresh_seconds)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        except KeyboardInterrupt:
            print("\nExiting.")


if __name__ == "__main__":
    ZcashAlert(DEFAULT_TICKER, DEFAULT_CONVERT, DEFAULT_DELTA_TRIGGER,
                 DEFAULT_SOUNDFILE, DEFAULT_DELTA_REFRESH_SECONDS).start()