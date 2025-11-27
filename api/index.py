from flask import Flask, jsonify
import requests
import feedparser # 专门解析 RSS 的神器
import re

app = Flask(__name__)

# 1. 赛程数据源 (ESPN)
ESPN_API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/13/schedule"

# 2. 新闻数据源 (Bleacher Report Lakers RSS)
NEWS_RSS_URL = "https://bleacherreport.com/articles/feed?tag_id=la-lakers"

@app.route('/api/schedule')
def get_schedule():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(ESPN_API_URL, headers=headers, timeout=10)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e), "events": []}), 500

@app.route('/api/news')
def get_news():
    try:
        # 使用 feedparser 解析 RSS
        feed = feedparser.parse(NEWS_RSS_URL)
        news_items = []
        
        for entry in feed.entries[:8]: # 只取前8条
            # 尝试提取图片：BR 的图片通常在 media_content 或 content 中
            img_url = "https://cdn.nba.com/manage/2023/10/lakers-logo-16x9-1.jpg" # 默认图
            
            # 1. 尝试从 media_content 获取
            if 'media_content' in entry and len(entry.media_content) > 0:
                img_url = entry.media_content[0]['url']
            # 2. 尝试从 description 中正则匹配 jpg/png
            elif 'summary' in entry:
                match = re.search(r'src="([^"]+\.(jpg|png|jpeg))"', entry.summary)
                if match:
                    img_url = match.group(1)

            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "time": entry.published,
                "image": img_url,
                "author": entry.get('author', 'Lakers Nation')
            })
            
        return jsonify({"status": "ok", "items": news_items})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    app.run()
