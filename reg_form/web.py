from flask import Flask, request, render_template
from cv2 import imwrite

app=Flask(__name__)

@app.route('/'):
def Index():
    return render_template('index.html')

@app.route("/upload",methods=["POST"])
def upload():
    file=request.files['Inputfile']
    file.imwrite("example.jpg")

if if __name__ == "__main__":
    app.run(debug=True)