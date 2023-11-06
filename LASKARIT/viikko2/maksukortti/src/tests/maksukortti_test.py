import unittest
from maksukortti import Maksukortti 

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kortti = Maksukortti(1000)

    def test_hello_world(self):
        self.assertEqual("Hello world", "Hello world")
    
    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10.00 euroa")


    def test_syo_edullisesti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_edullisesti()
        self.assertEqual(self.kortti.saldo_euroina(), 7.5)


    def test_syo_maukkaasti_vahentaa_saldoa_oikein(self):
        self.kortti.syo_maukkaasti()
        self.assertEqual(self.kortti.saldo_euroina(), 6.0)


    def test_syo_edullisesti_ei_vie_saldoa_negatiiviseksi(self):
        self.kortti.syo_edullisesti()
        self.assertEqual(self.kortti.saldo_euroina(), 7.5)


    def test_maukkaan_lounaan_syominen_ei_vie_saldoa_negatiiviseksi(self):
        self.kortti.syo_maukkaasti()
        self.assertEqual(self.kortti.saldo_euroina(), 6.0)


    def test_kortille_voi_ladata_rahaa(self):
        self.kortti.lataa_rahaa(2500)
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 35.00 euroa")


    def test_kortin_saldo_ei_ylita_maksimiarvoa(self):
        self.kortti.lataa_rahaa(20000)
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 150.00 euroa")

    def test_negatiivisen_summan_lataaminen_ei_muuta_kortin_saldoa(self):
        self.kortti.lataa_rahaa(-2000)
        self.assertEqual(str(self.kortti), "Kortilla on rahaa 10.00 euroa")
    
    def test_kortilla_pystyy_ostamaan_edullisen_lounaan_kun_kortilla_rahaa_vain_edullisen_lounaan_verran(self):
        self.kortti = Maksukortti(250)
        self.kortti.syo_edullisesti()
        self.assertEqual(self.kortti.saldo_euroina(), 0.0)

 
    def test_kortilla_pystyy_ostamaan_maukkaan_lounaan_kun_kortilla_rahaa_vain_maukkaan_lounaan_verran(self):
        self.kortti = Maksukortti(400)
        self.kortti.syo_maukkaasti()
        self.assertEqual(self.kortti.saldo_euroina(), 0.0)