from django.core.files.uploadedfile import InMemoryUploadedFile


def file_to_str(data_file: InMemoryUploadedFile):
    with open('marks/importer/files/upload.txt', 'wb') as dest:
        for chunk in data_file.chunks():
            dest.write(chunk)

