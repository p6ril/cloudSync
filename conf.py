# "private" variables for convenience

USER_HOME = "~"
DOCUMENTS = USER_HOME + "/Documents"

# only FILE_LIST and FOLDER_LIST are imported in cloudsync.py

FILE_LIST = (
    {'src': DOCUMENTS + "/source_file", 'dst': "destination directory full path"},
)

FOLDER_LIST = (
    {
        'src': "source directory full path",
        'dst': "destination directory full path",
        'options': (
            "-rpAXogEt",
            "--delete",
            "--exclude=tmp"
        )
    },
)
