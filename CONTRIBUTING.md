# Contribution guildeline

Mostly follows [guildlines from `nibabel`](https://nipy.org/nibabel/devel/devguide.html)

## Install development environment
This project is built on `poetry`.

Install poetry:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
```

Fork this repository and install the environment, clone your own fork
```
git clone https://github.com/URUSERNAME/nkicap.git
```

Install the environment
```
cd nkicap
poetry install
```
Activate the virtual environment to use it
```
poetry shell
```

## Add your analyis
1. Open an issue at the [upstream repository](https://github.com/htwangtw/nkicap/issues)
2. Update your fork from the upstream when your main branch is behind. This step is extremely important.
On your main branch:
```
git remote add upstream https://github.com/htwangtw/nkicap.git
git fetch upstream
git rebase upstream/main
git push origin main --force
```
4. Create a branch for the analysis you want to add and commit all your analysis to this branch
```
git checkout -b my-new-analysis
```
5. Create a pull request on the [upstream repository](https://github.com/htwangtw/limmpca/pulls)
@htwangtw will review your work and help you from here.

For more git related stuff on contributing, checkout [git for development](https://nipy.org/nibabel/gitwash/git_development.html)

## Suggestions on commit message formats
Please prefix all commit summaries with one (or more) of the following labels. 
This should help others to easily classify the commits into meaningful categories:
- BF : bug fix
- RF : refactoring
- NF : new feature
- BW : addresses backward-compatibility
- OPT : optimization
- BK : breaks something and/or tests fail
- PL : making pylint happier
- DOC: for all kinds of documentation related commits
- TEST: for adding or changing tests
