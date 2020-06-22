from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads, AUDIO
import speech_recognition as sr

app = Flask(__name__)

wavaudio = UploadSet('files', AUDIO)

app.config['UPLOADED_FILES_DEST'] = 'static/audio'
configure_uploads(app, wavaudio)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'au' in request.files:
        filename = wavaudio.save(request.files['au'])
        r = sr.Recognizer()
        audio = 'static/audio/{}'.format(filename)
        with sr.AudioFile(audio) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            with open("output.txt","a+") as f:
                f.write("\n"+text)
            return(jsonify(title=text))    
        except Exception as e:
            return(e)
        
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
 