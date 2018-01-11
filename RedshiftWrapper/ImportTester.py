import imp
 
class ImportTester(type):
    _HaveBeenCalled = False
    _CanImport = False
 
    @classmethod
    def _CheckImport(cls, clsName):
        # If we already test, we return the cached value
        if cls._HaveBeenCalled:
            return cls._CanImport
       
        # Check if module is already pressent
        try:
            imp.find_module(clsName)
            cls._CanImport = True
            return True
            
        # If module is not already loaded we try to laod it
        except ImportError:
            try:
                __import__(clsName)
                cls._CanImport = True
                return True
           
            except ImportError:
                print __import__(clsName)
                cls._CanImport = False
                return False
 
    def __call__(cls, *args, **kwargs):
        if not cls._HaveBeenCalled:
            cls._CheckImport("redshift")
            cls._HaveBeenCalled = True
           
        if cls._CanImport:
            return super(ImportTester, cls).__call__(*args, **kwargs)
        else:
            return False
