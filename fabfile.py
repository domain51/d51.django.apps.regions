from fabric.api import local

def test():
    "Run tests"
    print local("python ./run_tests.py", capture=True)

def init():
    "Initialize a virtualenv and install requirements"
    local("virtualenv .")
    local("pip install -E . -r requirements.txt")

def clean():
    "Remove the cruft created by virtualenv and pip"
    local("rm -rf bin/ include/ lib/ build/ MANIFEST")

def install():
    "Install"
    local("python setup.py install")
