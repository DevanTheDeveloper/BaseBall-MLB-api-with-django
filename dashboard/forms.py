from django import forms
from .models import Uploads

class FileForm(forms.ModelForm):
	class Meta:
		model = Uploads 
		fields = ['title','file']



'''
#	def validate_file(self):
#		try:
#			file = self.cleaned_data.get("file")
#			if not file.endswith('.csv'):
#				raise forms.ValidationError("This is not a csv")
#		except:
	#		return False
#		return True'''