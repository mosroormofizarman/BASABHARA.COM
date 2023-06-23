import firebase_admin, requests
from firebase_admin import credentials, db, auth, storage
from django.shortcuts import render
import tempfile, os

# Initialize Firebase Admin with service account credentials
cred = credentials.Certificate('main/firebase_config.json')

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

def post(request):
    message = ""
    if request.method == 'POST':
        name = request.POST.get('Adsname')
        name = name.replace('.', ' ').replace('$', ' ').replace('#', ' ').replace('[', ' ').replace(']', ' ').replace('/', ' ').replace('-', ' ')

        # Retrieve the uploaded file
        picture = request.FILES['picture']

        phone_number = request.POST.get('Number')
        location = request.POST.get('Location')
        cost = request.POST.get('Cost')

        try:
            # Check if Ad with the same name already exists
            ref = db.reference('Details')
            details = ref.get()
            ad_names = []
            for ad_id, ad_data in details.items():
                ad_name = list(ad_data.keys())[0]
                ad_names.append(ad_name)

                if name == ad_name:
                    message = "Ad with the same name already exists!"
                    break
            else:
                # If ad name is not found, push the data into the database
                ref = db.reference('Details')
                ad_ref = ref.push().child(name)
                ad_ref.set({
                    'location': location,
                    'phone_number': phone_number,
                    'cost': cost
                })

                # Set the file name to be the same as the ad name
                file_name = f"{name}"

                # Get a reference to the Firebase Storage bucket
                bucket = storage.bucket()

                # Create a new blob in the bucket and upload the file data
                blob = bucket.blob(file_name)
                blob.upload_from_file(picture, content_type='image/jpeg')

                message = "Posted Ad successfully!"

        except:
            message = "Posting Ad failed!"

    return render(request, 'post.html', {'message': message})

