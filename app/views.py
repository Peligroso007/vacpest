from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from decouple import config
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.services.get_profile import get_profile_by_id
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def Login(request):
    username = request.user.username
    user_obj = User.objects.filter(username=username).first()
    profile_obj = Profile.objects.filter(user=user_obj).first()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'User not found.')
            return render(request, 'login.html')

        profile_obj = Profile.objects.filter(user = user_obj).first()
        if not profile_obj.is_verified:
            messages.error(request, 'Account is not verified check your email.')
            return render(request, 'login.html')

        user = authenticate(request, username = username, password = password)
        if user is None:
            messages.error(request, 'Credentials are wrong please check your username and password.')
            return render(request, 'login.html')

        if profile_obj.role == 1:
            login(request, user)
            activity_log.objects.create(notification=user.username + " just logged in.")
            return redirect('manager_dashboard')

        if profile_obj.role == 2:
            login(request, user)
            activity_log.objects.create(notification=user.username + " just logged in.")
            return redirect('operator_dashboard')

        if profile_obj.role == 3:
            login(request, user)
            activity_log.objects.create(notification=user.username + " just logged in.")
            return redirect('sales_dashboard')

        if profile_obj.role == 4:
            login(request, user)
            activity_log.objects.create(notification=user.username + " just logged in.")
            return redirect('technician_dashboard')

        if profile_obj.role == 5:
            login(request, user)
            activity_log.objects.create(notification=user.username + " just logged in.")
            return redirect('contract_dashboard')

        if profile_obj.role == 6:
            login(request, user)
            activity_log.objects.create(notification=user.username + " just logged in.")
            return redirect('account_dashboard')

        if profile_obj.role == 7:
            login(request, user)
            activity_log.objects.create(notification=user.username + " just logged in.")
            return redirect('quality_dashboard')

    if request.user.is_authenticated:
        if profile_obj.role == 1:
            return redirect('manager_dashboard')

        if profile_obj.role == 2:
            return redirect('operator_dashboard')

        if profile_obj.role == 3:
            return redirect('sales_dashboard')

        if profile_obj.role == 4:
            return redirect('technician_dashboard')

        if profile_obj.role == 5:
            return redirect('contract_dashboard')

        if profile_obj.role == 6:
            return redirect('account_dashboard')

        if profile_obj.role == 7:
            return redirect('quality_dashboard')


    return render(request, 'login.html')


@login_required()
def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        role = request.POST.get('role')
        try:
            if User.objects.filter(username = username).first():
                messages.error(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.error(request, 'Email is already in use by a user.')
                return redirect('/register')
            user_obj = User.objects.create(username = username, email = email, first_name = first_name, last_name = last_name)
            user_obj.set_password(password)
            user_obj.save()
            activity_log.objects.create(notification=user_obj.username + " user is just created.")

            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj, phone = phone, gender = gender, role = role, address = address, auth_token= auth_token)
            profile_obj.save()
            send_verification_mail(email,auth_token,username)

            return  redirect('token_send')
        except Exception as e:
            print(e)
    return render(request, 'register.html')


def token_send(request):
    activity_log.objects.create(notification="Token has just been sent to the user who has just been created")
    return render(request, 'token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account has been already verified.')
                activity_log.objects.create(notification=profile_obj.user.username + " just tried to verify the account")
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            activity_log.objects.create(notification=profile_obj.user.username + " just verified the account")
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)



def error(request):
    return render(request, 'error.html')

def contract(request):
    return render(request, 'contract_dashboard.html')

def account(request):
    return render(request, 'account_dashboard.html')

def quality(request):
    return render(request, 'quality_dashboard.html')


def send_verification_mail(email, token, username):
    subject = 'Your account need to be verified'
    message = f'Hi {username} please click on the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = config('EMAIL_HOST_USER')
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    activity_log.objects.create(notification="A verification email was sent to " + username)


def send_confirmation_mail(email, username, technician):
    subject = 'Update From Vacpest'
    message = f'Hi {username} our technician {technician} is on the way.'
    email_from = config('EMAIL_HOST_USER')
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    activity_log.objects.create(notification="A job of "+username+" has just been confirmed by "+ technician)


def manager_dashboard(request):
    return render(request, 'manager_dashboard.html')

def operator_dashboard(request):
    return render(request, 'operator_dashboard.html')

def sales_dashboard(request):
    return render(request, 'sales_dashboard.html')

def technician_dashboard(request):
    return render(request, 'technician_dashboard.html')

def application(request):
    return render(request, 'application.html')

def Logout(request):
    activity_log.objects.create(notification=request.user.username + " just logged out.")
    logout(request)
    return redirect('login')


