# Input: parsed/
# Output: CSV for each platform (with the URL, dir, and file name); all_file_urls.json (with all files regardless of platform URLs)
# Notes: Also created repo_urls.json with only files that contain a platform URL

import json
import os
import re
import csv

sourceforge = open("repo_results/pmc_sourceforge.csv", "w")
github = open("repo_results/pmc_github.csv", "w")
gitlab = open("repo_results/pmc_gitlab.csv", "w")
bitbucket = open("repo_results/pmc_bitbucket.csv", "w")
has_repo_json = open("repo_results/pmc_repo_urls.json", "w")
all_files_json = open("repo_results/pmc_all_file_urls.json", "w")
csv_file2 = open("./data_processing/pmc_file_count.csv", "w")
csvwriter2 = csv.writer(csv_file2)
csvwriter2.writerow(['Directory', 'FileCount', 'FileWithURL'])

def url_union(repo_dict):
    repo_all = list(set(repo_dict["annot_urls"]).union(set(repo_dict["text_urls"])))
    return repo_all

def update_dict(dir_dict, repo_all, repo_dict):
    repo_dict["all_urls"] = repo_all
    repo_dict["url_count"] = len(repo_all)
    dir_dict["annot_urls"].extend(repo_dict["annot_urls"])
    dir_dict["text_urls"].extend(repo_dict["text_urls"])
    dir_dict["all_urls"].extend(repo_all)
    dir_dict["url_count"] = dir_dict["url_count"] + len(repo_all)
    return repo_dict

has_repo_data = {}
all_files_data = {}
total_all_files = 0
total_url_files = 0

