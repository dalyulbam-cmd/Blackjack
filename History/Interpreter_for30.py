import csv

new_data = []
note_name ="All_in_one.csv"

with open(note_name,'wt',encoding ='utf-8', newline ="") as statistic:
    writer = csv.writer(statistic)
    for i in range(100):
        file_name = "strategy_" + str(i) + ".csv"
        line_number = 0
        account = 0
        rate = 0 
        with open(file_name,'rt', encoding = 'utf-8', newline = "") as experiment:
            reader = csv.reader(experiment)
            for row in reader:
                line_number += 1 
                if not (line_number == 31 or line_number == 33) :
                    continue
                elif line_number == 31:
                    account = row[2]
                    continue
                else :
                    rate = row[0]
        experiment.close()
        new_data = [account,rate]
        writer.writerow(new_data)
statistic.close()
                                
