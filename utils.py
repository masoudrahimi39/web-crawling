import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        print(f'creating project: {directory}')
        os.makedirs(directory)
        

# creat queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'   # list of link in the waiting list to be crawled
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

def write_file(path, data):
    ''' create a new file'''
    with open(path, 'w') as f:
        f.write(data)

def append_to_file(path, data):
    with open(path, 'a') as f:
        f.write(data + '\n')

# delete contenc of a file
def delete_file_content(path):
    # print(path)
    with open(path, 'w'):
        # do nothing so the content will be overwritten with nothing
        pass

# read a file and conver each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_content(file)
    for link in sorted(links):
        append_to_file(file, link)
    


