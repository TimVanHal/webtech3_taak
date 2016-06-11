from django.shortcuts import render
import urllib2, json

base_url = 'https://api.github.com/repos/'

def get_commits(repo):
	data = {}
	commit_list = []
	get_url = base_url + repo + '/commits'
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
		commit_list.append(com)
	return commit_list

# Create your views here.
def index(request):
	return render(request, 'github_app/index.html')

def list(request):
	if request.method == "POST":
		commits = []
		list = request.POST.get('list')
		get_list = list.split('\r\n')
		for repo in get_list:
			repo_commits = get_commits(repo)
			for com in repo_commits:
				commits.append(com)
		return render(request, 'github_app/list.html', {'data' : commits})
	return render(request, 'github_app/list.html')

def detail(request):
	return HttpResponse("details")