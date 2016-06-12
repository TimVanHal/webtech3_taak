from django.shortcuts import render
import urllib2, json, urllib, os, zipfile, shutil

base_url = 'https://api.github.com/repos/'
basedir = "C:\github_app\download\\"
auth = '?client_id=db755be5ca0c733d4e26&client_secret=0ba906013f2752490a6839718fdbe41f58912927'

def get_commits(repo):
	data = {}
	commit_list = []
	get_url = base_url + repo + '/commits' + auth
	response = urllib2.urlopen(get_url)
	data = json.load(response)
	for commit in data:
		com = {}
		com['repo'] = repo
		committer = commit['commit']['committer']
		com['date'] = committer['date']
		com['name'] = committer['name']
		com['email'] = committer['email']
		com['message'] = commit['commit']['message']
		com['sha'] = commit['sha']
		commit_list.append(com)
	return commit_list

def get_files(repo, sha):
	data = {}
	file_list = []
	get_url = base_url + repo + '/commits/' + sha + auth
	response = urllib2.urlopen(get_url)
	data = json.load(response)
	files = data['files']
	for file in files:
		filedata = {}
		filedata['name'] = file['filename']
		filedata['status'] = file['status']
		file_list.append(filedata)
	return file_list

def get_top_ten(repo):
	commits = get_commits(repo)
	files = []
	for commit in commits:
		sha = commit['sha']
		temp_files = get_files(repo, sha)
		for file in temp_files:
			files.append(file)
	changelist = count_commits(files)
	sorted_list = sorted(changelist, key=lambda k : k['count'])[::-1]
	sorted_list = sorted_list[:10]
	return sorted_list


def count_commits(files):
	uniquefiles = []
	changelist = []
	for file in files:
		if file['name'] not in uniquefiles:
			uniquefiles.append(file['name'])
			temp = {}
			temp['name'] = file['name']
			temp['count'] = 1
			changelist.append(temp)
		else: # File is modified.
			listed_file = filter(lambda lfile: lfile['name'] == file['name'], changelist)[0]
			listed_file['count'] += 1
	return changelist

def download(repository):
	get_url = base_url + repository + '/zipball/master' + auth
	[user, rep] = repository.split('/')
	filename = basedir + user + '\\' + rep + '.zip'
	response = urllib.urlretrieve(get_url, filename)
	extract_dir = basedir + user + '\\' + rep
	if not os.path.exists(extract_dir):
		os.makedirs(extract_dir)
	else: #folder bestaat al, eerst oude versie verwijderen, vooraleer nieuwe versie upzippen
		for file in os.listdir(extract_dir):
			file_path = os.path.join(extract_dir, file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print(e)
	zip = zipfile.ZipFile(filename, 'r')
	zip.extractall(extract_dir)
	zip.close()

def create_dirs(user):
	app_dir = 'C:\github_app'
	dl_dir = app_dir + '\download'
	user_dir = dl_dir + '\\' + user
	if not os.path.exists(app_dir):
		os.makedirs(app_dir)
	if not os.path.exists(dl_dir):
		os.makedirs(dl_dir)
	if not os.path.exists(user_dir):
		os.makedirs(user_dir)

# Create your views here.
def index(request):
	return render(request, 'github_app/index.html')

def list(request):
	if request.method == "POST":
		commits = []
		list = request.POST.get('list')
		get_list = list.split('\r\n')
		for repo in get_list:
			user = repo.split('/')[0]
			create_dirs(user)
			download(repo)
			repo_commits = get_commits(repo)
			for com in repo_commits:
				commits.append(com)
		return render(request, 'github_app/list.html', {'data' : commits})
	return render(request, 'github_app/list.html')

def detail(request, user, rep):
	repo = user + '/' + rep
	top = get_top_ten(repo)
	return render(request, 'github_app/detail.html', {'files' : top})