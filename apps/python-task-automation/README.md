# Python task automation

Five independent command-line examples accompany the [article](https://todatabeyond.com/blog/practical-guide-to-task-automation-using-chatgpt-and-python) and [notebook](../../ChatGPT_Python_Task_Automation.ipynb).

Use Python 3.13 (tested: 3.13.7). Create a dedicated virtual environment, install
`pip install -r requirements.txt` from this directory, and install FFmpeg as a
system program for the notebook's synthetic MP3-to-WAV conversion. No OpenAI key
is needed for these five scripts. Google speech recognition and Google Translate
TTS are network services; only send audio/text you own and may share. Availability
is not guaranteed. The speech endpoint uses HTTPS and a trusted certifi CA bundle.

```bash
python text_audio.py example.txt example.mp3
ffmpeg -i example.mp3 -ac 1 -ar 16000 example.wav
python audio_text.py example.wav
python weather_report.py "Cairo"
python currency_converter.py 100 USD EUR
```

Create `example.txt` containing your own English text first. The notebook creates
its own small phrase and verifies the resulting transcript. wttr.in reports
current weather; Frankfurter supplies dated reference exchange rates, not a
transaction quote. Amounts use Decimal and two-place display rounding.

## Local email capture, not real delivery

Run `python -m aiosmtpd -n -l 127.0.0.1:8025` in one terminal, then
`python automate_email.py` in another. Default addresses use the reserved
`.invalid` domain, and the default host is loopback. The notebook starts and
stops its own local capture and checks the SMTP envelope, headers and body.
No real email was sent during validation.

Remote SMTP is an optional manual deployment, not the tested demonstration.
It requires explicit `--allow-remote --starttls`, a provider host/port, real
addresses and environment-only `SMTP_USERNAME`/`SMTP_PASSWORD` credentials.
Use a provider-supported OAuth client for OAuth authentication; this simple
password-login script can use an eligible Gmail app password after two-step
verification. Do not use your normal Gmail password or enable Less Secure Apps.
See [Google's app-password instructions](https://support.google.com/mail/answer/185833?hl=en).
Python already includes smtplib and email; do not install secure-smtplib.

## Validation

The complete companion notebook passed seven code cells in a fresh kernel:
real speech/TTS, weather and currency requests; local-only SMTP capture; and
regressions for invalid inputs, Decimal arithmetic, missing CLI arguments,
remote-email refusal, header injection and connection-failure cleanup.
Captured service results are run-specific, not guaranteed future values.
Committed notebooks are output-free; the article carries the actual results.
Original scripts, prompts and setup instructions remain verbatim in its
nonexecuting appendix. The original source repository is also linked in the
article. The maintained scripts here are the runnable path.
