
with open('some path', 'r') as f:
    orig_text = f.read()
    new_text = '<?xml ...>\n' + orig_text
with open('some path', 'w') as f:
    f.write(new_text)
