## update_blog.py
import feedparser
import os
from datetime import datetime


# RSS 피드 URL
BLOG_URL = "https://ego2-1.tistory.com/rss"

# README 파일 경로
README_FILE_PATH = "./README.md"

# 최신 글 개수
MAX_POST_COUNT = 5

def fetch_latest_blog_posts():
    feed = feedparser.parse(BLOG_URL)
    posts = []

    
    for entry in feed.entries[:MAX_POST_COUNT]:
        title = entry.title
        link = entry.link
		
        try:
            published_date_tuple = entry.published_parsed
            published_date = datetime(*published_date_tuple[:6]) # 년, 월, 일, 시, 분, 초만 사용
            formatted_date = published_date.strftime("%Y.%m.%d")
        except AttributeError:
            formatted_date = "Unknown Date"
        posts.append(f"- [{title}]({link}) ({formatted_date})")
    
    return posts

def update_readme(posts):
    with open(README_FILE_PATH, "r", encoding="utf-8") as readme_file:
        lines = readme_file.readlines()
    
    with open(README_FILE_PATH, "w", encoding="utf-8") as readme_file:
        in_blog_section = False
        for line in lines:
            # 삽입 위치 발견
            if line.strip() == "<!-- BLOG-POST-LIST:START -->":
                in_blog_section = True
                readme_file.write(line)
                for post in posts:
                    readme_file.write(f"{post}\n")
            # 종료 위치 발견
            elif line.strip() == "<!-- BLOG-POST-LIST:END -->":
                in_blog_section = False
                readme_file.write(line)
            # 나머지 출력
            elif not in_blog_section:
                readme_file.write(line)

        

if __name__ == "__main__":
    latest_posts = fetch_latest_blog_posts()
    update_readme(latest_posts)
