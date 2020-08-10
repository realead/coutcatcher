from libc.stdio cimport printf, fprintf, stderr

def print_to_stdout(const char* s):
    printf("%s", s)
    
def print_to_stderr(const char* s):
    fprintf(stderr, "%s", s)
