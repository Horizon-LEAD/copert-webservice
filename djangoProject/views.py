from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from rest_framework.response import Response
import subprocess
import os
from os.path import exists
import time
from zipfile import ZipFile
import time

#inputFilepath = 'C:\\Users\\Administrator\\Desktop\\djangoProject\\'
#outputFilepath = 'C:\\Users\\Administrator\\Desktop\\djangoProject\\output.xlsx'
#outputFilepathEB = 'C:\\Users\\Administrator\\Desktop\\djangoProject\\outputEB.xlsx'


#inputFilepath = 'C:\\Users\\valia\\PycharmProjects\\djangoProject\\'  #left for local Windows debug
#outputFilepath = 'C:\\Users\\valia\\PycharmProjects\\djangoProject\\output.xlsx'
#outputFilepath1 = 'C:\\Users\\valia\\PycharmProjects\\djangoProject\\outputEB.xlsx'


@api_view(['GET', 'POST'])
def index(request):
    res = -1
    if request.method == 'POST':
        print('request received')
        try:
            filepath = getInputFile(request)
            switch = request.POST.get('switch')
            EFoutput = request.POST.get('EF')      
            EBoutput = request.POST.get('EB')
            outputExtension = request.POST.get('outputFile')
            print('requet get fields')
        except:
            return Response({"Fail": "Input File/Parameter Error"}, status=status.HTTP_400_BAD_REQUEST)
        if EFoutput == 'false' and EBoutput == 'false': 
            return Response({"Fail": "Output file option does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        print('before file extention')
        outputFile, outputFileEB = decideFileExtention(outputExtension)
        print('before delteting')
        deleteOldOutputFiles(outputFile, outputFileEB)
        print('before run copert')
        res = runCopert(filepath, switch, EFoutput, EBoutput, outputFile, outputFileEB)
        print('before zip files')
        zipOutputFiles(outputFile, outputFileEB)
        if res == -1 :
            response = Response({"Fail": "COPERT Run Error - Please check input file"}, status=status.HTTP_400_BAD_REQUEST)
            print('before killing copert')
            os.system("TASKKILL /F /IM COPERT.exe")
        else:
            response = HttpResponse(open('output.zip', 'rb'), content_type='application/zip')
        print('before delete 2')
        deleteOldOutputFiles(outputFile, outputFileEB)
    else:
        response = Response({"Fail": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    
    return response


def decideFileExtention(outputExtension):
    if outputExtension is None:  # valia
        outputExtension = 'xlsx'
    if outputExtension == 'xlsx':
        outputFile = 'output.xlsx'
        outputFileEB = 'outputEB.xlsx'
    else:
        outputFile = 'output.json'
        outputFileEB = 'outputEB.json'
    return outputFile, outputFileEB


def zipOutputFiles(outputFile, outputFileEB):
    outputZip = ZipFile('output.zip', 'w')
    if exists(outputFile):
        outputZip.write(outputFile)
    if exists(outputFileEB):
        outputZip.write(outputFileEB)
    outputZip.close()


def deleteOldOutputFiles(outputFile, outputFileEB):
    if exists(outputFile):
        os.remove(outputFile)
    if exists(outputFileEB):
        os.remove(outputFileEB)


def getInputFile(request):
    for filename, file in request.FILES.items():
        file = request.FILES[filename]
        path = default_storage.save(file.name, file)		
    return path 


def runCopert(filepath, switch, EFoutput, EBoutput, outputFile, outputFileEB):
    filepath, command = prepareCommand(filepath, switch, EFoutput, EBoutput, outputFile, outputFileEB)
    t0 = time.time()
    t1 = time.time()
    cmd = subprocess.Popen(["start", "cmd", "/c", command], stdout=subprocess.PIPE, shell=True)
    while EBoutput == 'true' and not exists(outputFileEB) and (t1 - t0) < 200:
        time.sleep(2)
        t1 = time.time()
        print('searching for EB')
    while EFoutput == 'true' and not exists(outputFile)and (t1 - t0) < 200:
        time.sleep(2)
        t1 = time.time()
        print('searching for EF')
    os.remove(filepath)
    if (t1 - t0) > 200 :
        print('before killing cmd')
        cmd.kill()
        os.system("TASKKILL /F /IM COPERT.exe")
        print('after killing cmd')
        return -1
    cmd.kill()
    return 1


def prepareCommand(filepath, switch, EFoutput, EBoutput, outputFile, outputFileEB):  #valia this
    command = "copert -i " + filepath
    if EFoutput is not None and EFoutput == 'true':
        command = command + ' -oEF ' + outputFile + ' '
    if EBoutput is not None and EBoutput == 'true':
        command = command + ' -oEB ' + outputFileEB + ' '
    if switch is not None and switch != 'off':
        command = command + switch
    print (command)
    return filepath, command
