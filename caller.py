import composer
import xlrd

def read_excel():
    wb = xlrd.open_workbook('data.xlsx')
    sheet = wb.sheet_by_index(0)

    fields = {}
    field_names = []
    for i in range(sheet.ncols):
        field_names.append(sheet.cell_value(0,i))
    for i in range(sheet.nrows - 1):
        count = i + 1
        for j in range(sheet.ncols):
            if i not in fields.keys():
                fields[i] = {
                    field_names[j]: sheet.cell_value(count, j)
                }
            else:
                fields[i].update({field_names[j]: sheet.cell_value(count, j)})

    return fields

fin_fields = read_excel()

for key, value in fin_fields.items():
    composer.main(value)
