#!/usr/local/bin/python3

import sys
import os
import json

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
                {"day": day, "titles": titles} for day, titles in sorted(days.items())]
             } for month, days in sorted(months.items())]
         } for year, months in sorted(all_posts.items())]
    with open(POSTS_FILE, 'w') as f:
        f.write(json.dumps(all_posts_sorted))


def generate_rss_feed() -> None:
    try:
        f = open(RSS_FILE, 'w')
    except Exception as e:
        print("Cannot find rss file " + RSS_FILE)
        print(e)
        sys.exit(1)

    f.write('<?xml version="1.0"?>\n')
    f.write('<rss version="2.0" xmlns:atom=http://www.w3.org/2005/Atom">\n\n')
    f.write('<channel>\n\t<title>The Blog of a Math Nerd</title>\n')
    f.write('\t<description>Sports, math, programming</description>\n')
    f.write('\t<atom:link href=https://thedadams.com/feed.rss" rel="self" \
            type="application/rss+xml"/>\n')
    f.write('\t<link>https://thedadams.com/Blog.html</link>\n')
    f.write('\t<copyright>&#169; Donnie Adams</copyright>\n')
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
                f.write('\n\t<item>\n\n')
                f.write('\t\t<title>' + file_json["title"] + '</title>\n')
                f.write(
                    '\t\t<description><![CDATA[' +
                    file_json["body"].replace(
                        'href="/Post.html?post=',
                        'href="https://thedadams.com/Post.html?post=', -1
                    ) + ']]></description>\n'
                )
                f.write('\t\t<link>https://thedadams.com/Post.html?post=' +
                        year + '-' + month + '-' + d +
                        '</link>\n'
                        )
                f.write(
                    '\t\t<guid isPermaLink="false">\
                    https://thedadams.com/Post.html?post=' +
                    year + '-' + month + '-' + d +
                    '</guid>\n'
                )
                f.write(
                    '\t\t<pubDate>' +
                    month[2:] + ' ' + d + ' ' + year +
                    '</pubDate>\n\n')
                f.write('\t</item>\n\n')
                file.close()
                num += 1

                if num == 25:
                    done = True
                    break
            if done:
                break
        if done:
            break
    f.write('</channel>\n\n</rss>')
    f.close()


generate_tag_post_file()
generate_rss_feed()
