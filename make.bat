REM%~dp0docs\make html
for /f %%i in ('python -c "import sys, ploogz; sys.stdout.write(ploogz.__version__)"') do set VER=%%i
git tag %VER% -m "Adding a tag so that we can put this on PyPI."
git push --tags origin master
python setup.py sdist upload -r pypi



