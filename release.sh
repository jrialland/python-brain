#!/bin/bash

version=`python << '__eof'
import brain
print brain.__version__
__eof`

git tag "$version" -m "releasing version $version"
git push --tags origin master

#in order to publish to pipy, the account infos (obtained at https://pypi.python.org/pypi?%3Aaction=register_form)
#should written to a .pypirc file for the current user.
#[distutils] # this tells distutils what package indexes you can push to
#index-servers = pypitest
#
#[pypi]
#repository: https://pypi.python.org/pypi
#username=
#password=
#
#[pypitest]
#repository: https://testpypi.python.org/pypi
#username: jrialland

python setup.py register -r pypi
python setup.py sdist upload -r pypi