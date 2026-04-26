import yt_dlp
import json

CHANNELS = [
    'https://www.youtube.com/@ARYDigitalasia/playlists',
    'https://www.youtube.com/@humtv/playlists',
    'https://www.youtube.com/@HarPalGeoOfficial/playlists',
    'https://www.youtube.com/@GreenEntertainmentTV/playlists',
    'https://www.youtube.com/@ExpressEntertainment/playlists'
]

def scrape_dramas():
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'force_generic_extractor': False,
    }
    
    all_dramas = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in CHANNELS:
            print(f"Fetching from: {channel_url}")
            try:
                # हम प्लेलिस्ट का मेटाडेटा निकाल रहे हैं
                info = ydl.extract_info(channel_url, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        title = entry.get('title', '')
                        # कचरा फिल्टर
                        lower_title = title.lower()
                        if any(x in lower_title for x in ['ost', 'teaser', 'promo', 'short', 'song']):
                            continue
                        
                        # पब्लिश डेट निकालना (YYYYMMDD फॉर्मेट में मिलता है)
                        # अगर डेट नहीं मिलती तो बहुत पुरानी डेट (1900) डाल देंगे ताकि एरर न आए
                        pub_date = entry.get('upload_date') or "19000101"
                            
                        all_dramas.append({
                            "name": title.split('|')[0].split('-')[0].strip(),
                            "url": entry.get('url', ''),
                            "poster": entry.get('thumbnails', [{}])[-1].get('url', ''),
                            "date": pub_date  # सॉर्टिंग के लिए डेट सेव कर रहे हैं
                        })
            except Exception as e:
                print(f"Error: {e}")

    # --- जादुई सॉर्टिंग लॉजिक ---
    # यह लाइन पूरी लिस्ट को 'date' के हिसाब से छोटे से बड़े (Oldest to Newest) में लगा देगी
    all_dramas.sort(key=lambda x: x['date'])

    # JSON सेव करने से पहले 'date' की चाबी हटा देते हैं ताकि फाइल साफ रहे
    for item in all_dramas:
        del item['date']

    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_dramas, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_dramas()
