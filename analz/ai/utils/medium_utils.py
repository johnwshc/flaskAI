import PIL
# import internetdownloadmanager as idm
import charade
import requests
import threading
import multiprocessing
from PIL import Image, ImageFilter
import os
from config import Config
from cachetools import cached, TTLCache

class MapReduceUtils:

    """
    Filter returns the value only if the boolean function returns True.
Map function applies a function to all the items regardless of the
return value of the function and creates a new iterable object with the result.

    """

    @staticmethod
    def sample_map():
        myfriends = ['Cat', 'Dog', 'Parrot', 'Ant', 'Bird']
        uppercase = list(map(str.upper, myfriends))
        print(uppercase)

    @staticmethod
    def simple_filter():
        # With Filter
        age_list = [15, 18, 45, 90, 5]

        def eligibility_vote(age):
            return age >= 18

        print(list(filter(eligibility_vote, age_list)))



# class MediumUtils:
    
#     @staticmethod
#     def do_pillow(ifn):
#         dir = f"e:/Pictures"
#         afn = 'C:\\Users\]johnc\\OneDrive\\Pictures\\thetree.jpg'
#         img_fn = os.path.join(dir, ifn)
#
#         # Croping
#         im = PIL.Image.open(img_fn)
#         im = im.crop((34, 23, 100, 100))
#         # Resizing
#         im = PIL.Image.open(img_fn)
#         im = im.resize((50, 50))
#         # Flipping
#         im = PIL.Image.open(img_fn)
#         im = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
#         # Rotating
#         im = PIL.Image.open(img_fn)
#         im = im.rotate(360)
#         # Compressing
#         im = PIL.Image.open(img_fn)
#         im.save(img_fn, optimize=True, quality=90)
#         # Bluring
#         im = PIL.Image.open(img_fn)
#         im = im.filter(PIL.ImageFilter.BLUR)
#         # Sharpening
#         im = PIL.Image.open(img_fn)
#         im = im.filter(PIL.ImageFilter.SHARPEN)
#         # Set Brightness
#         im = PIL.Image.open(img_fn)
#         im = PIL.ImageEnhance.Brightness(im)
#         im = im.enhance(1.5)
#         # Set Contrast
#         im = PIL.Image.open(img_fn)
#         im = PIL.ImageEnhance.Contrast(im)
#         im = im.enhance(1.5)
#         # Adding Filters
#         im = PIL.Image.open(img_fn)
#         im = PIL.ImageOps.grayscale(im)
#         im = PIL.ImageOps.invert(im)
#         im = PIL.ImageOps.posterize(im, 4)
#         # Saving
#         im.save(img_fn)
#
#
#     # convert scientific notation to readable float
#     @staticmethod
#     def scinot_2_dec(sci: float):
#         return "{:.9f}".format(sci)
#
#
#         # Python Downloader
#         # pip install internetdownloadmanager
#
#     # @staticmethod
#     # def Downloader(url, output):
#     #     pydownloader = idm.Downloader(worker=20,
#     #                                   part_size=1024 * 1024 * 10,
#     #                                   resumable=True, )
#     #
#     #     pydownloader.download(url, output)
#     #   Usage:
#     # Downloader("Link url", "image.jpg")
#     # Downloader("Link url", "video.mp4")
#
#
#     # world news api
#     @staticmethod
#     def world_news():
#         # World News Fetcher
#         # pip install requests
#         import requests
#         ApiKey = "4710850799214474b3bc727039cfe2dc"
#         url = f"https://api.worldnewsapi.com/search-news?text=hurricane&api-key={ApiKey}"
#         headers = {
#             'Accept': 'application/json'
#         }
#         response = requests.get(url, headers=headers)
#         print("News: ", response.json())
#
#
# class FtFy:
#
#     """Wiktionary, the free dictionary"""
#     import ftfy
#
#     # print(ftfy.fix_text('Correct the sentence using â€œftfyâ€\x9d.'))
#     # print(ftfy.fix_text('âœ” No problems with text'))
#     # print(ftfy.fix_text('Ã perturber la rÃ©flexion'))
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

class PgeCode:
    import pgeocode
    # Checking for country "India"

    nomi = pgeocode.Nominatim('In')

    # Getting geo information by passing the postcodes

    nomi.query_postal_code(["620018", "620017", "620012"])

