import datetime
import os
import zipfile
from decimal import Decimal
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils import simplejson as json
from django.http import HttpResponse
from django.db.models import Model

from django.utils import simplejson
from django.utils.functional import Promise
from django.utils.translation import force_unicode
from django.utils.encoding import smart_unicode
from django.core.serializers.json import DjangoJSONEncoder


def makeJsonFriendly(data):
    '''Will traverse a dict or list compound data struct and
       make any datetime.datetime fields json friendly
    '''
    #print 'makeJsonFriendly called with data: ', str(data)
    #print 'which was a ', type(data)
    try:
        if isinstance(data, list):
            #print 'handling list'
            for e in data:
                e = makeJsonFriendly(e)
        elif isinstance(data, dict):
            #print 'handling dict'
            for key in data.keys():
                data[key] = makeJsonFriendly(data[key])
            
        elif isinstance(data, datetime.datetime):
            #print 'handling datetime'
            #print 'converting datetime: ', str(data)
            return data.strftime('%Y/%m/%d %H:%M')
        else:
            #print 'handling default case. Type was ', type(data)
            #print 'returning unmodified'
            return data #unmodified
    except Exception, e:
        print 'makeJsonFriendly encountered an error: ', str(e)
    #print 'end makeJsonFriendly'    
    return data

# ------------------------------------------------------------------------------
class ModelJSONEncoder(DjangoJSONEncoder):
    """
    (simplejson) DjangoJSONEncoder subclass that knows how to encode fields.y/

    (adated from django.serializers, which, strangely, didn't
     factor out this part of the algorithm)
    """
    def handle_field(self, obj, field):
        return smart_unicode(getattr(obj, field.name), strings_only=True)
    
    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            if field.rel.field_name == related._meta.pk.name:
                # Related to remote object via primary key
                related = related._get_pk_val()
            else:
                # Related to remote object via other field
                related = getattr(related, field.rel.field_name)
        return smart_unicode(related, strings_only=True)
    
    def handle_m2m_field(self, obj, field):
        if field.creates_table:
            return [
                smart_unicode(related._get_pk_val(), strings_only=True)
                for related
                in getattr(obj, field.name).iterator()
                ]
    
    def handle_model(self, obj):
        dic = {}
        for field in obj._meta.local_fields:
            if field.serialize:
                if field.rel is None:
                    dic[field.name] = self.handle_field(obj, field)
                else:
                    dic[field.name] = self.handle_fk_field(obj, field)
        for field in obj._meta.many_to_many:
            if field.serialize:
                dic[field.name] = self.handle_m2m_field(obj, field)
        return dic
    
    def default(self, obj):
        if isinstance(obj, Model):
            return self.handle_model(obj)
        else:
            return super(ModelJSONEncoder, self).default(obj)

