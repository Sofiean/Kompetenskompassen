import requests
import zipfile
import json
import csv
import io
from collections import Counter, defaultdict

def extract_skills_with_count(year, jsonl_file, existing_skills_with_count=None):
    skills_counter = Counter()
    occupation_skills_counter = defaultdict(Counter)

    if existing_skills_with_count:
        # Load existing skills with count
        for skill, count in existing_skills_with_count.items():
            skills_counter[skill] += count

    for line in jsonl_file:
        data = json.loads(line)
        enriched_skills = data.get("keywords", {}).get("enriched", {}).get("skill", [])
        occupation_field = data.get("occupation_field", [{}])[0].get("label", "")
        municipality = data.get("workplace_address", {}).get("municipality", "")

        if enriched_skills and occupation_field and municipality:
            skills = [skill.strip() for skill in enriched_skills]
            skills_counter.update(skills)
            occupation_skills_counter[(occupation_field, municipality)].update(skills)

    return skills_counter, occupation_skills_counter

def write_to_csv(occupation_skills_counter, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Occupation Field', 'Municipality', 'Skill', 'Count'])

        for (occupation_field, municipality), skill_counts in occupation_skills_counter.items():
            for skill, count in skill_counts.most_common(10):  # Justera antalet beroende på behov
                writer.writerow([occupation_field, municipality, skill, count])

years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

lines = 0

for year in years:
    url = f"https://data.jobtechdev.se/annonser/historiska/berikade/kompletta/{year}_beta1_jsonl.zip"
    csv_file_path = f"./skills_by_occupation_update{year}.csv"

    existing_skills_with_count = {}

    response = requests.get(url)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        file_name = zip_file.namelist()[0]
        with zip_file.open(file_name) as jsonl_file:
            unique_skills_with_count, occupation_skills_counter = extract_skills_with_count(year, jsonl_file, existing_skills_with_count)

    write_to_csv(occupation_skills_counter, csv_file_path)

    line_count = len(occupation_skills_counter)
    lines += line_count

print("Number of lines in the CSV files:", lines)
