from fastapi import APIRouter, UploadFile, File, Form
from os import getcwd, remove, makedirs, path as os_path, rename
from shutil import rmtree
from pathlib import Path
from fastapi.responses import FileResponse, JSONResponse
from typing import List

router = APIRouter(prefix='/files', tags=['Files Control'])

# * Upload Files

ALLOWED_EXTENSIONS = {'txt', 'sed'}
UPLOAD_FOLDER = 'static/data'
UPLOAD_MY_FOLDER = Path('static/data')
DELETE_FOLDER = Path('static')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def change_extension_to_txt(original_path):
    # Get the directory and file name from the path
    directory, name = os_path.split(original_path)

    # Change the extension to .txt
    new_name = os_path.splitext(name)[0] + '.txt'

    # Create the new path with the changed extension
    new_path = os_path.join(directory, new_name)

    # Rename the file using the function from the os module
    rename(original_path, new_path)

    return new_path


@router.post('/upload', tags=['Upload File'], status_code=200)
async def upload_file(file: UploadFile = File(...)):
    try:
        if not allowed_file(file.filename):
            return {'error': 'Solo se permiten archivos con extensiones .txt y .sed'}

        # Crea la carpeta si no existe
        makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Concatena la ruta de la carpeta de carga
        upload_path = f"{getcwd()}/{UPLOAD_FOLDER}/{file.filename}"

        with open(upload_path, 'wb') as myfile:
            content = await file.read()
            myfile.write(content)

        # Si la extensión es .sed, cambia la extensión a .txt
        if file.filename.lower().endswith('.sed'):
            upload_path = change_extension_to_txt(upload_path)

        return {'message': 'Archivo subido exitosamente'}
    except Exception as e:
        return {'error': f'Error interno del servidor: {str(e)}'}

# * Upload Multi Files


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def change_extension_to_txt(original_path):
    # Get the directory and file name from the path
    directory, name = os_path.split(original_path)

    # Change the extension to .txt
    new_name = os_path.splitext(name)[0] + '.txt'

    # Create the new path with the changed extension
    new_path = os_path.join(directory, new_name)

    # Rename the file using the function from the os module
    rename(original_path, new_path)

    return new_path


@router.post('/multiple', tags=['Upload Files'], status_code=200)
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    try:
        # Crea la carpeta si no existe
        makedirs(UPLOAD_FOLDER, exist_ok=True)

        for file in files:
            if not allowed_file(file.filename):
                # Si algún archivo no es permitido, retorna un error
                return JSONResponse(content={'saved': False, 'error': 'Solo se permiten archivos con extensiones .txt y .sed'}, status_code=400)

            # Concatena la ruta de la carpeta de carga
            upload_path = f"{getcwd()}/{UPLOAD_FOLDER}/{file.filename}"

            with open(upload_path, 'wb') as myfile:
                content = await file.read()
                myfile.write(content)

            # Si la extensión es .sed, cambia la extensión a .txt
            if file.filename.lower().endswith('.sed'):
                upload_path = change_extension_to_txt(upload_path)

        return JSONResponse(content={'saved': True}, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={'saved': False}, status_code=302)

# * View in Browser


@router.get('/{name_file}', tags=['View File'], status_code=200)
def get_file(name_file: str):
    file_path = UPLOAD_MY_FOLDER / name_file
    if file_path.is_file():
        return FileResponse(file_path, media_type='application/octet-stream', filename=name_file)
    else:
        return JSONResponse(content={'error': 'El archivo no existe'}, status_code=404)

# * download files


@router.get('/download/{name_file}', tags=['Download Files'], status_code=200)
def download_file(name_file: str):
    file_path = UPLOAD_MY_FOLDER / name_file
    if file_path.is_file():
        return FileResponse(file_path, media_type='application/octet-stream', filename=name_file)
    else:
        return JSONResponse(content={'error': 'El archivo no existe'}, status_code=404)

# Delete a file


@router.delete('/delete/{name_file}', tags=['Delete Files'], status_code=200)
def delete_file(name_file: str):
    file_path = UPLOAD_MY_FOLDER / name_file
    try:
        file_path.unlink()
        return JSONResponse(content={'removed': True, 'message': 'El archivo se ha eliminado exitosamente'}, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={'removed': False, 'message': 'File not found'}, status_code=404)

# Delete folder


@router.delete('/folder', tags=['Delete Folders'], status_code=200)
def delete_folder(folder_name: str = Form(...)):
    target_folder_path = DELETE_FOLDER / folder_name

    try:
        # Verificar si el directorio existe antes de intentar eliminarlo
        if target_folder_path.is_dir():
            rmtree(target_folder_path)
            return JSONResponse(content={'removed': True, 'message': 'Awebo si se pudo eliminar'}, status_code=200)
        else:
            return JSONResponse(content={'removed': False, 'message': 'La carpeta no existe'}, status_code=404)
    except Exception as e:
        return JSONResponse(content={'removed': False, 'message': f'Error al eliminar la carpeta: {str(e)}'}, status_code=500)
