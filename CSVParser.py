import os
import csv
import subprocess 




# Open and read the CSV file
def read_csv(filename, output_filename):
    unique_projects = set() 
    unique_rows = []

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf8") as file:
            reader = csv.reader(file)
            unique_rows.append(["Organization", "Project Name", "Github Link"])  # New headers

            # Read each row in the CSV file
            for row in reader:
                organization = row[0]
                project_name = row[1]

                # Checking if the project is already added
                if project_name not in unique_projects:
                    unique_projects.add(project_name)
                    # Generate GitHub link for the project
                    github_link = generate_github_links(project_name)
                    unique_rows.append([organization, project_name, github_link])
        
        # Writing the CSV File for unique projects with Github links
        with open(output_filename, "w", encoding="utf8", newline='') as output_file:
            writer = csv.writer(output_file)
            # Write all unique rows to the new file
            writer.writerows(unique_rows)

        print(r"Total Unique Projects %d" % len(unique_projects))
        return unique_projects
    else:
        print(f"File {filename} not found.")
        return

# We know that the links start with https://github.com/apache/{something}
def generate_github_links(project_name):
     # Remove 'apache' prefix and any leading '-' or '_'
    if project_name.startswith('apache'):
        project_name = project_name[6:]
        if project_name.startswith('-') or project_name.startswith('_'):
            project_name = project_name[1:] 
    github_link = f"https://github.com/apache/{project_name}"
    return github_link

# Fetching the clone of GitHub repositories from CSV GitHub link
def fetch_github_repo_clone(output, clone_root_dir, unique_projects_count):
    failed = 0
    succeed = 0
    total_links = len(unique_projects_count)
    count = 0
    try:
        with open(output, "r", encoding="utf8") as github_links: 
            # Create a directory to store cloned repos
            try: os.makedirs(clone_root_dir, exist_ok=True)
            except FileExistsError: print(f"Directory {clone_root_dir} already exists.")

            # Starting to clone the GitHub repositories
            csv_reader = csv.reader(github_links)
            next(csv_reader)
            # Loop each repository
            for links in csv_reader:
                print(f"\nRepo {count}/{total_links}")
                print(f"Cloning repository: {links[2]}")

                # Check if repository already cloned
                repo_name = links[0].rstrip('/').split('/')[-1]
                clone_dir = os.path.join(clone_root_dir, repo_name)
                if os.path.exists(clone_dir):
                    print(f"Repository {repo_name} already cloned.")
                    continue

                # Clone the repository
                result = subprocess.run(["git", "clone", links[2]], cwd=clone_root_dir)
                if result.returncode != 0:
                    failed += 1
                else:
                    succeed += 1
                count += 1

        print(f"\nSuccessfully cloned {succeed}/{total_links}")
        if(failed > 0):
            print(f"Failed cloned {failed}/{total_links}")
    except FileNotFoundError:
        print(f"\nFile {output} not found!")
# Defining main function
def main():
    input_file = "sonar_measures.csv"
    output_file = "parsed.csv"
    clone_root_dir = "cloned_repos"
    unique_project_count = read_csv(input_file, output_file)
    fetch_github_repo_clone(output_file, clone_root_dir, unique_project_count)

# Using the special variable 
if __name__=="__main__":
    main()
