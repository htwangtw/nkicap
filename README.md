# Resting state coactivation pattern (CAP) and thoughts during RS scan
Cool project

```
.
├── bin/                    Scripts of the analysis.
├── data/                   Data used to generate results
├── nkicap/                 Tools used to help the analysis. Content here need to pass CI
│   ├── tests/
│   └── utils.py
├── results/                Output of the analysis
├── CONTRIBUTING.md         Detailed contribution guideleines
├── LICENSE                 Duh
├── poetry.lock             Poetry created full dependency tree
├── pyproject.toml          Poetry project meta data - all you need for all dependency
└── README.md
```
## Dependency
- Python version 3.8
- Poetry version 1.1.4

Install poetry:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
```

Run this project locally:
```
git clone https://github.com/htwangtw/nkicap.git
cd nkicap
poetry install
```

Activate the related virtual environment
```
poetry shell
```

## Contribute to this repository
The dependecy of this project is managed with [poetry](https://github.com/python-poetry/poetry).

For adding a new analysis, please submit PR with your analysis as a script added to `bin/`.

If you feel the tool in the script needs more robust maintenance, refactor it and add to `nkicap/` with tests.

We use pytest for testing and black for formatting.

If the above three lines make no sense to you, see detailed [contribution guideline](CONTRIBUTING.md).