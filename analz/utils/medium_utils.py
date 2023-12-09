import PIL
import internetdownloadmanager as idm
import charade
import os


class MediumUtils:


    @staticmethod
    def PDF2Images():
        # PDF to Images
        import fitz
        pdf = 'sample_pdf.pdf'
        doc = fitz.open(pdf)
        for page in doc:
            pix = page.getPixmap(alpha=False)
            pix.writePNG('page-%i.png' % page.number)
    
    @staticmethod
    def do_pillow(ifn):
        dir = f"e:/Pictures"
        afn = 'C:\\Users\]johnc\\OneDrive\\Pictures\\thetree.jpg'
        img_fn = os.path.join(dir, ifn)

        # Croping 
        im = PIL.Image.open(img_fn)
        im = im.crop((34, 23, 100, 100))
        # Resizing
        im = PIL.Image.open(img_fn)
        im = im.resize((50, 50))
        # Flipping
        im = PIL.Image.open(img_fn)
        im = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        # Rotating
        im = PIL.Image.open(img_fn)
        im = im.rotate(360)
        # Compressing
        im = PIL.Image.open(img_fn)
        im.save(img_fn, optimize=True, quality=90)
        # Bluring
        im = PIL.Image.open(img_fn)
        im = im.filter(PIL.ImageFilter.BLUR)
        # Sharpening
        im = PIL.Image.open(img_fn)
        im = im.filter(PIL.ImageFilter.SHARPEN)
        # Set Brightness
        im = PIL.Image.open(img_fn)
        im = PIL.ImageEnhance.Brightness(im)
        im = im.enhance(1.5)
        # Set Contrast
        im = PIL.Image.open(img_fn)
        im = PIL.ImageEnhance.Contrast(im)
        im = im.enhance(1.5)
        # Adding Filters
        im = PIL.Image.open(img_fn)
        im = PIL.ImageOps.grayscale(im)
        im = PIL.ImageOps.invert(im)
        im = PIL.ImageOps.posterize(im, 4)
        # Saving
        im.save(img_fn)



        # Python Downloader
        # pip install internetdownloadmanager

    @staticmethod
    def Downloader(url, output):
        pydownloader = idm.Downloader(worker=20,
                                      part_size=1024 * 1024 * 10,
                                      resumable=True, )

        pydownloader.download(url, output)
    #   Usage:
    # Downloader("Link url", "image.jpg")
    # Downloader("Link url", "video.mp4")


    # world news api
    @staticmethod
    def world_news():
        # World News Fetcher
        # pip install requests
        import requests
        ApiKey = "4710850799214474b3bc727039cfe2dc"
        url = f"https://api.worldnewsapi.com/search-news?text=hurricane&api-key={ApiKey}"
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        print("News: ", response.json())


# class FtFy:
#     import ftfy
#
#     print(ftfy.fix_text('Correct the sentence using â€œftfyâ€\x9d.'))
#     print(ftfy.fix_text('âœ” No problems with text'))
#     print(ftfy.fix_text('Ã perturber la rÃ©flexion'))
#
#
# class PendulumUtil:
#     # import library
#     import pendulum
#
#     dt = pendulum.datetime(2023, 1, 31)
#     print(dt)
#
#     # local() creates datetime instance with local timezone
#
#     local = pendulum.local(2023, 1, 31)
#     print("Local Time:", local)
#     print("Local Time Zone:", local.timezone.name)
#
#     # Printing UTC time
#     utc = pendulum.now('UTC')
#     print("Current UTC time:", utc)
#
#     # Converting UTC timezone into Europe/Paris time
#
#     europe = utc.in_timezone('Europe/Paris')
#     print("Current time in Paris:", europe)

class TimerDecorator:
    @staticmethod
    def timer(func):
        import time
        def wrapper(*args, **kwargs):
            # start the timer
            start_time = time.time()
            # call the decorated function
            result = func(*args, **kwargs)
            # remeasure the time
            end_time = time.time()
            # compute the elapsed time and print it
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")
            # return the result of the decorated function execution
            return result

        # return reference to the wrapper function
        return wrapper

    @staticmethod
    @timer
    def train_model():
        import time
        print("Starting the model training function...")
        # simulate a function execution by pausing the program for 5 seconds
        time.sleep(5)
        print("Model training completed!")

    # train_model()

    #  simple decorator with args
    @staticmethod
    def debug(func):  # decorator
        def wrapper(*args, **kwargs):
            # print the fucntion name and arguments
            print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
            # call the function
            result = func(*args, **kwargs)
            # print the results
            print(f"{func.__name__} returned: {result}")
            return result

        return wrapper

    @staticmethod
    @debug
    def add_numbers(x, y):
        return x + y

    # add_numbers(7, y=5, )
    #        Output: Calling add_numbers with args: (7) kwargs: {'y': 5} \n add_numbers returned: 12

    # Exception handler decorator

    @staticmethod
    def exception_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Handle the exception
                print(f"An exception occurred: {str(e)}")
                # Optionally, perform additional error handling or logging
                # Reraise the exception if needed

        return wrapper


    @staticmethod
    @exception_handler
    def divide(x, y):
        result = x / y
        return result

    # divide(10, 0)  # Output: An exception occurred: division by zero

    # validation decorator
    @staticmethod
    def validate_input(*validations):
        def decorator(func):
            def wrapper(*args, **kwargs):
                for i, val in enumerate(args):
                    if i < len(validations):
                        if not validations[i](val):
                            raise ValueError(f"Invalid argument: {val}")
                for key, val in kwargs.items():
                    if key in validations[len(args):]:
                        if not validations[len(args):][key](val):
                            raise ValueError(f"Invalid argument: {key}={val}")
                return func(*args, **kwargs)

            return wrapper

        return decorator


    @staticmethod
    @validate_input(lambda x: x > 0, lambda y: isinstance(y, str))
    def divide_and_print(x, message):
        print(message)
        return 1 / x

    # divide_and_print(5, "Hello!")  # Output: Hello! 1.0

    # retry decorator
    @staticmethod
    def retry(max_attempts, delay=1):
        import time
        def decorator(func):
            def wrapper(*args, **kwargs):
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        print(f"Attempt {attempts} failed: {e}")
                        time.sleep(delay)
                print(f"Function failed after {max_attempts} attempts")

            return wrapper
        return decorator


    @staticmethod
    @retry(max_attempts=3, delay=2)
    def fetch_data(url):
        print("Fetching the data..")
        # raise timeout error to simulate a server not responding..
        raise TimeoutError("Server is not responding.")

    # fetch_data("https://example.com/data")  # Retries 3 times with a 2-second delay between attempts



