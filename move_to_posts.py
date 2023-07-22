#!/usr/local/bin/python3
import sys
import os
from json import dumps
from datetime import date


def full_month(month: str):
	return {
		"Jan": "01Jan",
		"Feb": "02Feb",
		"Mar": "03Mar",
		"Apr": "04Apr",
		"May": "05May",
		"Jun": "06Jun",
		"Jul": "07Jul",
		"Aug": "08Aug",
		"Sep": "09Sep",
		"Oct": "10Oct",
		"Nov": "11Nov",
		"Dec": "12Dec",
	}[month.title()]


def move_to_post(filename: str, year: int, month: str, day: int, updated: date, tags: list[str], author: str, title: str, description: str):
	with open(filename) as file:
		body = str(file.read())

	post_dir = "Posts/" + str(year) + "/" + month
	post_file = post_dir + "/" + str(day)
	os.makedirs(post_dir, exist_ok=True)

	file_json = {
		"author": author,
		"title": title,
		"body": body,
		"tags": tags,
		"description": description,
		"updated": updated.strftime("%m/%d/%Y"),
	}

	with open(post_file, 'w') as file:
		file.write(dumps(file_json))


if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print("Pass a file to add to the blog: e.g. " + sys.argv[0] + " 'new_post'")
		exit(1)

	year = int(input("What year is this post going to be posted? "))
	month = input("Enter the first three letters of the month this is going to be posted (e.g. Apr): ")
	day = int(input("What day is this post going to be posted? "))
	if day < 1 or day > 31:
		print("Invalid day " + str(day))
		exit(1)

	title = input("What is the title of this post? ")
	description = input("What one-line description should this post have?\n")
	tags = input("Enter a comma-separated list of tags: ")
	now = date.today()

	move_to_post(sys.argv[1], year, month, day, now, tags.split(","), "Donnie", title, description)
