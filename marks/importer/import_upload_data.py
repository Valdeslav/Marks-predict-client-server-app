from django.core.files.uploadedfile import InMemoryUploadedFile

supported_files = {'.csv': ',', '.tsv': '\t', '.psv': '|', '.ssv': ';'}


def import_data_from_file(data_file: InMemoryUploadedFile):
    save_getting_file(data_file)


def save_getting_file(data_file: InMemoryUploadedFile):
    file_name = data_file.name
    file_extention = file_name[file_name.rfind('.'):]
    if not supported_files[file_extention]:
        raise 
    with open('marks/importer/files/upload.txt', 'wb') as dest:
        for chunk in data_file.chunks():
            dest.write(chunk)