# ------------------------------------------------------------------------------
class LazyEncoder(ModelJSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        else:
            return super(LazyEncoder, self).default(o)


def json_encode(data):
    m = ModelJSONEncoder()
    try:
        d = m.encode(data)
        return d
    except Exception, e:
        print 'json_encode: couldn\'t encode', data, ':', str(e)
        return None

def json_decode(data):
    try:
        m = simplejson.JSONDecoder()
        d = m.decode(data)
        return d
    except Exception, e:
        print 'json_decode: couldn\'t decode ', data, ':', str(e)
        return data



def uniqueList(l):
    '''returns unique elements of l.
       sometimes you can use a set to do this, but 
       not if your list contains unhashable types, such as dict.
    '''
 
    seen = []
    result = []
    for i in l:
        if i not in seen:
            result.append(i)
        seen.append(i)

    return result

def translate_dict(data, tuplelist, includeRest = False, createEmpty=False):
    """takes data (should be a dict) and tuple list (list of tuples)
       for each tuple in the list, if the key (element 1) exists in the dict
       then its value is associated with a new key (element 2) in a new
       dict, which is returned.
       if 'includeRest' is True, any keys not mentioned are transplanted to 
       the new dict 'as is'
       if 'createNew' is True, if a key in the tuple doesn't exist, then it 
       is created in the new dict anyway
    """
    returnval = {}
    oldkeylist = []
    for oldkey, newkey in tuplelist:
        oldkeylist.append(oldkey)
        val = data.get(oldkey, None)
        if val != None or createEmpty:
            returnval[newkey] = val
        #otherwise dont bother adding this key, it wasnt in the original data
    if includeRest is True:
        for key in data.keys():
            if key not in oldkeylist:
                returnval[key] = data[key]

    return returnval         


def param_remap(d):
    for key in d:
        if key == 'quoterequestid':
            v = d[key]
            del d[key]
            d['qid'] = v
    return d

def jsonErrorResponse(msg='An error occured'):
    retdata = json.dumps({
        'success': False,
        'msg': msg
    })
    return HttpResponse(retdata)

def jsonResponse(data={}, items=None, mainContentFunction=None, params=None):
    #Sometimes we are passed 'data', and sometimes 'items'. We need to make
    #a decision based on which one we are going to use for the 'totalRows'.
    if items:
        totalrows = len(items)
    else:    
        totalrows = len(data)
    version = 1
    response = {'value': {'items':makeJsonFriendly(items), 'version':1, 'total_count':totalrows}}
    
    retval = {'success': True, 
              'data':makeJsonFriendly(data), 
              'totalRows':totalrows,
              'response': response 
              }
    if params:
        retval['params'] = params
    if mainContentFunction:
        retval['mainContentFunction'] = mainContentFunction

    retdata = json.dumps(retval)
    return HttpResponse(retdata)

class ZipPacker(object):

    def pack(self, files, drop_prefix, filename):
        import zipfile
        zipf = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        for f in files:
            if os.path.isfile(f):
                zipf.write(f, f[len(drop_prefix)+1:])
            elif os.path.isdir(f):
                for (archiveDirPath, dirNames, fileNames) in os.walk(f):
                    for fileName in fileNames:
                        filePath = os.path.join(archiveDirPath, fileName)
                        zipf.write(filePath, filePath[len(drop_prefix)+1:])

        zipf.close()
        return filename
        
class TarPacker(object):
    def __init__(self, compression=None):
        assert compression is None or compression in ('gz','bz2'), "Invalid compression type"
        self.compression = compression

    def pack(self, files, drop_prefix, filename):
        import tarfile
        mode = 'w'
        if self.compression is not None:
            mode = "%s:%s" % (mode, self.compression)
        tar = tarfile.open(filename, mode)
        for f in files:
            print f
            print f[len(drop_prefix)+1:]
            tar.add(f, f[len(drop_prefix):])
        tar.close()
        return filename
        
def guess_package_type(filename):
    def endswithany(s, sa):
        for end in sa:
            if s.endswith(end):
                return True
        return False
    packer = None
    if filename.endswith('.tar'):
        packer = TarPacker()
    elif endswithany(filename, ('.tgz', '.tar.gz')):
        packer = TarPacker(compression='gz')
    elif endswithany(filename, ('.tbz2', '.tar.bz2')):
        packer = TarPacker(compression='bz2')
    elif filename.endswith('zip'):
        packer = ZipPacker()

    return packer 

def pack_files(files, drop_prefix, package_name):
    import tempfile
    packer = guess_package_type(package_name)
    assert packer is not None, 'Invalid package type for ' + package_name
    dummy, filename = tempfile.mkstemp()
    print "FILENAME: " + filename
    package_path = packer.pack(files, drop_prefix, filename)

    return package_path

def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):

    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. "
            "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    #Little nested function to prepare the proper archive path
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)
    
    outFile = zipfile.ZipFile(zipFilePath, "w", compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        #Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            #some web sites suggest doing
            #zipInfo.external_attr = 16
            #or
            #zipInfo.external_attr = 48
            #Here to allow for inserting an empty directory.  Still TBD/TODO.
            outFile.writestr(zipInfo, "")
            
    outFile.close()
