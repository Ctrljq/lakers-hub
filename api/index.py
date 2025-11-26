from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ESPN 接口地址
ESPN_API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/13/schedule"

@app.route('/api/schedule')
def get_schedule():
    try:
        # 后端服务器去请求 ESPN，速度快且稳定，没有 CORS 问题
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(ESPN_API_URL, headers=headers, timeout=10)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e), "events": []}), 500

# Vercel 需要这一行来识别应用
if __name__ == '__main__':
    app.run()