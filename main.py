import sys
import pathlib

def input_file():
    reservations_ = {}

    try:
        file_path = sys.argv[1].strip()
        with open(file_path, 'r') as file:
            txt_lines = file.readlines()
    except:
        print("Something went wrong, just paste file location below")
        while 1:
            try:
                file_path = input("Enter Input.txt file path here please: ").strip()
                # if file_path == "":
                #     file_path = r"Z:\Users\carlos144green\Desktop\Input.txt"
                with open(file_path, 'r') as file:
                    txt_lines = file.readlines()
            except:
                print("File path didn't work, try again.\n")
            else:
                break

    for group in txt_lines:
        group = group.strip().split(" ")
        if group[0] in reservations_:
            print("REBOOKING FOUND, overwriting reservation ID for:", group[0], "\n")
        reservations_[group[0]] = int(group[1].strip("\n"))
    return reservations_


class Theater:
    def __init__(self, row_count, seat_per_row):
        self.row_count = row_count
        self.seat_per_row = seat_per_row
        self.row = [0] * seat_per_row
        self.chart = {}
        for i in range(self.row_count):
            self.chart[i] = [0] * seat_per_row

        self.availability = [seat_per_row] * row_count
        self.row_index = row_count - 1
        self.buffer_size = 3

    def show(self):
        print("                    [[     SCREEN     ]]                    ")
        for i in self.chart:
            print(self.chart[i])

    def assign_seats(self, reservations_):
        if sum(reservations_.values()) < 70 and len(reservations_) < 20:
            skip = 2
        else:
            skip = 1
        with open('output.txt', 'w') as file:

            for client_id, group_size in reservations_.items():
                file.write(client_id + " ")
                row_index = self.row_index
                while row_index >= skip and self.availability[row_index] < group_size:
                    row_index -= skip
                if self.availability[row_index] < group_size:
                    print("no more space for this size")
                    file.write('No seats available for this size \n')
                    continue
                for i in range(group_size):
                    self.chart[row_index][self.seat_per_row - self.availability[row_index]] = 1
                    file.write(chr(65 + row_index) + str(self.seat_per_row - self.availability[row_index]))
                    if i == group_size-1:
                        file.write('\n')
                    else:
                        file.write(',')
                    self.availability[row_index] -= 1

                for i in range(self.buffer_size):
                    if self.availability[row_index] > 0:
                        self.chart[row_index][self.seat_per_row - self.availability[row_index]] = 8
                        self.availability[row_index] -= 1

        print("Final availability: ", self.availability)

if __name__ == '__main__':
    reservations = input_file()
    theaterTest = Theater(10, 20)

    theaterTest.assign_seats(reservations)
    Theater.show(theaterTest)
    print("Output file located here: ", pathlib.Path(__file__).parent.resolve())
