import json
import urllib.request
import re

url = "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=46"
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
)

data = {
    "date": "2026年9月17日",
    "title": "つつうらうら。 こころもうらら",
    "link": "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=46",
    "image": ""
}

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        print(f"HTML length: {len(html)}")
        
        # より柔軟な条件でブログ詳細へのリンクを抽出
        links = re.findall(r'href="(/s/official/diary/detail/\d+[^"]*)"', html)
        
        # 画像の抽出
        images = re.findall(r'src="(https://cdn\.hinatazaka46\.com/files/\d+/diary/[^"]+)"', html)
        if not images:
            images = re.findall(r'src="(https?://[^"]+?/diary/[^"]+?\.(?:jpg|jpeg|png))"', html, re.IGNORECASE)
            
        # タイトルの抽出
        titles = re.findall(r'<div[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        if not titles:
            titles = re.findall(r'<p[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
        if not titles:
            titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL)

        # 日付の抽出
        dates = re.findall(r'<p[^>]*class="[^"]*date[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
        if not dates:
            dates = re.findall(r'<div[^>]*class="[^"]*date[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        
        print(f"Found links: {len(links)}, images: {len(images)}, titles: {len(titles)}, dates: {len(dates)}")
        
        if links:
            unique_links = []
            for l in links:
                if l not in unique_links:
                    unique_links.append(l)
            data["link"] = "https://www.hinatazaka46.com" + unique_links[0]
            
        if titles:
            clean_title = re.sub(r'<[^>]+>', '', titles[0]).strip()
            if clean_title:
                data["title"] = clean_title
                
        if dates:
            clean_date = re.sub(r'<[^>]+>', '', dates[0]).strip()
            if clean_date:
                data["date"] = clean_date
                
        if images:
            data["image"] = images[0]
            
except Exception as e:
    print(f"Error fetching blog: {e}")
    raise e

with open('blog_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
