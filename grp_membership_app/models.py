from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def registerValidator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['fname']) < 2:
			errors['fnameErr'] = "Your first name must be 2 or more characters."
		if len(postData['lname']) < 2:
			errors['lnameErr'] = "Your last name must be 2 or more characters."
		if not EMAIL_REGEX.match(postData['email']):
			errors['emailErr'] = "Invalid email address!"
		else:
			email_taken = User.objects.filter(email=postData['email'])
			print(email_taken)
			if len(email_taken) > 0:
				errors['emailTakenErr'] = "This email address already exists, please enter a different email address"
		if len(postData['password']) < 1:
			errors['pwdErr'] = "You must enter a password!"
		if len(postData['password']) < 8:
			errors['pwdErr'] = "Your password must be at least 8 characters."
		return errors

	def loginValidator(self, postData):
		errors = {}
		if len(postData['email']) < 1:
			errors['noEmailEnteredErr'] = "Please enter a valid email address and password."
		else:
			userInDB = User.objects.filter(email=postData['email'])
			if not userInDB:
				errors['notInDBErr'] = "Please enter a valid email address and password or register to create an account."
			else:
				loggedUser = userInDB[0]
				userPwd = (postData['password'])
				if bcrypt.checkpw(userPwd.encode(), loggedUser.password.encode()):
					print("password match")
				else:
					print("failed password")
					errors['badPwd'] = "Incorrect email address or password."
		return errors

class GroupManager(models.Manager):
	def groupValidator(self, postData):
		errors= {}
		if len(postData['org_name']) < 1:
			errors['orgNameShortErr'] = "Please enter an organization name."
		if len(postData['org_name']) < 6:
			errors['orgNameShortErr'] = "Organization name must be more than 5 characters long."
		if len(postData['desc']) < 1:
			errors['descShortErr'] = "Please enter a description"
		if len(postData['desc']) < 11:
			errors['descShortErr'] = "Description must be more than 10 characters long."
		return errors

# Create your models here.
class User(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	def __repr__(self):
		return f"<User object: {self.firstname} ({self.id})>"
	# group_created = a list of groups the user created
	# joined = a list of groups the user joined

class Group(models.Model):
	organization_name = models.CharField(max_length=45)
	description = models.TextField()
	creator = models.ForeignKey(User, related_name="group_created", on_delete=models.CASCADE)
	# group_created = a list of groups created by the user
	member = models.ManyToManyField(User, related_name="joined")
	# joined = a list of users who joined a group
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = GroupManager()
	def __repr__(self):
		return f"<Group object: {self.organization_name} ({self.id})>"
