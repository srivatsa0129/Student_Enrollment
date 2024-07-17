from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import StudentForm
from .models import Student
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = StudentForm()
    return render(request, 'enrollment/register.html', {'form': form})

def export_students_csv(request):
    students = Student.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number'])

    for student in students:
        writer.writerow([student.first_name, student.last_name, student.email, student.phone_number])

    return response

def export_students_pdf(request):
    students = Student.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, 'Student List')
    p.drawString(50, 750, 'First Name')
    p.drawString(150, 750, 'Last Name')
    p.drawString(250, 750, 'Email')
    p.drawString(350, 750, 'Phone Number')

    y = 730
    for student in students:
        p.drawString(50, y, student.first_name)
        p.drawString(150, y, student.last_name)
        p.drawString(250, y, student.email)
        p.drawString(350, y, student.phone_number)
        y -= 20

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
