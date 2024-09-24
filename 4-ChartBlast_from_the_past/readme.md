Billboard Chart Playlist Creator

The Billboard Chart Playlist Creator is a Python script that generates a Spotify playlist based on the top 100 songs from a specific date in the Billboard chart. It uses the Spotipy library to interact with the Spotify API and BeautifulSoup for web scraping.

Prerequisites:

- Python 3.x

- Spotipy library

- BeautifulSoup library

- dotenv library

Installation:

1\. Clone the repository:

   git clone https://github.com/your-username/billboard-chart-playlist-creator.git

2\. Install the required dependencies:

   pip install spotipy beautifulsoup4 python-dotenv

Usage:

1\. Obtain Spotify API credentials:

   - Go to the Spotify Developer Dashboard and create a new app.

   - Copy the Client ID and Client Secret.

2\. Create a file named ".env" in the project root directory and add the following contents:

   SPOTIPY_CLIENT_ID=your-client-id

   SPOTIPY_CLIENT_SECRET=your-client-secret

3\. Run the script:

   python playlist_creator.py

4\. Enter the desired date in the format YYYY-MM-DD when prompted.

5\. The script will generate a Spotify playlist with the top 100 songs from the Billboard chart on the specified date. If the playlist already exists, it will be updated with the new songs.

Contributing:

Contributions are welcome! If you have any suggestions or improvements for the project, feel free to submit a pull request.

License:

This project is licensed under the MIT License.