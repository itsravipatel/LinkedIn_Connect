# LinkedIn_Connect

Allows the user to send LinkedIn connection requests automatically via Selenium. If feasible, the tool parses an Excel file containing LinkedIn profile URLs and sends each one a connection request. The user has the option to dynamically incorporate the receiving profile's name into the connection request message and can also specify the number of requests to send. This application makes it easy for users to expand their LinkedIn connection network.

# Installation
Prerequisites:
1. Install [Python / Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html).
2. Download [Google Chrome](https://www.google.com/chrome/).

Steps:
1. Download source code.
2. Open your computer's terminal and navigate to the application's folder.
3. Run the following command to install the application's dependencies:
   ```console
   pip install pillow numpy pandas selenium requests openpyxl
   ```
4. Start the application by running the following command:
   ```console
   python main.py
   ```
