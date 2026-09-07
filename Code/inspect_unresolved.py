import pandas as pd
df = pd.read_csv(r'd:\tm\05_Own_Research\Data\master_screening_database.csv', dtype=str, encoding='utf-8-sig').fillna('')
unresolved = df[df['ta_decision'] == '']
print(f'Unresolved total: {len(unresolved)}')

empty_abs = unresolved[unresolved['abstract_snippet'].str.len() < 20]
has_abs = unresolved[unresolved['abstract_snippet'].str.len() >= 20]
print(f'No/minimal abstract: {len(empty_abs)} ({100*len(empty_abs)/len(unresolved):.1f}%)')
print(f'Has abstract: {len(has_abs)} ({100*len(has_abs)/len(unresolved):.1f}%)')
print()

print('--- SAMPLE: Unresolved WITH abstract (first 10) ---')
for _, row in has_abs.head(10).iterrows():
    title = str(row['title'])[:90]
    yr = str(row['year'])
    src = str(row['database_source'])
    print(f'  [{yr}][{src}] {title}')

print()
print('--- SAMPLE: Unresolved WITHOUT abstract (first 10) ---')
for _, row in empty_abs.head(10).iterrows():
    title = str(row['title'])[:90]
    yr = str(row['year'])
    src = str(row['database_source'])
    print(f'  [{yr}][{src}] {title}')
