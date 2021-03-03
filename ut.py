import datetime

#1. **************************************************************************************
txt = open(r'..\scratches\forgalom.txt', 'r')

for i in range(2):
    number_of_cars = (int(txt.readline()) if i == 1 else 0) # Storing the first line as the number of the cars

line = txt.readline()
data = () # For containing the txt from the 2. line

while line != '':
    data += (line.strip().split(" "),) # Writing every line in a tuple as a list
    line = txt.readline()

txt.close()

#2. **************************************************************************************
car_number_input = input("2. feladat Adja meg a jármű sorszámát: ")

try:
    car_number_input = int(car_number_input)
    if int(car_number_input) <= 0:
        raise SystemExit("A szám nem lehet negatív vagy nulla!")
    if car_number_input > number_of_cars:
        raise SystemExit("Kevesebb volt a megfigyelt autók száma!")
except ValueError:
    raise SystemExit("Pozitív egész számot adjon meg!") # Checking special characters

print(f"A(z) {car_number_input}. belépő {'Alsó' if data[car_number_input-1][4] == 'F' else 'Felső'} irányába haladt.")

#3. **************************************************************************************


for j in range(2):
    last_two_cars_felso = [data[i][:4:] for i in range(int(number_of_cars))[::-1] if data[i][-1]=="A"][:2:] # Last two elements in "data" ending with "F" (without the "F")

hour = int(last_two_cars_felso[0][0])*60 - int(last_two_cars_felso[1][0])*60
minute = int(last_two_cars_felso[0][1])*60 - int(last_two_cars_felso[1][1])*60
secs= int(last_two_cars_felso[0][2]) - int(last_two_cars_felso[1][2])
diff_last_cars = hour+minute+secs

print(f'A két jármű {diff_last_cars} mp különbséggel érte el az útszakasz kezdetét.')

#4. **************************************************************************************

hours_dirs = []

for i in range(24):
    felso = 0
    also = 0
    for j in range(number_of_cars):
        if i == int(data[j][0]):
            if data[j][-1] == "F":
                felso += 1
            else:
                also += 1

    hours_dirs.append([i, also, felso])

    if hours_dirs[i][1] != 0 and hours_dirs[i][2] != 0:
        print(hours_dirs[i][0], hours_dirs[i][1], hours_dirs[i][2])

#5. **************************************************************************************

data_editable = list(data)
temp_list = []
result_list = []
current_max = 0
for_pop = 0

data_editable.sort(key=lambda x: x[3]) # No idea what this does, and why this is not enough in itself

for i in range(number_of_cars):
    current_max = data_editable[i][3] if int(data_editable[i][3]) > int(current_max) else current_max # Findig the max value for min searching

for i in range(10):

    for j in range(number_of_cars-i):

        if int(data_editable[j][3]) <= int(current_max): # Searching for min, and popping it from a copy of "data"
            del temp_list[:]
            current_max = data_editable[j][3]
            temp_list.append(data_editable[j])
            for_pop = j

    result_list.append(data_editable.pop(for_pop))

for i in reversed(range(10)):
    print(f"Belépés: {result_list[i][0]} {result_list[i][1]} {result_list[i][2]} {'Alsó' if result_list[i][4] == 'F' else 'Felső'} felől érkezett "
          f"{round(int(result_list[i][3])*60/1000,1)} m/s ")

#6. **************************************************************************************

txt_w = open(r'..\scratches\also.txt', 'w')

last_date = datetime.datetime(100, 1, 1, 0,0,0)

for i in range(number_of_cars):
    if data[i][4] == "F":
        og_date = datetime.datetime(100, 1, 1, int(data[i][0]), int(data[i][1]), int(data[i][2]))
        exit_date = og_date + datetime.timedelta(0, int(data[i][3]))
        if last_date > exit_date:
            txt_w.writelines(f'{str(last_date.time()).split(":")[0]} {str(last_date.time()).split(":")[1]} {str(last_date.time()).split(":")[2]}\n')

        else:
            txt_w.writelines(f'{str(exit_date.time()).split(":")[0]} {str(exit_date.time()).split(":")[1]} {str(exit_date.time()).split(":")[2]}\n')
        last_date = og_date + datetime.timedelta(0, int(data[i][3]))

txt_w.close()