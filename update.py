import os
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://pogo.pk/"
REFERER_URL = "https://playerdee.top/"

def fetch_matches():
    matches = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": REFERER_URL
    }

    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Failed to fetch website. Status code: {response.status_code}")
            return matches

        soup = BeautifulSoup(response.text, 'html.parser')
        match_cards = soup.find_all('div', class_='match-card')
        
        if not match_cards:
            print("No matches found via automated scraping. Using sample structure.")
            return matches

        for card in match_cards:
            home_team = card.find('span', class_='home-team').text.strip() if card.find('span', class_='home-team') else "Home Team"
            away_team = card.find('span', class_='away-team').text.strip() if card.find('span', class_='away-team') else "Away Team"
            m3u8_link = card.get('data-stream', 'https://example.com/stream.m3u8')
            category = card.find('div', class_='league-name').text.strip() if card.find('div', class_='league-name') else "Live Sports"
            status = card.get('data-status', 'upcoming')
            start_time = card.find('span', class_='match-time').text.strip() if card.find('span', class_='match-time') else "Live Now"

            matches.append({
                "status": status,
                "category": category,
                "start_time": start_time,
                "home_team": home_team,
                "away_team": away_team,
                "m3u8": m3u8_link,
                "referer": REFERER_URL,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })

    except Exception as e:
        print(f"Error while scraping: {e}")

    return matches

def generate_m3u8():
    matches = fetch_matches()

    if not matches:
        matches = [
            {
                "status": "live",
                "category": "Live Now",
                "start_time": "Live Now!",
                "home_team": "Pogo Stream Match",
                "away_team": "Live",
                "m3u8": "https://example.com/live/stream.m3u8",
                "referer": REFERER_URL,
                "user_agent": "Mozilla/5.0"
            }
        ]

    m3u8_content = "#EXTM3U\n"
    m3u8_content += "#EXT-X-VERSION:3\n\n"

    live_matches = [m for m in matches if m.get("status") == "live"]
    upcoming_matches = [m for m in matches if m.get("status") != "live"]
    all_sorted_matches = live_matches + upcoming_matches

    for match in all_sorted_matches:
        if match.get("status") != "live" and match.get("start_time"):
            title = f"[{match['start_time']}] {match['home_team']} vs {match['away_team']}"
        else:
            title = f"{match['home_team']} vs {match['away_team']}"

        category = match.get("category", "Sports")

        m3u8_content += f'#EXTINF:-1 group-title="{category}",{title}\n'
        m3u8_content += f'#EXTVLCOPT:http-referrer={match["referer"]}\n'
        m3u8_content += f'#EXTVLCOPT:http-user-agent={match["user_agent"]}\n'
        m3u8_content += f'#EXTHTTP:{{"USER-AGENT":"{match["user_agent"]}","REFERER":"{match["referer"]}"}}\n'
        m3u8_content += f'{match["m3u8"]}\n\n'

    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u8_content)

    print("Playlist updated successfully with Referer!")

if __name__ == "__main__":
    generate_m3u8()
