import csv
import os


class CarBase:
    def __new__(cls, *args):
        valid_photo = ['.jpg', '.jpeg', '.png', '.gif']
        photo = any(os.path.splitext(name)[-1] in valid_photo for name in args)
        if photo:
            return super().__new__(cls)
        else:
            raise ValueError

    def __init__(self, brand, photo_file_name, carrying):
        photo = CarBase.valid_photo(photo_file_name)
        if not(photo and brand and carrying != ''):
            raise ValueError
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    @staticmethod
    def valid_photo(photo):
        return os.path.splitext(photo)[-1] in ['.jpg', '.jpeg', '.png', '.gif']

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]

    @classmethod
    def from_string(cls, car_type, brand, passenger_seats_count, photo_file_name, body_whl, carrying, extra, *args):

        if car_type == 'car':
            return Car(brand, photo_file_name, carrying, passenger_seats_count)
        if car_type == 'truck':
            return Truck(brand, photo_file_name, carrying, body_whl)
        if car_type == 'spec_machine':
            return SpecMachine(brand, photo_file_name, carrying, extra)
        else:
            raise ValueError


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count, *args):
        if passenger_seats_count == '':
            raise ValueError
        else:
            super().__init__(brand, photo_file_name, carrying)
            self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl='0x0x0'):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = '0x0x0' if body_whl == '' else body_whl
        try:
            self.body_length, self.body_width, self.body_height = map(float, self.body_whl.split('x'))
        except (ValueError, ):
            self.body_length, self.body_width, self.body_height = 0.0, 0.0, 0.0

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        if extra == '':
            raise ValueError
        else:
            super().__init__(brand, photo_file_name, carrying)
            self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename, encoding='utf-8') as csv_fd:
        reader = csv.reader(csv_fd, delimiter=',')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if row and row[0]:
                try:
                    car_list.append(CarBase.from_string(*row))
                except (ValueError, TypeError):
                    continue

    return car_list


def main():
    cars = get_car_list('cars.csv')
    print(len(cars))
    for car in cars:
        print(type(car))
    print('--')
    print(cars[0].passenger_seats_count)
    print(cars[1].get_body_volume())


if __name__ == '__main__':
    main()
