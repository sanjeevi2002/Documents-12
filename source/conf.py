project = 'Ethernet Communication'
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Ethernet Communication'
copyright = '2026, '
author = ''
release = '1.0'
latex_documents = [
    ('index', 'Ethernet_Communication.tex', project, author, 'manual'),
]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_title = 'Ethernet Communication'

html_logo = '_static/project_logo.svg'

# Logo size adjustment
html_css_files = ['custom_logo_scale.css', 'custom_overrides.css']

# Generated RST files: rstfile1

html_js_files = ['spx_pdf_download.js', 'spx_img_click.js']

latex_engine = 'pdflatex'

latex_toplevel_sectioning = 'section'

# Ensure LaTeX assets are copied to build directory
try:
    latex_additional_files
except NameError:
    latex_additional_files = []
for _p in ['_static/header.png', '_static/footer.png']:
    if _p not in latex_additional_files:
        latex_additional_files.append(_p)

# SPX_ENSURE_BABEL
latex_elements = globals().get('latex_elements', {})
_spx_lang = globals().get('language', 'en') or 'en'
if not isinstance(_spx_lang, str) or not _spx_lang.strip():
    _spx_lang = 'en'
_spx_lang_norm = _spx_lang.strip().lower().replace('_', '-')
_spx_lang_map = {'en': 'english', 'en-us': 'english', 'en-gb': 'british'}
_spx_lang_final = _spx_lang_map.get(_spx_lang_norm, _spx_lang_norm or 'english')
if not latex_elements.get('babel'):
    latex_elements['babel'] = r'\usepackage[' + _spx_lang_final + ']{babel}'

# Apply the supplied PHYTEC branding to the cover and document pages.
latex_elements['preamble'] = latex_elements.get('preamble', '') + r'''
\usepackage{fancyhdr}
\setlength{\headheight}{40pt}
\setlength{\headsep}{12pt}
\newcommand{\phytecpage}{
  \fancyhf{}
  \fancyhead[C]{\includegraphics[width=\textwidth]{header.png}}
  \fancyfoot[L]{\includegraphics[width=0.82\textwidth]{footer.png}}
  \fancyfoot[R]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}
\fancypagestyle{normal}{\phytecpage}
\fancypagestyle{plain}{\phytecpage}
\fancypagestyle{empty}{\phytecpage}
'''

# Prevent even-page blanks and simplify Sphinx maketitle
