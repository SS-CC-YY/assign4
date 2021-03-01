import json


def fileStruck(filename, size):
    fileInfo = {"name": filename, "size": size}

    fileBytes = json.dumps(fileInfo).encode('utf-8')
    return (len(fileBytes), fileBytes)


def fileInfo(bytesContext):
    '''

    :param bytesContext:
    :return: {'name':'xxx','size':xxx}
    '''
    strContext = str(bytesContext, 'utf-8')
    return json.loads(strContext)


if __name__ == '__main__':
    with open('text.txt','w') as fb:
        fb.write('hello')
