IF UNAME_SYSNAME == "Windows":
    cdef extern from *:
        """
        #include <windows.h>
        #include <io.h>
        #include <stdlib.h>
        #include <stdio.h>
        #include <fcntl.h>

        int open_temp_file() {
            TCHAR lpTempPathBuffer[MAX_PATH+1];//path+NULL

            //  Gets the temp path env string (no guarantee it's a valid path).
            DWORD dwRetVal = GetTempPath(MAX_PATH,          // length of the buffer
                                         lpTempPathBuffer); // buffer for path 
            if(dwRetVal > MAX_PATH || (dwRetVal == 0))
            {
                return -1;
            }

            //  Generates a temporary file name. 
            TCHAR szTempFileName[MAX_PATH + 1];//path+NULL
            DWORD uRetVal = GetTempFileName(lpTempPathBuffer, // directory for tmp files
                TEXT("tmp"),     // temp file name prefix 
                0,                // create unique name 
                szTempFileName);  // buffer for name 
            if (uRetVal == 0)
            {
                return -1;
            }

            HANDLE tFile = CreateFile((LPTSTR)szTempFileName, // file name 
                    GENERIC_READ | GENERIC_WRITE,      // first we write than we read 
                    0,                    // do not share 
                    NULL,                 // default security 
                    CREATE_ALWAYS,        // overwrite existing
                    FILE_ATTRIBUTE_TEMPORARY | FILE_FLAG_DELETE_ON_CLOSE, // "temporary" temporary file, see https://docs.microsoft.com/en-us/archive/blogs/larryosterman/its-only-temporary
                    NULL);                // no template 

            if (tFile == INVALID_HANDLE_VALUE) {
                return -1;
            }

            return _open_osfhandle((intptr_t)tFile, _O_APPEND | _O_TEXT);
        }

        int replace_stdout(int temp_fileno)
        {
            fflush(stdout);
            int old;
            int cstdout = _fileno(stdout);

            old = _dup(cstdout);   // "old" now refers to "stdout"
            if (old == -1)
            {
                return -1;
            }
            if (-1 == _dup2(temp_fileno, cstdout))
            {
                return -1;
            }
            return old;
        }

        int restore_stdout(int old_stdout){
            fflush(stdout);

            // Restore original stdout
            int cstdout = _fileno(stdout);
            return _dup2(old_stdout, cstdout);
        }
        
        
        void rewind_fd(int fd) {
            _lseek(fd, 0L, SEEK_SET);
        }
        """
        int open_temp_file()
        int replace_stdout(int temp_fileno)
        int restore_stdout(int old_stdout)
        void rewind_fd(int fd)
ELSE:
    cdef extern from *:
        """
        #include <stdio.h>


        int open_temp_file(void) {
            FILE *stream = tmpfile();
            int newfd = dup(fileno(stream));
            fclose(stream);
            return newfd;
        }

        int replace_stdout(int temp_fileno) {
            fflush(stdout);
            int old;
            int cstdout = fileno(stdout);

            old = dup(cstdout);   // "old" now refers to "stdout"
            if (old == -1)
            {
                return -1;
            }
            if (-1 == dup2(temp_fileno, cstdout))
            {
                return -1;
            }
            return old;
        }

        int restore_stdout(int old_stdout) {
            fflush(stdout);

            // Restore original stdout
            int cstdout = fileno(stdout);
            return dup2(old_stdout, cstdout);
        }
        
        
        void rewind_fd(int fd) {
            lseek(fd, 0L, SEEK_SET);
        }
        """
        int open_temp_file()
        int replace_stdout(int temp_fileno)
        int restore_stdout(int old_stdout)
        void rewind_fd(int fd)



import io
import os

cdef class CoutCatcher():
    cdef int temp_file_fd
    cdef int old_fd

    cdef init_members(self):
        self.temp_file_fd = -1
        self.old_fd = -1        

    def __cinit__(self):
        self.init_members()

    def start(self): #start capturing
        if self.old_fd == -1:
            self.temp_file_fd = open_temp_file()
            self.old_fd = replace_stdout(self.temp_file_fd)
    
    def stop(self): # stops capturing, returns TextIOWrapper
        if self.old_fd != -1:
            restore_stdout(self.old_fd)
            rewind_fd(self.temp_file_fd) # need to read from the beginning
            buffer = io.TextIOWrapper(os.fdopen(self.temp_file_fd, 'rb'))
            self.init_members()
            return buffer
        return None

    def stop_and_read(self): # stops capturing, returns contents as string, frees resources (i.e. deletes files)
        buf = self.stop()
        if buf is not None:
            with buf:
                return buf.read()
        return None
