# coding=utf-8

from django						import forms
from django.contrib.auth.models import User
from accounts.models 			import JobSeeker, Employer

class JobSeekerRegisterUserForm(forms.ModelForm):
	password_repeat = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password']

	def __init__(self, *args, **kwargs):

		super(JobSeekerRegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True
		
		self.fields['password'].widget = forms.PasswordInput()

		placeholders = {
			'first_name': 'نام',
			'last_name':  'نام خواندوادگی',
			'username':   'نام کاربری',
			'email':	  'آدرس الکترونیکی',
			'password':	  'رمز عبور',
			'password_repeat': 'تکرار رمز عبور'
		}

		for field in placeholders:
			self.fields[field].widget.attrs.update({'placeholder': placeholders[field]})

	def save(self, commit=True):
		user = super(JobSeekerRegisterUserForm, self).save(commit = False)
		
		# TODO make inactive
		user.active = False
		
		if commit:
			user.save()

		return user



class JobSeekerRegisterProfileForm(forms.ModelForm):
	class Meta:
		model = JobSeeker
		fields = ['address', 'postalCode', 'phoneNumber', 'city', 'birthDate']

	def __init__(self, *args, **kwargs):
		super(JobSeekerRegisterProfileForm, self).__init__(*args, **kwargs)

	def save(self, commit = False, user = None):
		jobseeker = super(JobSeekerRegisterProfileForm, self).save(commit = False)

		if user != None:
			jobseeker.user = user

		if commit:
			jobseeker.save()

		return jobseeker

class JobSeekerRegisterWorkForm(forms.ModelForm):
	class Meta:
		model = JobSeeker
		fields = ['job_status', 'cv']

	def save(self, commit = False):
		jobseeker = super(JobSeekerRegisterWorkForm, self).save(commit = False)
		
		# jobseeker.job_status = newseeker.job_status
		# jobseeker.cv = newseeker.cv

		if commit:
			jobseeker.save()

		return jobseeker

class JobSeekerRegisterFinalForm(forms.Form):
	terms = forms.BooleanField()

	def save(self):
		return None