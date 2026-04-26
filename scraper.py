import yt_dlp
import json

# तुम्हारे 5 चैनल्स
CHANNELS = [
    'https://www.youtube.com/@ARYDigitalasia/playlists',
    'https://www.youtube.com/@humtv/playlists',
    'https://www.youtube.com/@HarPalGeoOfficial/playlists',
    'https://www.youtube.com/@GreenEntertainmentTV/playlists',
    'https://www.youtube.com/@ExpressEntertainment/playlists'
]

def scrape_dramas():
    ydl_opts = {'extract_flat': True, 'quiet': True}
    all_dramas = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in CHANNELS:
            print(f"Checking: {channel_url}")
            try:
                info = ydl.extract_info(channel_url, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        title = entry.get('title', '')
                        if any(x in title.lower() for x in ['ost', 'teaser', 'promo']): continue
                        all_dramas.append({
                            "name": title.split('|')[0].split('-')[0].strip(),
                            "url": entry.get('url', ''),
                            "poster": entry.get('thumbnails', [{}])[-1].get('url', '')
                        })
            except Exception as e: print(f"Error: {e}")
    
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_dramas, f, ensure_ascii=False, indent=4)

if __name__ == "__main__": scrape_dramas()
