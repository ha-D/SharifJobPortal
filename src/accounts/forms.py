# coding=utf-8

from django						import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms 	import UserCreationForm
from django.conf 				import settings

from uuid 						import uuid1

from accounts.models 			import JobSeeker, Employer, UserProfile, CompanyImage

class ChangeJobseekerInfoForm(forms.ModelForm):
	class Meta:
		model = JobSeeker
		fields = ('job_status', 'cv',)

class ChangeCompanyInfoForm(forms.ModelForm):
	class Meta:
		model = Employer
		exclude = ('user',)

class CompanyImageUploadForm(forms.ModelForm):
	class Meta:
		model = CompanyImage
		fields = ('image',)

class ChangeUserInfoForm(forms.ModelForm):
	first_name = forms.CharField(max_length = 100, label="نام")
	last_name = forms.CharField(max_length = 100, label="نام خانوادگی")

	email = forms.EmailField(label="آدرس الکترونیکی")

	class Meta:
		model = UserProfile
		fields = ('address', 'postalCode', 'phoneNumber', 'city', 'image')

	def __init__(self, *args, **kwargs):
		if 'instance' in kwargs:
			user =  kwargs['instance'].user
			fields = {
				'first_name': user.first_name,
				'last_name': user.last_name,
				'email': user.email
			}
			super(ChangeUserInfoForm, self).__init__(initial=fields,*args, **kwargs)
		else:
			super(ChangeUserInfoForm, self).__init__(*args, **kwargs)

	def save(self):
		profile = super(ChangeUserInfoForm, self).save(commit=True)
		user = profile.user
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.save()




########################
#### Register Forms ####
########################

class RegisterUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):

		super(RegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True
		
		self.fields['password1'].widget = forms.PasswordInput()

		placeholders = {
			'first_name': 'نام',
			'last_name':  'نام خانوادگی',
			'username':   'نام کاربری',
			'email':	  'آدرس الکترونیکی',
			'password1':	  'رمز عبور',
			'password2': 'تکرار رمز عبور'
		}

		for field in placeholders:
			self.fields[field].widget.attrs.update({'placeholder': placeholders[field]})


class JobSeekerRegisterProfileForm(forms.ModelForm):
	class Meta:
		model = JobSeeker
		fields = ['sex', 'address', 'postalCode', 'phoneNumber', 'city', 'birthDate']

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

	def save_file(self, filename):
		with open(settings.MEDIA_ROOT + 'cv/%s' % filename, 'wb+') as destination:
			for chunk in self.cleaned_data['cv'].chunks():
				destination.write(chunk)

	def save(self, commit = False):
		jobseeker = super(JobSeekerRegisterWorkForm, self).save(commit = False)
		
		filename = str(uuid1())[:8] + '.pdf'
		self.save_file(filename)
		jobseeker.cv_filename = filename
	
		return jobseeker

class RegisterFinalForm(forms.Form):
	terms = forms.BooleanField()

	def save(self, commit=False):
		return True

class EmployerRegisterProfileForm(forms.ModelForm):
	class Meta:
		model = Employer
		fields = ['address', 'postalCode', 'phoneNumber', 'city', 'webSite',
				  'companyName', 'companyType', 'registrationNumber', 'contactEmail', 'establishDate']

	def __init__(self, *args, **kwargs):
		super(EmployerRegisterProfileForm, self).__init__(*args, **kwargs)

	# def save(self):
	# 	employer = super(EmployerRegisterProfileForm, self).save(commit = False)

	# 	return employer
