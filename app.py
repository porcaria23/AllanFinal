
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav'}

# Cria a pasta de uploads, se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html', database=db)

@app.route('/update', methods=['POST'])
def update():
    key = request.form['id']
    data = request.form['data']
    descricao = request.form['descricao'] # Obtém a descrição do formulário
    file = request.files.get('audio')

    if key in db:
        db[key]['Sala'] = data
        db[key]['Descrição'] = descricao # Atualiza a descrição no db
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            db[key]['Audio'] = filepath                                                      
        else:                                                                                                          
            db[key]['Audio'] = 'No Audio'  # Caso nenhum arquivo seja enviado                                            
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    if id in db:
        db[id]['Sala'] = 'No Data'
        db[id]['Descrição'] = 'No Data' # Zera a descrição
        db[id]['Audio'] = 'No Audio'
        return {'success': True}, 200
    else:
        return {'success': False, 'error': 'ID not found'}, 404

# Inicializa o banco de dados em memória
db = {
    'A1': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'B1': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'C1': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'D1': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'E1': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'A2': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'B2': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'C2': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'D2': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'},
    'E2': {'Sala': 'Sala', 'Audio': 'No Audio', 'Descrição': 'Descrição padrão'}
}


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
@app.route('/curioso.mp3')
def serve_audio():
    return send_from_directory('.', 'curioso.mp3')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