#
# class Mthreads:
#     @staticmethod
#     def download_url(url):
#         response = requests.get(url)
#         print(f"Downloaded {url}")
#
#     urls = ["https://www.example.com", "https://www.google.com", "https://www.github.com"]
#
#     # Create and start a thread for each URL
#     threads = []
#     for url in urls:
#         thread = threading.Thread(target=download_url, args=(url,))
#         threads.append(thread)
#         thread.start()
#
#     # Wait for all threads to finish
#     for thread in threads:
#         thread.join()
#     # Rather than downloading the urls sequentially, the requests are sent similutatncy
#     print("All downloads complete.")
#
#
# class MProcess:
#
#     def __init__(self):
#         self.test_image_path = f"{Config.basedir}\\images\carol on mantle.jpg"
#         self.test_output_path = f"{Config.basedir}\\output_images"
#         self.input_folder = f"{Config.basedir}\\images"
#         self.output_folder = f"{Config.basedir}\\output_images"
#         os.makedirs(self.output_folder, exist_ok=True)
#
#         self.image_paths = [os.path.join(self.input_folder, filename) for filename in os.listdir(self.input_folder)]
#
#     # Some function to process images and save it in independet location
#
#     def process_image(self):
#         image = Image.open(self.test_image_path)
#         blurred_image = image.filter(ImageFilter.GaussianBlur(5))
#         blurred_image.save(self.test_output_path)
#         print(f"Processed: {self.test_image_path} -> {self.test_output_path}")
#
#
#     def multi_process_images(self):
#         # Create and start a process for each image
#         processes = []
#         for image_path in self.image_paths:
#             output_path = os.path.join(self.output_folder, os.path.basename(self.test_image_path))
#             process = multiprocessing.Process(target=self.process_image, args=(image_path, output_path))
#             processes.append(process)
#             process.start()
#         # Wait for all processes to finish
#         for process in processes:
#             process.join()
#
#         print("Image processing complete.")

#
# class Caches:
#     # Create a cache with a time-to-live (TTL) of 300 seconds (5 minutes)
#     weather_cache = TTLCache(maxsize=100, ttl=300)
#
#     @staticmethod
#     @cached(weather_cache)
#     def get_weather(city):
#         print(f"Fetching weather data for {city}...")
#         # This is a dummy API and won't work if you run the code
#         response = requests.get(f"https://api.example.com/weather?city={city}")
#         return response.json()
#
#         # # Fetch weather for a city (API call will be made)
#         # city1_weather = get_weather("New York")
#
#         # Fetch weather for the same city again (cached result will be used)
#         # city1_weather_cached = get_weather("New York")
#
#         # # Fetch weather for a different city (API call will be made)
#         # city2_weather = get_weather("Los Angeles")
#
#         # print("City 1 Weather (API call):", city1_weather)
#         # print("City 1 Weather (Cached):", city1_weather_cached)
#         # print("City 2 Weather (API call):", city2_weather)
#

class Generator:
    @staticmethod
    def process_item(itm):
        print(itm)
    def large_dataset_generator(data):
        for item in data:
            yield Generator.process_item(item)

    # Usage
    # data = [...]  # Large dataset
    # for processed_item in large_dataset_generator(data):
    #     # Process each item one at a time
    #     print(processed_item)


class Funcs:
    @staticmethod
    def shout(name):
        return f'Hey! My name is {name}.'

    @staticmethod
    def break_sentence(sentence: str):
        return sentence.split(' ')

    @staticmethod
    def practice(name):

        # we will use break_sentence defined above

        # assign function to another variable
        another_breaker = Funcs.break_sentence

        another_breaker(Funcs.shout('John'))
        # ['Hey!', 'My', 'name', 'is', 'John.']

        # Woah! Yes, this is a valid way to define function
        name_decorator = lambda x: '-'.join(list(name))

        name_decorator('John')
        # 'J-o-h-n'
    @staticmethod
    def dash_decorator(name):
        return '-'.join(list(name))

    @staticmethod
    def no_decorator(name):
        return name

    @staticmethod
    def shout2(name, decorator=no_decorator):
        decorated_name = decorator(name)
        return f'Hey! My name is {decorated_name}'

