# Input: repo_urls.json
# Output: urls_per_file.csv (directory, average # of URLs per file, category)
# Notes: Similar to dir_urls.py but generates the average # of URLs per file instead of total

import json
import csv

repo_file = open("./repo_results/pmc_repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("./data_processing/pmc_urls_per_file.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Directory', 'URICount', 'Category'])

total_file_count = 0
total_url_count = 0
total_sourceforge_count = 0
total_github_count = 0
total_gitlab_count = 0
total_bitbucket_count = 0
for dir in repo_json:
    sourceforge_count = repo_json[dir]["sourceforge"]["url_count"]
    github_count = repo_json[dir]["github"]["url_count"]
    gitlab_count = repo_json[dir]["gitlab"]["url_count"]
    bitbucket_count = repo_json[dir]["bitbucket"]["url_count"]
    total_sourceforge_count = total_sourceforge_count + sourceforge_count
    total_github_count = total_github_count + github_count
    total_gitlab_count = total_gitlab_count + gitlab_count
    total_bitbucket_count = total_bitbucket_count + bitbucket_count
    dir_file = open("pmc_parsed/" + dir + ".json")
    dir_json = json.load(dir_file)
    dir_file.close()
    dir_count = 0
    file_count = 0
    for file in dir_json[dir]["files"]:
        file_count = file_count + 1
        dir_count = dir_count + dir_json[dir]["files"][file]["url_count"]
    total_file_count = total_file_count + file_count
    total_url_count = total_url_count + dir_count
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], dir_count/file_count, "Total"])
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], sourceforge_count/file_count, "SourceForge"])
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], github_count/file_count, "GitHub"])
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], gitlab_count/file_count, "GitLab"])
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], bitbucket_count/file_count, "Bitbucket"])
print("Total file count: " + str(total_file_count))
print("Total URL count: " + str(total_url_count))
print("SourceForge count: " + str(total_sourceforge_count))
print("GitHub count: " + str(total_github_count))
print("GitLab count: " + str(total_gitlab_count))
print("Bitbucket count: " + str(total_bitbucket_count))
csv_file.close()