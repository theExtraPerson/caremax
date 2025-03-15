# python script for handling forms
# create forms for user registration
# forms for provider registration

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import Length

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')


# labtest order forms
class OrderForm(FlaskForm):
    test_type = SelectField('Test Type', choices=[
        ('whole_genome', 'Whole Genome Sequencing'),
        ('whole_exome', 'Whole Exome Sequencing')
    ])
    submit = SubmitField('Order Test')

class ArticleUploadForm(FlaskForm):
    title = StringField('Title', validators=[Length(0, 128)])
    clinic = StringField('Clinic', validators=[Length(0, 128)])
    pdf = StringField('PDF Path', validators=[Length(0, 256)])
    submit = SubmitField('Upload Article')

# rare disease registry form
class RareDiseaseRegistryForm(FlaskForm):
    pass

# medical report form
class MedicalReportForm(FlaskForm):
    pass

# medical personnel registration form



