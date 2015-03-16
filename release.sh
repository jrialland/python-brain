#!/bin/bash
set -e

#run unit tests
PYTHONPATH=$PYTHONPATH:`pwd` python tests/all_tests.py
if [ $? -ne 0 ]; then
  echo 'unit tests failed !' >&2
  exit 1
fi

if [ ! -d '3to2-1.0' ]; then
	wget "https://bitbucket.org/amentajo/lib3to2/downloads/3to2-1.0.tar.gz"
	tar -zxvf 3to2-1.0.tar.gz
fi

#apply 3to2
for py in `find ./ -type f -name "*_py3.py"`; do
   py2=`echo $py | sed -e s/_py3/_py2/`
   cp $py $py2
   3to2-1.0/3to2 -w $py2
done

#apply autopep8 formatting
for py in `find ./ -type f -name "*.py"`; do
	autopep8 -i $py
done

#cleanup temporary files
find ./ -name "*.pyc" | xargs rm -f
find ./ -name "*.bak" | xargs rm -f
find ./ -type d -name "__pycache__" | xargs rm -rf

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
