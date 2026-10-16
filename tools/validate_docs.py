"""Check local documentation links, SVG structure, provenance and teaching math.

Run with Python 3: python tools/validate_docs.py
No external Python dependencies are required. This does not validate MATLAB.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from fractions import Fraction
import json, math, re, sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
errors=[]
warnings=[]
count=0
for file in ROOT.rglob('*.md'):
 if '.git' in file.parts: continue
 count+=1
 text=file.read_text(encoding='utf-8')
 if 'https://www.google.com/search?q=' in text:
  errors.append(f'{file.relative_to(ROOT)}: search-result link remains')
 if '**English Original**' in text:
  errors.append(f'{file.relative_to(ROOT)}: ambiguous original-text label remains')
 if text.count('```') % 2:
  errors.append(f'{file.relative_to(ROOT)}: unmatched code fence')
 for match in re.finditer(r'(!?)\[([^\]]*)\]\(([^\s)]+)\)',text):
  is_image,alt,dest=match.groups()
  parts=urlsplit(dest)
  if parts.scheme or dest.startswith('//'): continue
  if not parts.path: continue
  path=(file.parent/unquote(parts.path)).resolve()
  try: path.relative_to(ROOT)
  except ValueError:
   errors.append(f'{file.relative_to(ROOT)}: local link escapes repository: {dest}')
   continue
  if not path.exists(): errors.append(f'{file.relative_to(ROOT)}: missing target: {dest}')
  if is_image and not alt.strip(): errors.append(f'{file.relative_to(ROOT)}: missing image description')

for file in (ROOT/'assets').glob('*.svg'):
 try:
  node=ET.parse(file).getroot()
  if node.tag!='{http://www.w3.org/2000/svg}svg': errors.append(f'{file.name}: incorrect SVG root')
  if node.find('{http://www.w3.org/2000/svg}title') is None: errors.append(f'{file.name}: missing title')
  if node.find('{http://www.w3.org/2000/svg}desc') is None: errors.append(f'{file.name}: missing description')
 except ET.ParseError as ex: errors.append(f'{file.name}: {ex}')

def rank(rows):
 a=[[Fraction(v) for v in row] for row in rows]
 r=0
 for c in range(len(a[0])):
  pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
  if pivot is None: continue
  a[r],a[pivot]=a[pivot],a[r]
  scale=a[r][c]; a[r]=[v/scale for v in a[r]]
  for i in range(len(a)):
   if i!=r:
    factor=a[i][c]; a[i]=[v-factor*w for v,w in zip(a[i],a[r])]
  r+=1
  if r==len(a): break
 return r

try:
 # Independent checks of stated mathematical examples, not simulations of EEG.
 assert max(abs(math.sin(math.pi*n)) for n in range(20)) < 1e-12
 assert math.isclose(3/3,1.0)
 x=[2+0.8*t for t in [0,1,2,3,4]]
 corrected=[v-2.4 for v in x]
 assert all(math.isclose(corrected[i+1]-corrected[i],0.8) for i in range(4))
 assert rank([[1,0],[0,1],[1,1]])==2
 assert rank([[Fraction(1,2),Fraction(-1,2)],[Fraction(-1,2),Fraction(1,2)]])==1
 assert rank([[Fraction(1,2),Fraction(-1,2)],[Fraction(-1,2),Fraction(1,2)],[Fraction(1,2),Fraction(1,2)]])==2
 assert math.isclose(10*math.log10(2),3.0102999566,abs_tol=1e-9)
 assert math.isclose(10*math.log10(4),6.0205999133,abs_tol=1e-9)
except AssertionError:
 errors.append('Teaching mathematical identity check failed')

manifest=json.loads((ROOT/'docs/source_manifest.json').read_text(encoding='utf-8'))
for entry in manifest['entries']:
 if entry.get('http_status')!=200:
  warnings.append(f'Source needs separate verification: {entry["url"]} (status {entry.get("http_status")})')
 if entry.get('http_status')==200 and not entry.get('sha256'):
  errors.append(f'Missing source checksum: {entry["url"]}')

print(json.dumps({'markdown_files':count,'svg_files':len(list((ROOT/'assets').glob('*.svg'))),'sources':len(manifest['entries']),'errors':errors,'warnings':warnings,'matlab_runtime_validation':False},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
