import json
import urllib.request
import re

url = "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=46"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        # 簡易的なパターンマッチングによる最新記事の抽出
        titles = re.findall(r'<p class="title"><span>(.*?)<\/span><\/p>', html)
        dates = re.findall(r'<p class="date path"><span>(.*?)<\/span>', html)
        
        if titles and dates:
            latest_title = titles[0].strip()
            latest_date = dates[0].strip()
            
            data = {
                "date": latest_date,
                "title": latest_title
            }
            
            with open('blog_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(f"Error fetching blog: {e}")
