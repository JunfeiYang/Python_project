#__*__ encoding: utf-8: __*__
import apachelog,sys


if len(sys.argv) == 2:
  # Format copied and pasted from Apache conf - use raw string + single quotes
  format = r'%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"'

  p = apachelog.parser(format)
  log_file = sys.argv[1]
  for line in open(log_file):
    try:
       data = p.parse(line)
    except:
       sys.stderr.write("Unable to parse %s" % line)

####
else:
   print ''' "usage: %s logfile" % sys.argv[0]
             "ex:    %s  apachelog" % sys.argv[0]"
         '''
   sys.exit(2)
            
    

