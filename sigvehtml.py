import sys
import re


def convert(lines):

    # remove \n
    lines = [line[:-1] for line in lines]

    boxes = [[] for i in range(len(lines))]

    for y, line in enumerate(lines):
        if '#' in line:
            for x, letter in enumerate(line):
                if letter == '#':
                    boxes[y].append(x)

    boxes = filter(lambda x: x[1], enumerate(boxes))

    output = []

    for i in range(0, len(boxes), 2):
        start = boxes[i]
        end = boxes[i + 1]

        output.append(row())

        for j in range(0, len(start[1]), 2):
            topleft = start[0], start[1][j]
            topright = start[0], start[1][j + 1]
            bottomleft = end[0], end[1][j]
            bottomright = end[0], end[1][j + 1]

            width = (topright[1] - topleft[1] + 2) / 6

            output.append(div(width))

            # do we think it is a picture?
            picture = True
            for line in lines[topleft[0] + 1:bottomleft[0]]:
                line = line[topleft[1] + 1:topright[1]]
                if 'the' in line or 'Download' in line:
                    picture = False

            if picture:
                image = educated_guess_at_image()
                output.append('<img style=width:100%%;margin-bottom:40px;display:block src="%s" />' % image)
            else:
                output.append('<p>\n')
                for _line in lines[topleft[0] + 1:bottomleft[0]]:
                    line = _line[topleft[1] + 1:topright[1]]
                    if not line.strip():
                        output.append('</p>\n<p>\n')
                    else:
                        if '*' in line:
                            idx = line.find('*')
                            text = line[idx+2:].strip()
                            # yes, we cheat and drop the ul tags
                            output.append('<li><a href="%s">%s</a></li>' % (re.sub(' ','-', text.lower()), text))
                        else:
                            output.append(line)
                output.append('</p>\n')
            output.append(div_end())
        output.append(row_end())

    return header() + ''.join(output) + footer()


def row():
    return '<div class="row">\n'


def div(width):
    return '<div class="col-xs-%s">\n' % str(width)

def div_end():
    return '</div>'

def row_end():
    return div_end()


def header():
    return """
<!DOCTYPE html>
<html>
    <head>
    <title>Sigvehtml</title>
    <meta charset="utf8" />
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <link rel="stylesheet" type="text/css" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css">
    </head>
    <body>

    <header>
    <h1>Sigvehtml</h1>
    </header>

    <div class="container">
    """


def footer():
    return """
    </div>

    </body>
</html>
"""

def educated_guess_at_image():
    return 'http://pensivetoaster.com/wp-content/uploads/2013/05/elephant-banner.jpg'


def main():

    with open(sys.argv[1], 'r') as f:
        lines = [line for line in f]

    output = convert(lines)
    print output


if __name__ == "__main__":
    main()