class Encodings:

    def detect(s):

        try:
            # check it in the charade list
            if isinstance(s, str):
                return charade.detect(s.encode())
                # detecting the string
            else:
                return charade.detect(s)

        # in case of error
        # encode with 'utf -8' encoding
        except UnicodeDecodeError as inst:
            print(inst)
            return charade.detect(s.encode('utf-8'))

    def convert_to_utf8(s):
        encoding = 'utf-8'

        # if in the charade instance
        if isinstance(s, str):
            s = s.encode()

        # retrieving the encoding information
        # from the detect() output
        encode = Encodings.detect(s)['encoding']

        if encode == 'utf-8':
            return s
        else:
            return s.encode(encoding = 'UTF-8', errors = 'strict')

class MapFuncs:
    def __init__(self):
        numbers = [1, 2, 3, 4, 5]
        self.squared_numbers = map(self.square, numbers)
        print(f"squares: {list(self.squared_numbers)}")
        results = map(lambda x: (self.square(x), self.cube(x)), numbers)
        results = list(results)
        print(f"squares and cubes: {results}")
        numbers2 = [10, 20, 30, 40, 50]
        added_numbers = map(self.add, numbers, numbers2)
        added_numbers = list(added_numbers)
        print(f"map to multiple iterables: numbers 1({numbers} and numbers 2: {numbers2}\n")
        print('added_numbers', added_numbers)
        even_squared = map(self.square, filter(lambda x: x % 2 == 0, numbers))
        even_squared = list(even_squared)
        print(f"even squared, using filter(): {even_squared}")

    def square(self, x):
        return x ** 2

    def add(self, x, y):
        return x + y

    def cube(self, x):
        return x ** 3

    # Output: [(1, 1), (4, 8), (9, 27), (16, 64), (25, 125)]


class PgeCode:
    import pgeocode
    # Checking for country "India"

    nomi = pgeocode.Nominatim('In')

    # Getting geo information by passing the postcodes

    nomi.query_postal_code(["620018", "620017", "620012"])


class Dictionairies:
    d = {'a': 4, 'b': 2, 'c': 3, 'd': 1}

    @staticmethod
    def sort_dictionary_by_value(d: dict):
        return sorted(d.items(), key=lambda x: x[1])

    @staticmethod
    def pretty_print_sort(d: dict):
        import json

class FactoryPattern:
    class Dog:
        def __init__(self):
            self.name = "dog"

    class Cat:
        def __init__(self):
            self.name = "cat"

    class AnimalFactory:
        def create_animal(self, animal_type):
            if animal_type == "dog":
                return FactoryPattern.Dog()
            elif animal_type == "cat":
                return FactoryPattern.Cat()
            else:
                return None

        # factory = AnimalFactory()
        # animal = factory.create_animal("dog")
        # print(animal.name)


class Singleton:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    # a = Singleton()
    # b = Singleton()
    #
    #
    # print(a is b)
# Output?True


class AdapterPattern:
    class Target:
        def request(self):
            pass

    class Adaptee:
        def specific_request(self):
            pass

    class Adapter(Target):
        def __init__(self, adaptee):
            self.adaptee = adaptee

        def request(self):
            self.adaptee.specific_request()

            # adaptee = AdapterPattern.Adaptee()
            # adapter = AdapterPattern.Adapter(adaptee)
            # adapter.request()


class DecoratorPattern:
    def logging(func):
        def wrapper(*args, **kwargs):
            print("call function:", func.__name__)
            return func(*args, **kwargs)

        return wrapper

        # @logging
        # def foo():
        #     print("hello world")
        # foo()
        # Output?call function: foo hello world


class ObserverPattern:
    class Subject:
        def __init__(self):
            self.observers = []

        def attach(self, observer):
            self.observers.append(observer)

        def detach(self, observer):
            self.observers.remove(observer)

        def notify(self):
            for observer in self.observers:
                observer.update(self)

    class Observer:
        def update(self, subject):
            pass

    class ConcreteSubject(Subject):
        def __init__(self):
            super().__init__()
            self.state = 0

        def get_state(self):
            return self.state

        def set_state(self, state):
            self.state = state
            self.notify()

    class ConcreteObserver(Observer):
        def update(self, subject):
            print("state changed to:", subject.get_state())

    # subject = ConcreteSubject()
    # observer = ConcreteObserver()
    # subject.attach(observer)
    # subject.set_state(1)

    # Output?state changed to: 1


