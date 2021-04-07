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
├── CONTRIBUTING.md
├── LICENSE
├── poetry.lock
├── pyproject.toml
└── README.md
```


## Contribute to this repository
For adding a new analysis, please submit PR with your analysis as a script added to `bin/`.
If you feel the tool in the script needs more robust maintenance, refactor it and add to `nkicap/` with tests.
We use pytest for testing and black for formatting.
If the above three lines make no sense to you, see detailed [contribution guideline](CONTRIBUTING.md).
