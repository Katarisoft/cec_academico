

{
    # The human-readable name of your module, displayed in the interface
    'name': "Web académico",
    # A more extensive description
    'description': """
    """,
    # Which modules must be installed for this one to work
    'depends': ['base', 'curso', 'cec_alumnos', 'cec_docentes','website'],

    # data files which are always installed
    'data': [
        'templates.xml',
    ]

}

