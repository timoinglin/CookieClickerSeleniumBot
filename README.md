# CookieClickerSeleniumBot

An advanced automation bot for [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/), built using Selenium WebDriver. This bot enhances your gameplay by automating cookie clicking, golden cookie collection, upgrade purchases, and game save management.


**Note:** This bot is designed to assist with cookie farming while you're away. It is *not* a fully autonomous bot that plays through the entire game. This way, you can still enjoy the core fun of the game, such as planning your strategies, making legacy upgrades, and unlocking achievements. The bot simply ensures that your progress continues even when you're not actively playing.

## Features

- **Automated Big Cookie Clicking**: Rapidly clicks the big cookie to maximize cookie production.
- **Golden Cookie Detection and Clicking**: Continuously monitors and clicks golden cookies immediately upon appearance.
- **Automatic Upgrades and Product Purchases**:
  - Buys available upgrades to boost production efficiency.
  - Purchases products, prioritizing the most expensive affordable ones to optimize growth.
- **Game Save Management**:
  - **Initial Save Loading**: Automatically imports the most recent game save at startup.
  - **Periodic Backups**: Exports and saves the game state at configurable intervals.
  - **Backup Rotation**: Retains a specified number of backups, deleting the oldest to manage storage.

## Requirements

- **Python 3.7 or higher**
- **Google Chrome Browser**
- **Chrome WebDriver**: Managed automatically via `webdriver-manager`.
- **Dependencies**: Listed in `requirements.txt`.

## Installation (Windows)

### 1. Install Python

Ensure Python 3.7 or higher is installed. Download it from [python.org](https://www.python.org/downloads/).

### 2. Clone the Repository

Open Command Prompt and run:

```bash
git clone https://github.com/timoinglin/CookieClickerSeleniumBot.git
cd CookieClickerSeleniumBot
```

### 3. Create a Virtual Environment

Create a virtual environment to manage dependencies:

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

```bash
venv\Scripts\activate
```

### 5. Upgrade Pip (Optional but Recommended)

```bash
pip install --upgrade pip
```

### 6. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Bot

### Option 1: Using the Batch File (`start_bot.bat`)

To simplify running the bot, a `start_bot.bat` file is provided in the root directory.

1. **Ensure the virtual environment is created** as per the installation instructions.
2. **Double-click** the `start_bot.bat` file in the project directory.
3. The bot will start automatically, activating the virtual environment and running the script.
4. The Command Prompt window will remain open to display logs and messages.

### Option 2: Using Command Prompt

With the virtual environment activated, you can run the bot via Command Prompt:

```bash
python cookie_clicker_bot.py
```

### Controls

- **Pause the Bot**: Press `Esc` while the bot is running to pause automation.
- **Resume or Exit**: After pausing, press `x` to exit or any other key to resume.

### Configuration

You can adjust settings by modifying constants at the beginning of the script:

- `CHECK_INTERVAL`: Interval in seconds to check for upgrades and products (default: 5 seconds).
- `EXPORT_INTERVAL`: Interval in seconds to export game saves (default: 60 seconds).
- `MAX_BACKUPS`: Maximum number of backup files to retain (default: 30).
- `COOKIE_CLICK_DELAY`: Delay between big cookie clicks in seconds (default: 0.01 seconds).

### Save Files

- **Location**: Game saves are stored in the `exports` directory within the project folder.
- **Backup Management**: The bot maintains backups by date and time, deleting the oldest when `MAX_BACKUPS` is exceeded.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.