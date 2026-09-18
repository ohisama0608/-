import json
import urllib.request
import re

url = "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=46"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

data = {
    "date": "2026年9月17日",
    "title": "つつうらうら。 こころもうらら",
    "link": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=46",
    "image": ""
}

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        links = re.findall(r'<a href="(/s/official/diary/detail/\d+\?ima=\d+&ct=\d+)">', html)
        images = re.findall(r'<img[^>]+src="(https://cdn\.hinatazaka46\.com/files/\d+/diary/official/member/moblog/[^"]+)"', html)
        titles = re.findall(r'<div class="title"[^>]*>(.*?)<\/div>', html)
        if not titles:
            titles = re.findall(r'<p class="title"[^>]*>(.*?)<\/p>', html)
        dates = re.findall(r'<p class="date path"[^>]*>(.*?)<\/p>', html)
        
        if titles:
            clean_title = re.sub(r'<[^>]+>', '', titles[0]).strip()
            if clean_title:
                data["title"] = clean_title
        if dates:
            clean_date = re.sub(r'<[^>]+>', '', dates[0]).strip()
            if clean_date:
                data["date"] = clean_date
        if links:
            data["link"] = "https://www.hinatazaka46.com" + links[0]
        if images:
            data["image"] = images[0]
except Exception as e:
    print(f"Error fetching blog: {e}")

with open('blog_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
