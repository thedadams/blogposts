#!/usr/local/bin/python3

import sys
import os
import json
from datetime import datetime
from html import escape

POST_ROOT = "Posts/"
RSS_FILE = "feed.rss"
POST_TAGS_FILE = "PostTags.json"
POSTS_FILE = "Posts.json"


def generate_tag_post_file() -> None:
    all_tags = {}
    all_posts = {}
    for directory, _, files in os.walk(POST_ROOT):
        for day in files:
            year = directory.lstrip(POST_ROOT)
            year, month = year.split("/")
            tag_date = year[:4] + "-" + month + "-" + day
            post_json = {}
            with open(directory + "/" + day, "r") as f:
                post_json = json.loads(f.read())

            for tag in post_json["tags"]:
                if tag not in all_tags:
                    all_tags[tag] = {}
                if post_json["title"] not in all_tags[tag]:
                    all_tags[tag][post_json["title"]] = tag_date

            if year not in all_posts:
                all_posts[year] = {}
            if month not in all_posts[year]:
                all_posts[year][month] = {}
            if day not in all_posts[year][month]:
                all_posts[year][month][day] = []
            all_posts[year][month][day].append(post_json["title"])

    with open(POST_TAGS_FILE, 'w') as f:
        f.write(json.dumps(all_tags))

    all_posts_sorted = [
        {"year": year, "months": [
            {"month": month, "days": [
                {"day": day, "titles": titles} for day, titles in sorted(days.items(), reverse=True)]
             } for month, days in sorted(months.items(), reverse=True)]
         } for year, months in sorted(all_posts.items(), reverse=True)]
    with open(POSTS_FILE, 'w') as f:
        f.write(json.dumps(all_posts_sorted))


def generate_rss_feed() -> None:
    try:
        f = open(RSS_FILE, 'w')
    except Exception as e:
        print("Cannot find rss file " + RSS_FILE)
        print(e)
        sys.exit(1)

    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write('<rss xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom/" xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">')
    f.write('<channel><title>The Blog of a Math Nerd</title>')
    f.write('<description>Sports, math, programming</description>')
    f.write('<link>https://thedadams.com/blog.html</link>')
    f.write('<atom:link href="https://raw.githubusercontent.com/thedadams/blogposts/main/feed.rss" rel="self" type="application/rss+xml" />')
    f.write('<copyright>&#169; Donnie Adams</copyright>')
    years = os.listdir(POST_ROOT)
    years.sort(reverse=True)
    num = 0
    done = False
    for year in years:
        if os.path.isfile(POST_ROOT + year):
            continue
        months = os.listdir(POST_ROOT + year)
        months.sort(reverse=True)
        for month in months:
            if os.path.isfile(POST_ROOT + year + "/" + month):
                continue
            days = os.listdir(POST_ROOT + year + "/" + month)
            days.sort(reverse=True)
            for d in days:
                if done:
                    break
                if d == ".DS_Store":
                    continue

                file_json = {}
                with open(POST_ROOT + year + "/" + month + "/" + d) as file:
                    file_json = json.loads(file.read())
                f.write('<item>')
                f.write('<title>' + file_json.get("title", "") + '</title>')
                f.write('<description>'+ file_json.get("description", "") + '</description>')
                f.write('<content:encoded>' + escape(file_json.get("body", "").replace('href="blog.html?post=', 'href="https://thedadams.com/blog.html?post=', -1)) + '</content:encoded>')
                f.write('<link>https://thedadams.com/blog.html?post=' + year + '-' + month + '-' + d + '</link>')
                f.write('<guid isPermaLink="false">https://thedadams.com/blog.html?post=' + year + '-' + month + '-' + d + '</guid>')
                f.write('<pubDate>' + datetime(int(year), int(month[:2]), int(d), hour=12).strftime("%a, %d %b %Y %H:%M:%S GMT") + '</pubDate>')
                f.write('</item>')
                file.close()
                num += 1

                if num == 25:
                    done = True
                    break
            if done:
                break
        if done:
            break
    f.write('</channel></rss>')
    f.close()


generate_tag_post_file()
generate_rss_feed()
