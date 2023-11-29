from django.shortcuts import render
from aerouser.models import userdata
from .models import Ventilator,Patient

"""def device_reg(request):
    if request.method == 'POST':
        field1_data = request.POST.get('email')
        request.session['email'] = field1_data
        if not userdata.objects.filter(email__iexact=field1_data).exists():
            error_message = "Please sign up."
            return render(request, "device_reg.html", {'error_message': error_message})
        
        return render(request,"device_reg2.html")
    else:
        return render(request, "device_reg.html")"""

def device_reg2(request):
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number')
        location = request.POST.get('location')
        model = request.POST.get('model')
        
        new_entry = Ventilator(
            serial_number=serial_number,
            location=location,
            model=model  
        )
       
        new_entry.save()
        return render(request, "landing.html")
    else:
        return render(request, "device_reg2.html") 
    
def patient_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        patient_id = request.POST.get('patient_id')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
    
        new_entry = Patient(
            name=name,
            patient_id=patient_id,
            age=age,
            gender=gender,
            status=status
        )
        new_entry.save()
        return render(request, "landing.html")
    else:
        return render(request, "patient.html")  
    
def patient_list(request):
    if request.method == 'GET':
        patients = Patient.objects.all()  
        return render(request, "patient_list.html", {'patients': patients})
    else:
        return render(request, "patient.html") 
    
def device_list(request):
    if request.method == 'GET':
        devices = Ventilator.objects.all()  
        return render(request, "device_list.html", {'devices': devices})
    else:
        return render(request, "device_reg2.html") 

