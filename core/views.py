from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusinessCard
from .forms import ImageUploadForm
import pytesseract
from PIL import Image
import re
import os

# Function to extract text from an image
def extract_text(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
    return text

# Function to extract information from text
def extract_info(text):
    company_name_regex = re.compile(r'(?i)(company|business|firm|organization|organisation|llc|pvt|ltd|consultancy|trading|GP|LP|JV|SP|Branch|Rep Office|Public SH Co|Private SH Co|PLBS|PE|Trade Lic|Prof. Lic.|Ind. Lic.|Tour. Lic|Health Lic| Food Lic.|Real Est. Lic.|Fin. Serv. Lic.|Media Lic.|Edu. Lic.)[:=]?\s*([^@\n]+)(?:\n|$)')
    phone_regex = re.compile(r'\b((?:\+\d{1,2}\s*)?(?:\(\d{1,}\)\s*)?\d{1,}[\s\.-]?\d{1,}[\s\.-]?\d{1,})(?:\s*\(?(?:ext|x|ex)?\.?\s*(\d{1,})\)?)?\b')
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    website_regex = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/?)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')

    company_name_match = re.search(company_name_regex, text)
    phone = re.search(phone_regex, text)
    email = re.search(email_regex, text)
    website = re.search(website_regex, text)

    company_name = company_name_match.group(2).strip() if company_name_match else None
    phone = phone.group(0).strip() if phone else None
    email = email.group(0).strip() if email else None
    website = website.group(0).strip() if website else None

    return company_name, phone, email, website

# View for uploading image and performing OCR
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create directory if it doesn't exist
            media_root = os.path.join(os.getcwd(), 'media')
            uploaded_images_dir = os.path.join(media_root, 'uploaded_images')
            os.makedirs(uploaded_images_dir, exist_ok=True)

            # Save the uploaded image
            uploaded_image = request.FILES['image']
            image_path = os.path.join(uploaded_images_dir, uploaded_image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            # Extract text from the image
            extracted_text = extract_text(image_path)

            # Extract information from the text
            company_name, phone, email, website = extract_info(extracted_text)

            # Save the extracted information to the database
            business_card = BusinessCard.objects.create(
                filename=uploaded_image.name,
                company_name=company_name,
                phone=phone,
                email=email,
                website=website
            )

            # Return extracted information as JSON response
            return JsonResponse({
                'company_name': company_name,
                'phone': phone,
                'email': email,
                'website': website
            })
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = ImageUploadForm()
    return render(request, 'capture_image.html', {'form': form})
