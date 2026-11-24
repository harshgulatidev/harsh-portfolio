"""Build the public portfolio from its existing asset release; no credentials required."""
from pathlib import Path
from urllib.request import urlopen
from html import escape
import re
BASE = 'https://peaceful-lokum-2c2fee.netlify.app/'
OUT = Path('dist')
FILES = ["index.html","privacy.html","robots.txt","sitemap.xml","404.html","demo/wedding.html","assets/app.js","assets/favicon.svg","assets/font-abrilfatface.woff2","assets/font-alegreya.woff2","assets/font-catalog.json","assets/font-dmsans.woff2","assets/font-lora.woff2","assets/font-manrope.woff2","assets/font-sourcesans3.woff2","assets/free-fonts.json","assets/harsh.jpg","assets/social.jpg","assets/social.svg","assets/style.css","assets/LICENSE-abrilfatface.txt","assets/LICENSE-alegreya.txt","assets/LICENSE-dmsans.txt","assets/LICENSE-lora.txt","assets/LICENSE-manrope.txt","assets/LICENSE-sourcesans3.txt","fonts/abrilfatface.zip","fonts/alegreya.zip","fonts/dmsans.zip","fonts/lora.zip","fonts/manrope.zip","fonts/sourcesans3.zip"]
for name in FILES:
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(BASE + name, timeout=30) as response:
        target.write_bytes(response.read())
html = (OUT/'index.html').read_text(encoding='utf-8')
for form_id, subject, reply in [
 ('enquiryForm','New project enquiry | Harsh Gulati', 'Thank you for contacting Harsh Gulati. Your project brief has been received. I will review it and follow up personally. No work or charges begin until we agree the scope and quote. WhatsApp: +91 7011640244. Portfolio: https://harshgulati.work.gd/'),
 ('newsletterForm','Newsletter interest request | Harsh Gulati', 'Thank you for your interest in my free resources and development updates. This is an interest request only. Recurring newsletters will not start until a separate confirmation process is ready. You can request removal by replying to Harsh at harshgulati8966@gmail.com.')]:
    hidden = ''.join('<input type="hidden" name="'+k+'" value="'+escape(v,quote=True)+'">' for k,v in {'_subject':subject,'_template':'table','_autoresponse':reply,'_next':'https://harshgulati.work.gd/thank-you.html'}.items())
    html = re.sub(r'<form id="'+form_id+r'"[^>]*>', '<form id="'+form_id+'" method="POST" action="https://formsubmit.co/harshgulati8966@gmail.com">'+hidden, html)
html = html.replace('name="website"', 'name="_honey"')
html = re.sub(r'<input[^>]*name="form-name"[^>]*>', '', html)
html = html.replace('href="privacy.html"','href="/privacy.html"')
html = html.replace('</footer>', '<a href="https://dnsexit.com/" rel="noopener" target="_blank">DNS by DNSExit</a></footer>')
html = re.sub(r'<p[^>]*data-i="formNote"[^>]*>.*?</p>', '<p>FormSubmit delivers this form and may request a spam check. A thank-you email is requested after delivery. For a quick response, use WhatsApp.</p>', html)
html = re.sub(r'<p[^>]*data-i="newsletterCopy"[^>]*>.*?</p>', '<p>Register your interest in free resources and updates. This request does not start a newsletter subscription; email confirmation is being configured.</p>', html)
(OUT/'index.html').write_text(html)
js_path=OUT/'assets/app.js'
js=js_path.read_text(encoding='utf-8')
js=js.replace("e.preventDefault();if(!form.reportValidity())return;", "e.preventDefault();if(!form.reportValidity())return;form.submit();return;")
js_path.write_text(js)
(OUT/'thank-you.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Thank you | Harsh Gulati</title><link rel="stylesheet" href="/assets/style.css"><main class="simple-page"><h1>Thank you for getting in touch.</h1><p>Your request has been sent. I will follow up personally. Please check your inbox and spam folder for any acknowledgement.</p><p>Newsletter interest requests are not active subscriptions. No recurring updates will be sent until email confirmation is available.</p><a class="button lime" href="/">Back to portfolio</a><p><a href="https://wa.me/917011640244">Chat on WhatsApp</a></p></main></html>')
p=OUT/'privacy.html'
pv=p.read_text(encoding='utf-8').replace('Netlify Forms','FormSubmit and Harshs email inbox').replace('Form data is stored in FormSubmit and Harshs email inbox, separately from public website files.', 'Form submissions are transmitted to FormSubmit for spam checks and email delivery to Harsh. They may be processed and retained by that provider and in email backups. See https://formsubmit.co/privacy.pdf for its policy.')
p.write_text(pv)
print('Built',len(FILES),'assets plus thank-you page')

css_path=OUT/'assets/style.css'
css_path.write_text(css_path.read_text(encoding='utf-8')+'\n@media(max-width:700px){.hero-art{overflow:clip}}\n',encoding='utf-8')
