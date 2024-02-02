# FastAPI File Upload API 🚀

## Description

Welcome to the FastAPI File Upload API, where you can seamlessly manage the upload, download, and deletion of files. Explore the powerful features below to make the most out of this API!

## Quick Start

### Installation

Ensure FastAPI is installed in your environment. If not, install it using:

```bash
pip install fastapi
```

### Install additional dependencies from the requirements.txt file:

pip install -r requirements.txt

### Run the Server

Start the server with uvicorn using:
Run the Server
`uvicorn main:app --reload`

## API Features

## Upload a Single File 📤

Method: POST
Route: /upload
Description: Upload a single file effortlessly. Watch your files come to life and enhance your workflow!

## Upload Multiple Files 📤📤

Method: POST
Route: /multiple/files
Description: Streamline your workflow by uploading multiple files simultaneously. Effortless efficiency at your fingertips!

## View File in Browser 👀

Method: GET
Route: /file/{name_file}
Description: Visualize file content directly in your browser. Explore and appreciate your uploaded files seamlessly!

## Download File 📥

Method: GET
Route: /download/{name_file}
Description: Download files directly to your device with ease. Access your files wherever you need them!

## Delete File 🗑️

Method: DELETE
Route: /deleting/{name_file}
Description: Effortlessly declutter your server by deleting unwanted files. Keep your space organized and efficient!

## Delete Folder 🗑️📁

Method: DELETE
Route: /folder
Description: Say goodbye to entire folders and their contents. Clean up your space in one swift action!

## Documentation and API Exploration

- Swagger Documentation:
  Access the Swagger documentation at /docs for interactive API exploration.

* ReDoc Documentation:
  Explore the ReDoc documentation at /redoc for a clean and interactive API reference.
