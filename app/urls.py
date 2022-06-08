from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('register', register, name='register'),
    path('token', token_send, name='token_send'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error', error, name='error'),
    path('application', application, name='application'),
    path('job_record', Job_record, name='job_record'),
    path('employee', Employee, name='employee'),
    path('job_confirm/<int:record_id>', Job_confirm, name='job_confirm'),
    path('notify/<int:record_id>', Notify, name='notify'),
    path('edit/<int:emp_id>', edit_employee, name='edit_employee'),
    path('edit_record/<int:rec_id>', edit_record, name='edit_record'),
    path('update/<int:emp_id>', update_employee, name='update_employee'),
    path('update_record/<int:rec_id>', update_record, name='update_record'),
    path('delete/<int:emp_id>', delete_employee, name='delete_employee'),
    path('delete_record/<int:rec_id>', delete_record, name='delete_record'),
    path('service_report/<int:record_id>', View_service_report, name='view_service_report'),
    path('application_form', application_form, name='application_form'),
    path('manager_dashboard', manager_dashboard, name='manager_dashboard'),
    path('operator_dashboard', operator_dashboard, name='operator_dashboard'),
    path('sales_dashboard', sales_dashboard, name='sales_dashboard'),
    path('technician_dashboard', technician_dashboard, name='technician_dashboard'),
    path('activity', Activity_log, name='activity_log'),
    path('contract', contract, name='contract_dashboard'),
    path('account', account, name='account_dashboard'),
    path('quality', quality, name='quality_dashboard'),
]