file_list = os.listdir("pmc_parsed/")
for file_name in file_list:
    dir = re.findall(r"(\d{6}).json", file_name)[0]
    has_repo_data[dir] = {"files":{}}
    all_files_data[dir] = {"files":{}}
    print(file_name)
    f = open("pmc_parsed/" + file_name, "r")
    json_data = json.load(f)

    all_dir_sourceforge_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    repo_dir_sourceforge_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    all_dir_github_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    repo_dir_github_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    all_dir_gitlab_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    repo_dir_gitlab_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    all_dir_bitbucket_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    repo_dir_bitbucket_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}

    all_files = 0
    url_files = 0
    for pdf_name in json_data[dir]["files"]:
        all_files = all_files + 1
        if json_data[dir]["files"][pdf_name]["url_count"] != 0:
            url_files = url_files + 1
        annot_urls = json_data[dir]["files"][pdf_name]["annot_urls"]
        text_urls = json_data[dir]["files"][pdf_name]["text_urls"]

        sourceforge_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
        github_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
        gitlab_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
        bitbucket_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}

        for url in annot_urls:
            sf = re.search(r"(sourceforge.net)", url)
            if sf is not None:
                sourceforge_dict["annot_urls"].append(url)
                sourceforge.write(url + " " + dir + " " + pdf_name + "\n")

            gh = re.search(r"(github.com|github.io)", url)
            if gh is not None:
                github_dict["annot_urls"].append(url)
                github.write(url + " " + dir + " " + pdf_name + "\n")
            
            gl = re.search(r"(gitlab.com|gitlab.io)", url)
            if gl is not None:
                gitlab_dict["annot_urls"].append(url)
                gitlab.write(url + " " + dir + " " + pdf_name + "\n")
            
            bb = re.search(r"(bitbucket.org)", url)
            if bb is not None:
                bitbucket_dict["annot_urls"].append(url)
                bitbucket.write(url + " " + dir + " " + pdf_name + "\n")
        
        for url in text_urls:
            sf = re.search(r"(sourceforge.net)", url)
            if sf is not None:
                sourceforge_dict["text_urls"].append(url)
                sourceforge.write(url + " " + dir + " " + pdf_name + "\n")

            gh = re.search(r"(github.com|github.io)", url)
            if gh is not None:
                github_dict["text_urls"].append(url)
                github.write(url + " " + dir + " " + pdf_name + "\n")
            
            gl = re.search(r"(gitlab.com|gitlab.io)", url)
            if gl is not None:
                gitlab_dict["text_urls"].append(url)
                gitlab.write(url + " " + dir + " " + pdf_name + "\n")
            
            bb = re.search(r"(bitbucket.org)", url)
            if bb is not None:
                bitbucket_dict["text_urls"].append(url)
                bitbucket.write(url + " " + dir + " " + pdf_name + "\n")
        
        sourceforge_all = url_union(sourceforge_dict)
        github_all = url_union(github_dict)
        gitlab_all = url_union(gitlab_dict)
        bitbucket_all = url_union(bitbucket_dict)

        all_files_data[dir]["files"][pdf_name] = {}
        all_sourceforge_dict = update_dict(all_dir_sourceforge_dict, sourceforge_all, sourceforge_dict)
        all_files_data[dir]["files"][pdf_name]["sourceforge"] = all_sourceforge_dict
        all_github_dict = update_dict(all_dir_github_dict, github_all, github_dict)
        all_files_data[dir]["files"][pdf_name]["github"] = all_github_dict
        all_gitlab_dict = update_dict(all_dir_gitlab_dict, gitlab_all, gitlab_dict)
        all_files_data[dir]["files"][pdf_name]["gitlab"] = all_gitlab_dict
        all_bitbucket_dict = update_dict(all_dir_bitbucket_dict, bitbucket_all, bitbucket_dict)
        all_files_data[dir]["files"][pdf_name]["bitbucket"] = all_bitbucket_dict

        if len(sourceforge_all) + len(github_all) + len(gitlab_all) + len(bitbucket_all) != 0:
            has_repo_data[dir]["files"][pdf_name] = {}
            if len(sourceforge_all) != 0:
                repo_sourceforge_dict = update_dict(repo_dir_sourceforge_dict, sourceforge_all, sourceforge_dict)
                has_repo_data[dir]["files"][pdf_name]["sourceforge"] = repo_sourceforge_dict
            if len(github_all) != 0:
                repo_github_dict = update_dict(repo_dir_github_dict, github_all, github_dict)
                has_repo_data[dir]["files"][pdf_name]["github"] = repo_github_dict
            if len(gitlab_all) != 0:
                repo_gitlab_dict = update_dict(repo_dir_gitlab_dict, gitlab_all, gitlab_dict)
                has_repo_data[dir]["files"][pdf_name]["gitlab"] = repo_gitlab_dict
            if len(bitbucket_all) != 0:
                repo_bitbucket_dict = update_dict(repo_dir_bitbucket_dict, bitbucket_all, bitbucket_dict)
                has_repo_data[dir]["files"][pdf_name]["bitbucket"] = repo_bitbucket_dict
        
    all_files_data[dir]["sourceforge"] = all_dir_sourceforge_dict
    has_repo_data[dir]["sourceforge"] = repo_dir_sourceforge_dict
    all_files_data[dir]["github"] = all_dir_github_dict
    has_repo_data[dir]["github"] = repo_dir_github_dict
    all_files_data[dir]["gitlab"] = all_dir_gitlab_dict
    has_repo_data[dir]["gitlab"] = repo_dir_gitlab_dict
    all_files_data[dir]["bitbucket"] = all_dir_bitbucket_dict
    has_repo_data[dir]["bitbucket"] = repo_dir_bitbucket_dict

    csvwriter2.writerow(["20" + dir[0:2] + "-" + dir[2:], all_files, url_files])
    total_all_files = total_all_files + all_files
    total_url_files = total_url_files + url_files

json.dump(all_files_data, all_files_json)
json.dump(has_repo_data, has_repo_json)
has_repo_json.close()
all_files_json.close()
sourceforge.close()
github.close()
gitlab.close()
bitbucket.close()
csv_file2.close()

print("Total number of files: " + str(total_all_files))
print("Files with URLs: " + str(total_url_files))