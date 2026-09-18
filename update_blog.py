import json
import urllib.request
import re

url = "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=46"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        links = re.findall(r'<a href="(/s/official/diary/detail/\d+\?ima=\d+&ct=\d+)">', html)
        images = re.findall(r'<img src="(https://cdn\.hinatazaka46\.com/files/\d+/diary/hinata/[^"]+)"', html)
        titles = re.findall(r'<p class="title"><span>(.*?)<\/span><\/p>', html)
        dates = re.findall(r'<p class="date path"><span>(.*?)<\/span>', html)
        
        if titles and dates:
            latest_title = titles[0].strip()
            latest_date = dates[0].strip()
            latest_link = "https://www.hinatazaka46.com" + links[0] if links else "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=46"
            latest_img = images[0] if images else ""
            
            data = {
                "date": latest_date,
                "title": latest_title,
                "link": latest_link,
                "image": latest_img
            }
            
            with open('blog_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(f"Error fetching blog: {e}")