def application_form(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        post_code = request.POST.get('post_code')
        job_date = request.POST.get('job_date')
        job_time = request.POST.get('job_time')
        job_detail = request.POST.get('job_detail')

        try:
            record_obj = job_record.objects.create(first_name=first_name,last_name=last_name,email=email,address=address,city=city,state=state,post_code=post_code,job_date=job_date,job_time=job_time,job_detail=job_detail)
            record_obj.save()
            activity_log.objects.create(notification="A new job jas been created.")
            messages.success(request, "Record has been successfully added.")
            return redirect('application_form')
        except Exception as e:
            print(e)
    return render(request, 'application.html')


@login_required()
def Job_record(request):
    record = job_record.objects.all()
    return render(request, 'job_record.html', {'record': record})
@login_required()
def Job_confirm(request, record_id):
    technician = request.user.username
    if request.method == 'POST':
        try:
            Record_obj = job_record.objects.filter(id=record_id).first()
            if Record_obj is None:
                messages.error(request, 'Record not found')
                return redirect('job_record')
            service_frequency = request.POST.get('service_frequency')
            service_finished_time = request.POST.get('service_finished_time')
            further_service = request.POST.get('further_service')
            area_treated = request.POST.get('area_treated')
            unchecked_area = request.POST.get('unchecked_area')
            type_of_pest_control = request.POST.get('type_of_pest_control')
            other_type = request.POST.get('other_type')
            service_report = request.POST.get('service_report')
            Record_obj.technician = technician
            Record_obj.is_done = True
            Record_obj.save()

            service_obj = Service_report.objects.create(job_id=Record_obj, service_frequency=service_frequency,service_finished_time=service_finished_time,further_service=further_service,area_treated=area_treated,unchecked_area=unchecked_area,type_of_pest_control=type_of_pest_control,other_type=other_type, service_report=service_report)
            service_obj.save()
            activity_log.objects.create(notification="A service report has been updated for "+Record_obj.first_name + " by " + technician)

            return redirect('job_record')
        except Exception as e:
            print(e)



    return render(request, 'job_confirm.html', {'record_id': record_id})

@login_required()
def Employee(request):
    employees = User.objects.all()
    return render(request, 'employee.html', {'employees': employees})


def View_service_report(request, record_id):
    Record_obj = job_record.objects.filter(id=record_id).first()
    return render(request, 'service_report.html', {'record': Record_obj})

def Notify(request,record_id):
    technician = request.user.username
    job_record_obj = get_object_or_404(job_record, id=record_id)
    email = job_record_obj.email
    username = job_record_obj.first_name
    send_confirmation_mail(email, username, technician)
    return redirect('job_record')

def edit_employee(request, emp_id):
    employee = User.objects.filter(pk=emp_id).first()
    return render(request, 'user_edit.html', {"employee": employee})

def delete_employee(request, emp_id):
    try:
        employee = User.objects.filter(pk=emp_id).first()
        activity_log.objects.create(notification=employee.username +" has been deleted from system.")
        User.objects.get(pk=emp_id).delete()
        messages.success(request, "Employee is Successfully deleted.")
        return redirect('employee')
    except Exception as e:
        print(e)

    messages.error(request, "Something went wrong.")
    return redirect('employee')

def update_employee(request, emp_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        role = request.POST.get('role')

        try:
            user = User.objects.filter(pk=emp_id).first()

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.profile.phone = phone
            user.email = email
            user.profile.gender = gender
            user.profile.address = address
            user.profile.role = role

            user.save()
            user.profile.save()
            activity_log.objects.create(notification=user.username + " user has just been updated.")
            messages.success(request, 'Employee record updated.')
            return redirect('employee')
        except Exception as e:
            print(e)

    return redirect('employee')

def edit_record(request, rec_id):
    record = job_record.objects.filter(pk=rec_id).first()
    return render(request, 'record_edit.html', {"record": record})

def delete_record(request, rec_id):
    try:
        record = job_record.objects.filter(pk=rec_id).first()
        job_record.objects.get(pk=rec_id).delete()
        activity_log.objects.create(notification="Record of  "+record.first_name+" been deleted from the system")
        messages.success(request, "Record is Successfully deleted.")
        return redirect('job_record')
    except Exception as e:
        print(e)

    messages.error(request, "Something went wrong.")
    return redirect('job_record')

def update_record(request, rec_id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        post_code = request.POST.get('post_code')
        job_date = request.POST.get('job_date')
        job_time = request.POST.get('job_time')
        job_detail = request.POST.get('job_detail')

        try:
            record = job_record.objects.filter(pk=rec_id).first()

            record.first_name = first_name
            record.last_name = last_name
            record.email = email
            record.address = address
            record.city = city
            record.state = state
            record.post_code = post_code
            record.job_time = job_time
            record.job_date = job_date
            record.job_detail = job_detail

            record.save()
            activity_log.objects.create(notification="Record of "+record.first_name+" has been updated recently.")
            messages.success(request, "Record updated successfully.")
            return redirect('job_record')
        except Exception as e:
            print(e)
    return redirect('job_record')


def Activity_log(request):
    activity = activity_log.objects.all()
    return render(request, 'activity_log.html', {"activity": activity})

