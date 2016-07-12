from datetime import datetime

str = '''
<html>
    <body>
        <p> Generated: {t}</p>
    </body>
</html>
'''.format(t = datetime.now())

print (str)
