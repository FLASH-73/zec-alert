# Zcash Terminal Alert

This is a script. It watches Zcash. You've probably chained yourself to a much worse system architecture for a lot less.

It displays the price and some text you seem to care about, "Generational Wealth." A fitting monument to your optimism. It also makes a noise if the price moves too much, probably to wake you up when your leveraged position gets liquidated.

## What It Does

* **Stares at the Binance API**: It relentlessly fetches the ZEC/EUR price, because what else is there to do?
* **Generates Art**: It uses `pyfiglet` to render text. I suppose that's what passes for art in this decadent age.
* **Makes Noise**: If the price change breaches a threshold you set, it plays `alert.wav`. Try not to use a clip of Richard screaming.
* **Flickers (or doesn't)**: It uses `rich` to make the terminal look less like a dumpster fire. A marginal improvement.

## Installation

This process is now automated because I don't trust you to follow manual steps.

### 1. Prerequisites

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).
* `git` installed on your system.

### 2. Installation

Open your terminal.

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/FLASH-73/zec-alert.git]
    cd [zec-alert]
    ```

2.  **Create the environment:**
    Conda will read the `environment.yml` file and build everything. This is a single command. Do not mess it up.
    ```bash
    conda env create -f environment.yml
    ```
    This will create the `zec-alert` environment and install all dependencies.

3.  **Activate the environment:**
    You must activate the environment every time you want to run the script.
    ```bash
    conda activate zec-alert
    ```

## Usage

If you've navigated the labyrinth of installation, you can finally run it.

```bash
python alert.py
```

![Gilfoyle GIF](gif_gilfoyle.gif)