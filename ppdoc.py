import pdoc
from pathlib import Path
from markdown_it import MarkdownIt
from pathlib import Path
import shutil

OUTPUT_DIR = Path('docs')

MODULES = [
    'QFlow',
    'examples.example'
]

import pdoc.cli
import sys

mdHTML = MarkdownIt(
    'commonmark',
    {
        'html': True,
        'linkify': True,
        'typographer': True,
    }
)

readmeHTML = mdHTML.render(open('README.md', encoding='utf-8').read())

indexHTML = \
r'''
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>QFlow Docs</title>
    <style>
        body {
            background-color: #0d1117;
            color: white;
            font-family: -apple-system,
                        BlinkMacSystemFont,
                        "Segoe UI",
                        Helvetica,
                        Arial,
                        sans-serif;
            padding: 10px 20px 10px 20px
        }

        a {
            color: #58a6ff;
        }

        pre, code {
            background-color: #161b22;
            border-radius: 2px;
            padding: 1em 1em;
        }

        .navbar {
            background: #0d1117;
            padding: 10px 20px;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .menu {
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .menu > li {
            position: relative;
            display: inline-block;
        }

        .menu a {
            color: #c9d1d9;
            text-decoration: none;
            padding: 8px 12px;
            display: block;
        }

        .menu a:hover {
            color: #ffffff;
        }

        .dropdown-menu {
            display: none;
            position: absolute;
            background: #161b22;
            list-style: none;
            padding: 5px 0;
            margin: 0;
            min-width: 160px;
            border-radius: 2px;
            box-shadow: 0 8px 24px rgba(0,0,0,.3);
        }

        .dropdown-menu li a {
            padding: 8px 14px;
        }

        .dropdown-menu li a:hover {
            background: #21262d;
        }

        .dropdown:hover .dropdown-menu {
            display: block;
        }
    </style>
    <link rel="icon" href="assets/icons/QFlow-white-icon.png">
</head>
<body>
    <nav class="navbar">
        <ul class="menu">
            <li class="dropdown">
                <a href="#">Docs ▾</a> <!-- # No Icon -->
                <ul class="dropdown-menu">
                    <li><a href="QFlow/index.html">QFlow</a></li>
                    <li><a href="examples/example.html">Example</a></li>
                </ul>
            </li>
        </ul>
    </nav>
    
    %readme%
</body>
</html>
'''

def index() -> None:
    indexPath = OUTPUT_DIR / 'index.html'
    indexPath.write_text(indexHTML.replace(r'%readme%', readmeHTML), encoding='utf-8')

    src = Path('assets')
    dst = Path('docs/assets')

    shutil.copytree(
        src,
        dst,
        dirs_exist_ok=True
    )


def main():
    sys.argv = [
        'pdoc',
        '--html',
        '--force',
        '--output-dir', 'docs',
        *MODULES
    ]

    pdoc.cli.main()

    index()

if __name__ == '__main__':
    main()