from flask import Flask, url_for, redirect, render_template, request
import os, pytesseract
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image

# Path for current location
project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_url_path = '',
            static_folder = 'static',
            template_folder = 'templates')

photos = UploadSet('photos', IMAGES)

app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'images'

# Class for Image to Text
class GetText(object):
    
    def __init__(self, file):
        self.file = pytesseract.image_to_string(Image.open(project_dir + '/images/' + file))


# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if the form is empty
        if 'photo' not in request.files:
            return 'there is no photo in form'
           
        photo = request.files['photo']
        path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        # Save the photo in the upload folder
        photo.save(path)
        
        # Class instance 
        textObject = GetText(photo.filename)
        result = textObject.file
        
        # Send the result text as a session to the /result route
        return redirect(url_for('result', result=result))
    return render_template('index.html')

# Result page
@app.route('/result', methods=['GET', 'POST'])
def result():
    result = request.args.get('result', None)
    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

