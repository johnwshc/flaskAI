import requests
from dataclasses import dataclass
from enum import Enum, unique
from analz.utils.podbeanapi import PBPoetry as PBP, PBLabor as PBL,PBRecovery as PBR, PBWNL as PBW, PBSports as PBS
from pprint import pprint

class WebTests:

    @staticmethod
    def wprest_test():
        url = "http://localhost:5000/manage/wprest"
        data = {'title': 'TestTitle', 'xpwd': 'vil3nin'}
        r = requests.get(url=url, params=data)
        print(r)
        return

class PB_PostsTests:
    @staticmethod
    def test_poetry_post():
        ptst = PBP.test()
        return PBP(props=ptst)

    @staticmethod
    def web_test_poetry_post():
        from pathlib import Path
        from bs4 import BeautifulSoup

        url = f"http://localhost:5000/manage/pb_poetry_publish"

        # r = requests.get(url)
        # soup = BeautifulSoup(r.text, 'lxml')
        # csrf_token = soup.find('input', attrs={'name': 'csrf_token'})['value']
        data = PBP.test()
        fn = data.get('filename', None)

        pr = requests.post(url, data=data)
        return data, pr

    @staticmethod
    def test_labor_post():

        ptst = PBL.test()
        pbl = PBL(props=ptst)
        return pbl

    @staticmethod
    def web_test_labor_post():
        url = f"http://localhost:5000/manage/pb_labor_publish"
        data = PBL.test()
        pr = requests.post(url, data=data)


        return data, pr

    @staticmethod
    def test_recovery_post():
        ptst =  PBR.test()
        pbr = PBR(props=ptst)
        return pbr

    def web_test_recovery_post():

        url = f"http://localhost:5000/manage/pb_recovery_publish"
        data = PBR.test()
        pr = requests.post(url, data=data)

        return data, pr

    @staticmethod
    def test_wnl_post():
        ptst = PBW.test()
        pbw = PBW(props=ptst)
        return pbw

    @staticmethod
    def web_test_wnl_post():
        url = f"http://localhost:5000/manage/pb_wnl_publish"
        data = PBW.test()
        pr = requests.post(url, data=data)

        return data, pr


    @staticmethod
    def test_sports_post():
        ptst = PBS.test()
        pbs = PBS(props=ptst)
        return pbs

    @staticmethod
    def web_test_sports_post():
        url = f"http://localhost:5000/manage/pb_sports_publish"
        data = PBS.test()
        pr = requests.post(url, data=data)

        return data, pr

    @staticmethod
    def txt_len(tx: str = None):

        txt = """I have walked through many lives, some of them my own,
        and I am not who I was,
        though some principle of being
        abides, from which I struggle
        not to stray.
        When I look behind,
        as I am compelled to look
        before I can gather strength
        to proceed on my journey,
        I see the milestones dwindling
        toward the horizon
        and the slow fires trailing
        from the abandoned camp-sites,
        over which scavenger angels
        wheel on heavy wings.
        Oh, I have made myself a tribe
        out of my true affections,
        and my tribe is scattered!
        How shall the heart be reconciled
        to its feast of losses?
        In a rising wind
        the manic dust of my friends,
        those who fell along the way,
        bitterly stings my face.
        Yet I turn, I turn,
        exulting somewhat,
        with my will intact to go
        wherever I need to go,
        and every stone on the road
        precious to me.
        In my darkest night,
        when the moon was covered
        and I roamed through wreckage,
        a nimbus-clouded voice
        directed me:
        'Live in the layers,
        not on the litter.'
        Though I lack the art
        to decipher it,
        no doubt the next chapter
        in my book of transformations
        is already written.
        I am not done with my changes."""

        return len(txt)

@unique
class CarBrand(Enum):
    VOLVO = "volvo"
    BMW = "bmw"
    VW = "volkswagen"

@dataclass(frozen=True)
class Car:
    type: str
    brand: CarBrand
    mileage: int
# volvo = Car(type="318i", brand=CarBrand.BMW, mileage=1000)
# volvo.brand = CarBrand.VOLVO






