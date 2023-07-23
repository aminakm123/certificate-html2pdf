import hashlib
import json
import random
import string

from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template

from xhtml2pdf import pisa

from pdfcertificate.forms import CertificateForm, VerifyCertificateForm
from pdfcertificate.models import Certificate


def generate_verification_code(name,subtitle,date,sign):
    user_data = f"{name}{subtitle}{date}{sign}"
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits,k=10))
    verification_code = hashlib.sha256(user_data.encode('utf-8') + random_string.encode('utf-8')).hexdigest()
    return verification_code


def create_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            print("form is valid")
            name = form.cleaned_data['name']
            subtitle = form.cleaned_data['subtitle']
            date = form.cleaned_data['date']
            sign = form.cleaned_data['sign']
            verification_code = generate_verification_code(name,subtitle,date,sign)
            # Get the custom content from the request, if available
            custom_content = request.POST.get('custom_content', '')

            print("name",name)
            print("verification code",verification_code)

            Certificate.objects.create(
                name = name,
                subtitle = subtitle,
                date = date,
                sign = sign,
                custom_content = custom_content,
                verification_code = verification_code
            )
            # return redirect('pdfcertificate:pdf_certificate', pk=verification_code)
        # return HttpResponseRedirect(reverse('pdf_certificate'))
            print("data saved to model")
            response_data = {
                "success": True,
                "message": "Certificate created successfully!",
                "verification_code": verification_code,
                "status" : "true",
                "title" : "Successfully Created"
            }

        else:
            print("not valid")
            form = CertificateForm()
            # return render(request,'create_certificate.html',{"form":form})   

            def generate_form_errors(args,formset=False):
                message = ''
                if not formset:
                    print("not formset")
                    for field in args:
                        print("field",field)
                        if field.errors:
                            message += str(field.errors)  + "|"
                            print("message",message)
                        else:
                            print("non field errors",args.non_field_errors)
                            print("above is a non field error")
                            for err in args.non_field_errors():
                                print("err",err)
                                message += str(err) + "|"
                                print("message",message)
                            
                elif formset:
                    print("formset")
                    for form in args:
                        for field in form:
                            if field.errors:
                                message += str(field.errors) + "|"
                                print("message",message)
                        for err in form.non_field_errors():
                            message += str(err) + "|"
                            print("message",message)
                return message[:-1]
            print("form not valid")
            response_data = {  
                "success" : False,              
                "stable" : "True",
                "status" : "false",
                "title" : "Form validation error",
                "message" :generate_form_errors(form,formset=False)
            }
        return HttpResponse(json.dumps(response_data), content_type = 'application/javascript')
    
    else:
        form = CertificateForm()
        return render(request,'create_certificate.html',{"form":form})   


def pdf_certificate(request,pk):
    certificate = get_object_or_404(Certificate.objects.filter(verification_code=pk))
    template_path = 'certificate.html'
    context = {'certificate':certificate}
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'filename = "certificate.pdf"'   
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse("we had some errors <pre>" + html + "</pre>")
    return response

def verify_certificate(request):
    if request.method == 'POST':
        form = VerifyCertificateForm(request.POST)
        verification_code = request.POST.get('verification_code')
        if Certificate.objects.filter(verification_code=verification_code).exists():
            response_data = {
                "success": True,
                "title": "Verified",
                "message" : "Certificate is valid"
            }
        else:
            response_data = {
                "success" : False,
                "title" : "Not Verified",
                "message" : "Certificate is not valid"
            }
        return HttpResponse(json.dumps(response_data), content_type = 'application/javascript')
    else:
        form = VerifyCertificateForm()
        return render(request,'verify_certificate.html',{"form":form})