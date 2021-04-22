import csv
import datetime

csv.field_size_limit(100000000)
vacs = list(csv.DictReader(open('C:\\Users\\iKerng\\Python\\Data\\vacancy.csv', encoding='utf-8', newline='')))

# Сколько вакансий, которые вам нравятся?
# Насколько свежие эти вакансии?
# Сколько вакансий с позициями на которых вы работаете?
# Сколько вакансий для аналатика данных?
# Сколько вакансий для аналитика данных с использованием Python?

vac_like = 0
count_work_vac = 0
count_da_vac = 0
count_da_vac_py = 0
count_vac_fresh_month = 0
count_vac_fresh_kvartal = 0
count_vac_fresh_halfyear = 0
count_vac_fresh_older_halfyear = 0

for i in range(len(vacs)):
    # Сколько вакансий с позициями на которых вы работаете?
    vacs_str_title = str(vacs[i]['vactitle'])
    if (('qa' in vacs_str_title.lower()) or ('тестировщ' in vacs_str_title.lower()) or \
        ('q&a' in vacs_str_title.lower())) and \
            ('auto' not in vacs_str_title.lower() and 'атф' not in vacs_str_title.lower() and \
             'авто' not in vacs_str_title.lower() and 'нагруз' not in vacs_str_title.lower() and \
             'НТ' not in vacs_str_title):
        count_work_vac += 1
    # Сколько вакансий для аналатика данных?
    if ('data analyst' in vacs_str_title.lower()) or ('DA' in vacs_str_title) or ('аналитик данных' in
                                                                                  vacs_str_title.lower()):
        count_da_vac += 1
        # Сколько вакансий для аналитика данных с использованием Python?
        if ('python' in (vacs[i]['vacdescription']).lower()) or ('питон' in (vacs[i]['vacdescription']).lower()):
            count_da_vac_py += 1
            # Сколько вакансий, которые вам нравятся?
            if (('sql' in (vacs[i]['vacdescription']).lower())
                    and ('ML' in vacs[i]['vacdescription'])):
                vac_like += 1
                vac_date = datetime.datetime.strptime(vacs[1]['vacdate'], '%Y-%m-%d')
                delta_days = (datetime.datetime.today() - vac_date).days
                # Насколько свежие эти вакансии?
                if delta_days <= 30:
                    count_vac_fresh_month += 1
                elif 30 < delta_days <= 30 * 3:
                    count_vac_fresh_kvartal += 1
                elif 30 * 3 < delta_days < 30 * 6:
                    count_vac_fresh_halfyear += 1
                else:
                    count_vac_fresh_older_halfyear += 1

print('Сколько вакансий, которые вам нравятся? - ' + str(vac_like) + '. Из них')
print('\t вакансий младше месяца - ' + str(count_vac_fresh_month))
print('\t вакансий младше квартала - ' + str(count_vac_fresh_kvartal))
print('\t вакансий младше полугода - ' + str(count_vac_fresh_halfyear))
print('\t вакансий старше полугода - ' + str(count_vac_fresh_older_halfyear))
print('Сколько вакансий с позициями на которых вы работаете? - ' + str(count_work_vac))
print('Сколько вакансий для аналатика данных? - ' + str(count_da_vac))
print('Сколько вакансий для аналитика данных с использованием Python? - ' + str(count_da_vac_py))
