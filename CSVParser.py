import os
import csv

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

        return unique_projects
    else:
        print(f"File {filename} not found.")

# We now that the links start https://github.com/apache/{something}
def generate_github_links(project_name):
     # Remove 'apache' prefix and any leading '-' or '_'
    if project_name.startswith('apache'):
        project_name = project_name[6:]
        if project_name.startswith('-') or project_name.startswith('_'):
            project_name = project_name[1:] 
    github_link = f"https://github.com/apache/{project_name}"
    return github_link


# Defining main function
def main():
    input_file = "sonar_measures.csv"
    output_file = "parsed.csv"
    read_csv(input_file, output_file)
    print("Done")
    

# Using the special variable 
if __name__=="__main__":
    main()
