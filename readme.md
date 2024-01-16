## Initial tips for developers
1. Do not push `data`, `images` and LLM submodules.
2. `test.ipynb` and `playground.py` have been added to `.gitignore`, one can use them for testing purposes.
3. Place general utilities in `utils.py` and use them as much as possible.
4. `main.py` is used for running all project services. Make sure your service works properly before commiting it.
5. Describing the usage of your component or service in `readme.md` for teammates is **highly recommended**.