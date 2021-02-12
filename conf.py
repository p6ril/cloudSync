# "private" variables for convenience

USER_HOME = "/home/gandalf"
DOCUMENTS = USER_HOME + "/Documents"
TRESORIT_DRIVE = USER_HOME + "/Tresors"
INTERNXT_DRIVE = USER_HOME + "/Internxt Drive"

# only FILE_LIST and FOLDER_LIST are imported in cloudsync.py

FILE_LIST = (
    {'src': DOCUMENTS + "/KeePassXC.kdbx", 'dst': TRESORIT_DRIVE + "/security"},
    {'src': DOCUMENTS + "/KeePassXC-noyubikey.kdbx", 'dst': TRESORIT_DRIVE + "/security"},
)

FOLDER_LIST = (
    {
        'src': TRESORIT_DRIVE + "/finance",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete",
            "--exclude=.tresorit"
        )
    },
    {
        'src': TRESORIT_DRIVE + "/documents",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete",
            "--exclude=.tresorit"
        )
    },
    {
        'src': TRESORIT_DRIVE + "/music",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete",
            "--exclude=.tresorit"
        )
    },
    {
        'src': TRESORIT_DRIVE + "/security",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete",
            "--exclude=.tresorit",
            "--exclude=security/archives"
        )
    },
    {
        'src': USER_HOME + "/dev/cloudsync",
        'dst': TRESORIT_DRIVE + "/gitbackup",
        'options': (
            "-rpAXogEtc",
            "--delete",
            "--exclude=.git",
            "--exclude=.idea",
            "--exclude=venv",
            "--exclude=__pycache__",
            "--exclude=*.swp"
        )
    },
    {
        'src': USER_HOME + "/dev/joplinRevisionsCleanUp",
        'dst': TRESORIT_DRIVE + "/gitbackup",
        'options': (
            "-rpAXogEtc",
            "--delete",
            "--exclude=.git",
            "--exclude=.idea",
            "--exclude=venv",
            "--exclude=*.swp"
        )
    },
    {
        'src': USER_HOME + "/dev/dirdiff",
        'dst': TRESORIT_DRIVE + "/gitbackup",
        'options': (
            "-rpAXogEtc",
            "--delete",
            "--exclude=.git",
            "--exclude=*.swp"
        )
    },
    {
        'src': TRESORIT_DRIVE + "/gitbackup",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete", 
            "--exclude=.tresorit"
        )
    }
)
