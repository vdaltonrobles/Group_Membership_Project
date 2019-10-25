from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Group

# Create your views here.
def index(request):
	return redirect('/main')

def main(request):
	return render(request, 'main.html')

def register(request):
	errors = User.objects.registerValidator(request.POST)
	print(errors)
	print(len(errors))
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/main')
	userPwd = request.POST['password']
	hashedPwd = bcrypt.hashpw(userPwd.encode(), bcrypt.gensalt())
	print(hashedPwd)
	newuser = User.objects.create(firstname=request.POST['fname'], lastname = request.POST['lname'], email=request.POST['email'], password=hashedPwd.decode())
	request.session['userID'] = newuser.id
	return redirect('/main')

def login(request):
	print(request.POST)
	errors = User.objects.loginValidator(request.POST)
	print(errors)
	print(len(errors))
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/main')
	user = User.objects.filter(email=request.POST['email'])
	print(user)
	user = user[0]
	print(user)
	request.session['userID'] = user.id
	print(user)
	return redirect('/groups')

def groups(request):
	loggedInUser = User.objects.get(id=request.session['userID'])
	context = {
		'loggedInUser': User.objects.get(id=request.session['userID']),
		'groupList': Group.objects.all(),
		
	}
	return render(request, 'groups.html', context)

def create_org(request):
	print(request.POST)
	errors = Group.objects.groupValidator(request.POST)
	print(errors)
	print(len(errors))
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/groups')
	loggedInUser = User.objects.get(id=request.session['userID'])
	newgroup = Group.objects.create(organization_name=request.POST['org_name'], description=request.POST['desc'], creator=loggedInUser)
	print(newgroup)
	newgroup.member.add(loggedInUser)
	return redirect('/groups')

def groupPage(request, group_id):
	context = {
		'loggedInUser': User.objects.get(id=request.session['userID']),
		'groupList': Group.objects.filter(id=group_id),
	}
	return render(request, 'page.html', context)

def deleteGroup(request, group_id):
	groupSelected = Group.objects.get(id=group_id)
	groupSelected.delete()
	return redirect('/groups')

def joinGroup(request, group_id):
	loggedInUser = User.objects.get(id=request.session['userID'])
	groupToJoin = Group.objects.get(id=group_id)
	loggedInUser.joined.add(groupToJoin)
	return redirect('/groups/' + group_id)

def leaveGroup(request, group_id):
	loggedInUser = User.objects.get(id=request.session['userID'])
	groupToLeave = Group.objects.get(id=group_id)
	loggedInUser.joined.remove(groupToLeave)
	return redirect ('/groups/' + group_id)

def logout(request):
	request.session.clear()
	return redirect('/main')

