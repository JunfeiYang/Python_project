/* tcpportping.c */
#include <Python.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/time.h>
 
/* count time functions */
static double mytime(void)
{
    struct timeval tv;
    if (gettimeofday(&tv, NULL) == -1)
        return 0.0;
 
    return (double)tv.tv_usec + (double)tv.tv_sec * 1000000;
}
 
static PyObject *                                 /* returns object */
tcpping(PyObject *self, PyObject *args )
{
    struct  sockaddr_in addr;
    struct  hostent *hp;
    double  time;
    char    *host = NULL;
    int     fd;
    int     port, timeout;
 
    if (!PyArg_ParseTuple(args, "sii", &host, &port, &timeout))  /* convert Python -> C */
        return NULL;                              /* null=raise exception */
 
    if ((fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        return Py_BuildValue("d", -1.0);        /* convert C -> Python */
    }
 
    bzero((char *)&addr, sizeof(addr));
    if ((hp = gethostbyname(host)) == NULL) {
        return Py_BuildValue("d", -2.0);        /* convert C -> Python */
    }
    bcopy(hp->h_addr, &addr.sin_addr, hp->h_length);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
 
    struct timeval tv;
 
    tv.tv_sec = 0;
    tv.tv_usec = timeout * 1000;
 
    double stime = mytime();
    if (connect(fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        return Py_BuildValue("d", -3.0);        /* convert C -> Python */
    }
    fd_set read, write;
    FD_ZERO(&read);
    FD_ZERO(&write);
 
    FD_SET(fd, &read);
    FD_SET(fd, &write);
 
    if (select(fd + 1, &read, &write, NULL, &tv) == 0) {
        close(fd);
        return Py_BuildValue("d", -4.0);        /* convert C -> Python */
    }
 
    double etime = mytime();
    time = etime - stime;
    if (!FD_ISSET(fd, &read) && !FD_ISSET(fd, &write)) {
        close(fd);
        return Py_BuildValue("d", -4.0);        /* convert C -> Python */
    }
    close(fd);
    return Py_BuildValue("d", time/1000);        /* convert C -> Python */
}
 
/* registration table  */
static struct PyMethodDef portping_methods[] = {
    {"tcpping", tcpping, METH_VARARGS},       /* method name, C func ptr, always-tuple */
    {NULL, NULL}                   /* end of table marker */
};
 
/* module initializer */
void inittcpportping( )                       /* called on first import */
{                                      /* name matters if loaded dynamically */
    (void) Py_InitModule("tcpportping", portping_methods);   /* mod name, table ptr */
}
/*执行以下命令编译成python模块*/
/*gcc tcpportping.c  -I /usr/include/python2.7 -shared -L /usr/bin/ -fpic -l python2.7 -o tcpportping.so*/
