from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Hospital, Doctor, Patient, Feedback, Ambulance, AmbulanceBooking, AffiliationRequest


# User Registration Form (For Patients)

class PatientRegistrationForm(UserCreationForm):
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[("M", "Male"), ("F", "Female")])
    address = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser  # Directly link to CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'age', 'gender', 'address', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "patient"  # Set role as patient
        if commit:
            user.save()
            # Create a Patient instance linked to this user (without medical history)
            Patient.objects.create(user=user, age=self.cleaned_data["age"],
                                   gender=self.cleaned_data["gender"],
                                   address=self.cleaned_data["address"],
                                   phone=self.cleaned_data["phone"])
        return user

# Hospital Registration Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Hospital

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Hospital


class HospitalRegistrationForm(UserCreationForm):
    hospital_name = forms.CharField(max_length=255, required=True, label="Hospital Name")
    description = forms.CharField(widget=forms.Textarea, required=True, label="Description")
    location = forms.CharField(max_length=255, required=True, label="Location")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "hospital_name", "description", "location"]

    def save(self, commit=True):  # ✅ Now it's inside the class
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = "hospital"  # ✅ Set role here
        user.is_active = False  # 🔒 inactive until approved
        if commit:
            user.save()
            Hospital.objects.create(
                user=user,
                name=self.cleaned_data["hospital_name"],
                description=self.cleaned_data["description"],
                location=self.cleaned_data["location"],
                is_approved=False
            )
        return user




# Doctor Registration Form
from django import forms
from .models import CustomUser, Doctor, Specialization


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Specialization


class DoctorRegistrationForm(UserCreationForm):
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=True,
        label="Specialization",
        empty_label="Select Specialization"
    )
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")
    license_number = forms.CharField(max_length=100, required=True, label="License Number")  # ✅ New field

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "specialization", "phone", "license_number"]

    def __init__(self, *args, **kwargs):
        self.hospital = kwargs.pop("hospital", None)  # ✅ Get hospital from view
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "doctor"  # ✅ Assign role
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                hospital=self.hospital,
                specialization=self.cleaned_data["specialization"],
                phone=self.cleaned_data["phone"],
                license_number=self.cleaned_data["license_number"]  # ✅ Save license number
            )
        return user



# Login Form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["age", "gender", "address", "phone", "medical_history", "profile_picture"]  # ✅ Include Profile Picture


from .models import Appointment

from django import forms
from .models import Appointment

from django import forms
from .models import Appointment
from .models import Doctor, Hospital


from django import forms
from .models import Appointment

from django import forms
from .models import Appointment


from django import forms
from django.utils import timezone  # ✅ Fixing the missing import
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'consultation_type', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # ✅ Calendar Selection
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),  # ✅ Time Picker
            'consultation_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.hospital_id = kwargs.pop('hospital_id', None)
        self.doctor_id = kwargs.pop('doctor_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Prevent duplicate bookings
        if Appointment.objects.filter(
            doctor_id=self.doctor_id,
            hospital_id=self.hospital_id,
            date=date,
            time=time
        ).exists():
            raise forms.ValidationError("This time slot is already booked for the selected doctor.")

        # Ensure the appointment date is not in the past
        if date and date < timezone.now().date():
            raise forms.ValidationError("You cannot book an appointment in the past.")

        return cleaned_data



class RescheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["rating", "comments"]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} ⭐") for i in range(1, 6)]),
            "comments": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your feedback..."}),
        }


class AmbulanceForm(forms.ModelForm):
    class Meta:
        model = Ambulance
        fields = ["vehicle_number", "driver_name", "driver_contact", "location", "is_available"]


class AmbulanceBookingForm(forms.ModelForm):
    class Meta:
        model = AmbulanceBooking
        fields = ["hospital", "ambulance", "pickup_latitude", "pickup_longitude"]
        widgets = {
            "pickup_latitude": forms.HiddenInput(),
            "pickup_longitude": forms.HiddenInput(),
        }




class AffiliationRequestForm(forms.ModelForm):
    class Meta:
        model = AffiliationRequest
        fields = ["from_hospital", "to_hospital"]


from django import forms
from .models import Referral, Doctor

from django import forms
from .models import Referral, Doctor

from django import forms
from .models import Referral, Doctor

from django import forms
from .models import Referral, Doctor


class ReferralForm(forms.ModelForm):
    to_doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), label="To Doctor")

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop("doctor", None)  # Get current doctor
        super().__init__(*args, **kwargs)

        if doctor:
            # Get doctors from affiliated hospitals
            affiliated_hospitals = doctor.hospital.affiliated_hospitals.all()
            self.fields["to_doctor"].queryset = Doctor.objects.filter(hospital__in=affiliated_hospitals)

    class Meta:
        model = Referral
        fields = ["to_doctor", "reason"]


from django import forms
from .models import Doctor

from django import forms
from .models import Doctor

class DoctorProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    license_number = forms.CharField(max_length=50, required=True, label="License Number")  # ✅ New field

    available_days = forms.MultipleChoiceField(
        choices=Doctor.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Available Days"
    )
    available_start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
        label="Available Start Time"
    )
    available_end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
        label="Available End Time"
    )

    class Meta:
        model = Doctor
        fields = [
            "specialization",
            "phone",
            "appointment_fee",
            "profile_picture",
            "license_number",              # ✅ Include in Meta fields
            "available_days",
            "available_start_time",
            "available_end_time"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email
            self.fields["license_number"].initial = self.instance.license_number  # ✅ Pre-fill license number
            self.fields["available_days"].initial = self.instance.available_days.split(",") if self.instance.available_days else []
            self.fields["available_start_time"].initial = self.instance.available_start_time
            self.fields["available_end_time"].initial = self.instance.available_end_time

    def save(self, commit=True):
        doctor = super().save(commit=False)
        user = doctor.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        doctor.license_number = self.cleaned_data["license_number"]  # ✅ Save license number
        doctor.available_days = ",".join(self.cleaned_data["available_days"])
        doctor.available_start_time = self.cleaned_data["available_start_time"]
        doctor.available_end_time = self.cleaned_data["available_end_time"]

        if commit:
            user.save()
            doctor.save()
        return doctor



from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complaint Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your issue'}),
        }

        from django import forms
from .models import Doctor

class DoctorStatusForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


