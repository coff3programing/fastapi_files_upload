from fastapi import APIRouter, UploadFile, File, Form
from os import getcwd, remove
from shutil import rmtree
from fastapi.responses import FileResponse, JSONResponse
from typing import List

router = APIRouter()

#* Upload Files
@router.post('/upload', tags=['Upload File'], status_code=200)
async def upload_file(file: UploadFile = File(...)):
    with open(getcwd() + '/' + file.filename, 'wb') as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    return 'success'
  

#* Upload Multi Files
@router.post('/multiple/files', tags=['Upload Files'], status_code=200)
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            with open(file.filename, "wb") as my_file:
                content = await file.read()
                my_file.write(content)
                my_file.close()
        return JSONResponse(content={'saved': True}, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={'saved': False}, status_code=302)
  
#* View in Browser
  
@router.get('/file/{name_file}', tags=['View File'], status_code=200)
def get_file(name_file: str):
    return FileResponse(getcwd() + '/' + name_file)

#* download files
@router.get('/download/{name_file}', tags=['Download Files'], status_code=200)
def get_file(name_file : str):
    return FileResponse(getcwd() + '/' + name_file, media_type='application/octet-stream', filename= name_file)

@router.delete('/deleting/{name_file}', tags=['Delete Files'] , status_code=200)
def delete_file(name_file: str):
    try:
        remove(getcwd() + '/' + name_file)
        return JSONResponse(content={'removed': True}, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={'removed': False, 'message': 'File not found'}, status_code=404)

@router.delete('/folder', tags=['Delete Folders'] , status_code=200)
def delete_file(folder_name: str = Form(...)):
    rmtree(getcwd() + folder_name)
    return JSONResponse(content={'removed': True}, status_code=200)
  