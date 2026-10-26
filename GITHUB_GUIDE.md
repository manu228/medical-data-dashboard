# Beginner-friendly GitHub upload and deployment guide

## Option A: Upload directly in your browser (no Git install)

1. Visit [github.com](https://github.com) and create/sign in to a free account.
2. Click the **+** menu → **New repository**.
3. Name it `medical-data-dashboard`, set **Public**, and click **Create repository**.
4. On the empty repository page, select **uploading an existing file**.
5. Extract the ZIP file and upload the **contents of the `medical-data-dashboard` folder**, including `app.py`, `analysis.py`, `requirements.txt`, `README.md`, `RESULTS.md`, `GITHUB_GUIDE.md`, `data/`, `screenshots/`, and `tests/`. Depending on your browser, drag the folders or upload files by folder. **Do not upload only the ZIP**; Streamlit needs individual source files.
6. GitHub's browser uploader may skip hidden files, so `.gitignore` is optional at first. Do not upload any passwords or API keys.
7. Enter `Initial release: CellScope medical data dashboard` as a commit message and click **Commit changes**.
8. Confirm the README preview and screenshot display correctly. Copy the repository address; put that link on your résumé.

## Option B: Run on your Mac

Install **Python 3.10 or newer** from [python.org](https://www.python.org/downloads/) if needed. Extract the ZIP, then open Terminal and run:

```bash
cd ~/Downloads/medical-data-dashboard
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 -m streamlit run app.py
```

Terminal should open the app in your default web browser (usually localhost:8501). If it doesn't, copy the Local URL and paste it into your browser.

When finished, press `Ctrl+C` in Terminal to stop the app, and `deactivate` to exit the virtual environment.

## Deploy a public interactive demo — free, no local install required

1. Once the **individual files** are committed to your GitHub repository, visit [share.streamlit.io](https://share.streamlit.io).
2. Sign in using GitHub, authorize access if prompted, and select **Create app**.
3. Choose **Yup, I have an app** or the existing repository deployment option.
4. Set repository to `your-username/medical-data-dashboard`, branch to `main`, and main file path to `app.py`.
5. Click **Deploy**. The service installs packages from `requirements.txt` and gives you a URL such as `https://your-app-name.streamlit.app`.
6. Open the deployed URL and verify the filters, box plot, scatter plot and CSV download work.
7. Add that public demo URL under the README introduction and in your portfolio.

If GitHub browser upload struggles with folders, use the free **GitHub Desktop** app, which can publish a local project folder without commands.

## What to put on your résumé

**CellScope — Interactive Medical Data Explorer** | Python, Pandas, Streamlit, Plotly, scikit-learn
- Developed an interactive dashboard analyzing 569 real cytology image samples, with responsive diagnostic-label filters and descriptive feature comparisons.
- Implemented box plots, scatter plots, summary statistics, reproducible tests, and downloadable filtered data; documented data limitations.

Add your actual GitHub URL and deployed demo URL as links.

## What to say in cold emails

> I recently built a Python/Streamlit medical data explorer to analyze diagnostic image features using an open UCI dataset. The project includes interactive filtering, statistical summaries, and transparent documentation. The code and screenshots are on GitHub: [your real link].

Replace the bracketed link only after you upload the project. Do not claim it is deployed until your public link works.