class Dictionaries:

    @staticmethod
    def key_exists(key="phone"):
        d = {"name": "Tony", "age": 100}

        if key in d:
            print("Key exists")
        else:
            print("Not exists")

    @staticmethod
    def make_dicts():
        # Create a dictionary from another dictionary
        original_dict = {'a': 1, 'b': 2, 'c': 3}
        new_dict = {key: value for key, value in original_dict.items() if value % 2 == 0}
        print(new_dict)
        # Output: {'b': 2}

        # Create a dictionary from a list of key-value pairs
        pairs = [('a', 1), ('b', 2), ('c', 3)]
        new_dict = {key: value for key, value in pairs if value % 2 == 0}
        print(new_dict)
        # Output: {'b': 2}

#         data cleaning
        # Extract specific fields from a list of dictionaries
        data = [{'name': 'John', 'age': 35, 'city': 'New York'},
                {'name': 'Jane', 'age': 28, 'city': 'London'},
                {'name': 'Jim', 'age': 42, 'city': 'Paris'}]

        names = {d['name']: d['age'] for d in data}
        print(names)
        # Output: {'John': 35, 'Jane': 28, 'Jim': 42}

        # Convert a list of strings into a dictionary mapping each string to its length
        words = ['dog', 'cat', 'elephant', 'giraffe']
        lengths = {word: len(word) for word in words}
        print(lengths)
        # Output: {'dog': 3, 'cat': 3, 'elephant': 8, 'giraffe': 7}

        # Group a list of numbers based on whether they are even or odd
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        grouped = {'even': [n for n in numbers if n % 2 == 0],
                   'odd': [n for n in numbers if n % 2 != 0]}
        print(grouped)
        # Output: {'even': [2, 4, 6, 8, 10], 'odd': [1, 3, 5, 7, 9]}

        # Group a list of strings based on their first letter
        words = ['apple', 'banana', 'cherry', 'date', 'elderberry']
        grouped = {letter: [word for word in words if word[0] == letter]
                   for letter in set(word[0] for word in words)}
        print(grouped)
        # Output: {'a': ['apple'], 'b': ['banana'], 'c': ['cherry'], 'd': ['date'], 'e': ['elderberry']}

        # Count the frequency of words in a text
        text = 'the quick brown fox jumps over the lazy dog'
        words = text.split()
        frequency = {word: words.count(word) for word in set(words)}
        print(frequency)
        # Output: {'the': 2, 'quick': 1, 'brown': 1, 'fox': 1, 'jumps': 1,
        # 'over': 1, 'lazy': 1, 'dog': 1}

        # Count the number of times each character appears in a string
        string = 'hello world'
        frequency = {char: string.count(char) for char in set(string)}
        print(frequency)
        # Output: {'h': 1, 'e': 1, 'l': 3, 'o': 2, 'w': 1, 'r': 1, 'd': 1}


class REUtils:
    @staticmethod
    def replaceNonAlphaNumericChars(s: str):
        import re

        return re.sub('[^0-9a-zA-Z]+', '_', s)


    @staticmethod
    def get_sentences(txt):
        import re
        tpat1 = r'([A-Z][^\.!?]*[\.!?])'
        pat = re.compile(tpat1, re.M)
        sentences = pat.findall(txt)
        return sentences

    @staticmethod
    def compute_chunks(sentences, chunk_size=700 ):
        wl = lambda x: len(x.split(' '))
        sensums = []
        chunks = []
        for s in sentences:
            nw = wl(s)
            sensums.append((nw,s))

            chunk_sum = sum([x[0] for x in sensums])
            if chunk_sum >= chunk_size:
                ctxt = [' '.join(s[1]) for s in sensums]

                chunks.append(ctxt)
                sensums.clear()

        return chunks


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(repr(current))
            current = current.next
        return "->".join(nodes)

    @staticmethod
    def traverse(linked_list):
        current = linked_list.head
        while current:
            print(current.data)
            current = current.next

    @staticmethod
    def reverse_linked_list(head):
        previous = None
        current = head
        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        return previous

    def insert_after_value(self, data_after, data_to_insert):
        if self.head is None:
            return

        current = self.head
        while current:
            if current.data == data_after:
                new_node = Node(data_to_insert)
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next

        self.append(data_to_insert)

    def delete_node(self, data):
        current = self.head

        if current is None or current.data == data:
            self.head = current.next if current else None
            return

        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next






