# GenAI 11 Projects

A collection of 11 Python projects built with Streamlit. The apps
include AI-powered text tools, local language-model demos, web scraping,
and household/expense utilities.

## Projects

  ------------------------------------------------------------------------------------------------------------
                     \# Project          Main file                                          What it does
  --------------------- ---------------- -------------------------------------------------- ------------------
                      1 AI Email         `01_AI_Email_Improver/email_app.py`                Rewrites emails in
                        Improver                                                            a selected tone
                                                                                            using Gemini.

                      2 AI Hotel Booking `02_AI_Hotel_Booking_Assistant/hotel_app.py`       Drafts hotel guest
                        Assistant                                                           replies. It does
                                                                                            not make actual
                                                                                            reservations.

                      3 AI WhatsApp      `03_AI_WhatsApp_Reply_Generator/whatsapp_app.py`   Suggests replies
                        Reply Generator                                                     in a selected
                                                                                            tone, language,
                                                                                            and length. It
                                                                                            does not send
                                                                                            messages.

                      4 AI Expense       `04_AI_Expense_Analysis/`                          Expense-analysis
                        Analysis                                                            project. Run the
                                                                                            entry file you
                                                                                            used when testing
                                                                                            it.

                      5 AI Python Code   `05_AI_Python_Code_Explainer/code_explainer.py`    Explains pasted
                        Explainer                                                           Python code using
                                                                                            Gemini.

                      6 AI Question      `06_AI_Question_Answer_Generator/qa_app.py`        Answers questions
                        Answer Generator                                                    about a passage
                                                                                            using a local
                                                                                            FLAN-T5 model.

                      7 GPT-2 Text       `07_GPT2_Text_Generation/gpt2_app.py`              Continues a text
                        Generation                                                          prompt using a
                                                                                            local GPT-2 model.

                      8 Web Scraping     `08_Web_Scraping/web_scraper.py`                   Extracts titles,
                                                                                            headings,
                                                                                            paragraphs, and
                                                                                            links from
                                                                                            accessible HTML
                                                                                            pages.

                      9 Expense Helper   `09_Expense_Helper/expense_helper.py`              Records income and
                                                                                            expenses, shows
                                                                                            totals, and
                                                                                            exports
                                                                                            transactions.

                     10 Grocery          `10_Grocery_Assistant/grocery_app.py`              Maintains a
                        Assistant                                                           grocery list,
                                                                                            estimated cost,
                                                                                            and purchased
                                                                                            status.

                     11 Home Assistant   `11_Home_Assistant/home_assistant.py`              Tracks household
                                                                                            tasks, due dates,
                                                                                            priorities, and
                                                                                            completion.
  ------------------------------------------------------------------------------------------------------------

> Project 4's exact entry-point filename was not confirmed here. Use the
> actual filename in that folder.

## Requirements

-   Windows with PowerShell
-   Python and the installed dependencies
-   Internet connection for package installation and first-time model
    downloads
-   A Gemini API key for projects that call Gemini

## Setup

Open PowerShell and move to the project root:

``` powershell
cd "C:\Users\hp\Desktop\D-drive\coding\jupiterAnaconda\Project-143\Project-143\GenAI_11_Projects"
```

Activate the virtual environment:

``` powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies if needed:

``` powershell
python -m pip install --upgrade pip
python -m pip install streamlit google-genai openai transformers torch sentencepiece requests beautifulsoup4 pandas
```

## Gemini API key

Set your key in the same PowerShell window before launching a
Gemini-powered app:

``` powershell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

Replace the placeholder locally. Do not put your real key in this
README, source code, screenshots, Git repositories, or messages. This
environment variable lasts only for the current PowerShell session.

Verify the key is set without printing it:

``` powershell
python -c "import os; print('API key detected:', bool(os.getenv('GEMINI_API_KEY')))"
```

## Run the apps

Run one Streamlit app at a time from the project root. Stop the current
app with `Ctrl+C` before starting another.

``` powershell
python -m streamlit run ".\01_AI_Email_Improver\email_app.py"
python -m streamlit run ".\02_AI_Hotel_Booking_Assistant\hotel_app.py"
python -m streamlit run ".\03_AI_WhatsApp_Reply_Generator\whatsapp_app.py"
python -m streamlit run ".\05_AI_Python_Code_Explainer\code_explainer.py"
python -m streamlit run ".\06_AI_Question_Answer_Generator\qa_app.py"
python -m streamlit run ".\07_GPT2_Text_Generation\gpt2_app.py"
python -m streamlit run ".\08_Web_Scraping\web_scraper.py"
python -m streamlit run ".\09_Expense_Helper\expense_helper.py"
python -m streamlit run ".\10_Grocery_Assistant\grocery_app.py"
python -m streamlit run ".\11_Home_Assistant\home_assistant.py"
```

For Project 4, run the entry-point file you used when testing it. For
example, if it is named `app.py`:

``` powershell
python -m streamlit run ".\04_AI_Expense_Analysis\app.py"
```

Change `app.py` if your filename differs. Streamlit usually provides the
local URL `http://localhost:8501`.

## Local models

Projects 6 and 7 use Hugging Face Transformers models. Their first run
downloads model files and may take time depending on internet speed.
They do not need a Gemini API key.

## Data and privacy

-   Projects 9, 10, and 11 save records in JSON files in their own
    project folders.
-   Project 8 parses the HTML returned by a website; some websites block
    requests or load content through JavaScript.
-   Do not enter passwords, payment details, or other sensitive
    information into prompts or test pages.
-   Keep saved JSON files private if they contain personal records.

## Troubleshooting

### Gemini returns `503 UNAVAILABLE` / high demand

This is a provider-side availability or capacity error. It does not
necessarily mean the code or API key is wrong. Try again later or test a
model available to your API key rather than repeatedly guessing model
names.

### API key missing

Set `GEMINI_API_KEY` in the same PowerShell session used to launch
Streamlit.

### Package missing

Activate the virtual environment and run:

``` powershell
python -m pip install PACKAGE_NAME
```

Replace `PACKAGE_NAME` with the missing package named in the error.

### Streamlit is already running

In the PowerShell window running it, press `Ctrl+C`, then launch the app
you want.

### Local model download fails

Check the internet connection and try again. The first FLAN-T5 or GPT-2
download can take longer than later launches.

## Project status

The project creator reports checking the apps one by one. Gemini-based
generation may still encounter intermittent `503 high demand` responses,
so successful app launch and successful AI generation should be checked
separately.

## Suggested improvements

-   Add screenshots of each project.
-   Add a `requirements.txt` file.
-   Add tests and input validation.
-   Add a `.gitignore` for `venv/`, local data files, and secrets.
-   Keep API keys in environment variables rather than source code.
