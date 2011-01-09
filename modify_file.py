import re
import string

### Requirements ###########################
# This requires <scopecontent> tags on each field

new_id_digits = 4
collection_name = 'P0034'

pattern = r'">P0034/(.+)</container>'
prog = re.compile(pattern)

with open('P0034_Python.xml', 'r') as f:
    out_file = open('P0034_output.xml', 'w')
    translation_file = open('P0034_translation.xml', 'w')
    translation_file.write('Naming Translation for Collection: %s\n\n' % collection_name)
    entry_num = 1
    for k, line in enumerate(f.xreadlines()):
        result = prog.search(line)
        if result:
            #print 'original %s' % line
            old_description = result.group(1)
            #Replace the old description with the new ID
            id = string.zfill(entry_num, new_id_digits)
            new_id = '%s/%s' % (collection_name, id)
            repl = '">%s</container>' % new_id
            modified_line = re.sub(pattern, repl, line)

            #Put the tag in the scopecontent section
            if '/did><scopecontent></scopecontent>' in modified_line:
                repl = '<p>Barnes original number: %s.</p></scopecontent>' % old_description
                modified_line = re.sub('</scopecontent>', repl, modified_line)
            elif '/did><scopecontent><p></p>' in modified_line:
                repl = '/did><scopecontent><p>Barnes original number: %s.' % old_description
                modified_line = re.sub('/did><scopecontent><p>', repl, modified_line)
            elif '/did><scopecontent><p>' in modified_line:
                repl = '/did><scopecontent><p>Barnes original number: %s; ' % old_description
                modified_line = re.sub('/did><scopecontent><p>', repl, modified_line)
            else:
                exc = Exception("Line '%s' is invalid" % modified_line)
                print exc
            entry_num = entry_num + 1
            line = modified_line
            translation_file.write("'%s' => '%s'\n" % (old_description, id))
            #print '%s\n' % modified_line
        out_file.write(line)
f.closed
translation_file.close()
out_file.close()
