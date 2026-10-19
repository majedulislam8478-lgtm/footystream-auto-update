import os

def generate_m3u8():
    # সরাসরি আপনার কাঙ্ক্ষিত প্লেলিস্ট স্ট্রাকচার এখানে ডিফাইন করা থাকবে, যা কোনো এরর ছাড়াই কাজ করবে
    m3u8_content = "#EXTM3U\n"
    m3u8_content += "#EXT-X-VERSION:3\n\n"

    # একটি লাইভ বা আপকামিং ম্যাচের উদাহরণ
    m3u8_content += '#EXTINF:-1 group-title="Live Sports",[Starts in: 00:00:00] Team A vs Team B\n'
    m3u8_content += '#EXTVLCOPT:http-referrer=https://playerdee.top/\n'
    m3u8_content += '#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n'
    m3u8_content += '#EXTHTTP:{"USER-AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)","REFERER":"https://playerdee.top/"}\n'
    m3u8_content += 'https://example.com/live/stream.m3u8\n\n'

    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u8_content)

    print("Playlist generated successfully!")

if __name__ == "__main__":
    generate_m3u8()
