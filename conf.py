# "private" variables for convenience

USER_HOME = "/home/gandalf"
DOCUMENTS = USER_HOME + "/Documents"
SPIDEROAK_HIVE = USER_HOME + "/SpiderOak Hive"
INTERNXT_DRIVE = USER_HOME + "/Internxt Drive"

# only FILE_LIST and FOLDER_LIST are imported in cloudsync.py

FILE_LIST = (
    {'src': DOCUMENTS + "/KeePassXC.kdbx", 'dst': SPIDEROAK_HIVE + "/security"},
    {'src': DOCUMENTS + "/KeePassXC-noyubikey.kdbx", 'dst': SPIDEROAK_HIVE + "/security"},
)

FOLDER_LIST = (
    {
        'src': SPIDEROAK_HIVE + "/finance",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete"
        )
    },
    {
        'src': SPIDEROAK_HIVE + "/documents",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete"
        )
    },
    {
        'src': SPIDEROAK_HIVE + "/music",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete"
        )
    },
    {
        'src': SPIDEROAK_HIVE + "/security",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete",
            "--exclude=security/archives", )
    },
    {
        'src': USER_HOME + "/dev/cloudsync",
        'dst': SPIDEROAK_HIVE + "/gitbackup",
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
        'dst': SPIDEROAK_HIVE + "/gitbackup",
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
        'src': SPIDEROAK_HIVE + "/gitbackup",
        'dst': INTERNXT_DRIVE,
        'options': (
            "-rpAXogEt",
            "--delete"
        )
    }
)
