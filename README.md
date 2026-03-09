🤖 JARVIS: Personal Voice Assistant

A simple yet powerful voice assistant built using Python. It uses AI to answer questions, helps with daily tasks like opening websites, and can even fetch the latest news for you.

🌟 What can it do?
Talks to you: Uses AI (Groq/Llama 3.3) to give smart, witty answers like the real Jarvis.

Voice Control: Just say "Jarvis" to wake it up and give a command.

Opens Apps: Can launch VS Code, Chrome, YouTube, or LinkedIn instantly.

Plays Music: Integrated with a custom library to play your favorite tracks.

Live News: Fetches the latest headlines from India.

Memory: Remembers the last few things you talked about.

🛠️ How to setup
Clone this folder to your computer.

Install the requirements using:
pip install -r requirements.txt

Add your API Keys in a .env file:

GROQ_API_KEY

NEWS_API_KEY

Run the script:
python main3.py (or whichever version you are using).

📂 Project Structure
main.py: The core engine of Jarvis.

musicLibrary.py: Where all your favorite song links are stored.

jarvis_memory.json: Stores your chat history so Jarvis remembers you.

.env: To keep your secret API keys safe.

🚀 Future Plans
Adding Computer Vision to recognize faces.

Improving the UI with a dashboard.