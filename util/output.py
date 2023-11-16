import xlsxwriter
import json


def makexlsx(name, data, title):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()

    merge_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet.write_row('A1', title, merge_format)

    row = 1
    col = 0

    for i in data:
        datalen = len(data[i])

        if datalen > 1:
            worksheet.merge_range(row, 0, row + datalen - 1, 0, i, merge_format)
        else:
            worksheet.write(row, 0, i, merge_format)

        for j in range(datalen):
            for k in range(len(data[i][j])):
                worksheet.write(row + j, k + 1, data[i][j][k], merge_format)

        row += datalen

    workbook.close()


if __name__ == '__main__':
    pass
