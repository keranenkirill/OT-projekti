import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_kortille_voi_ladata_rahaa(self):
        self.maksukortti.lataa_rahaa(2500)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 35.00 euroa")

    def test_saldo_vähenee_oikein_jos_rahaa_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 5.00 euroa")
    
    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_metodi_palauttaa_True_jos_rahat_riittivät_ja_muuten_False(self):
        f = self.maksukortti.ota_rahaa(1001)
        self.assertEqual(f, False)
        t = self.maksukortti.ota_rahaa(999)
        self.assertEqual(t, True)

    def test_palauttaa_oikean_muunnoksen_senteista_euroiksi(self):
        self.maksukortti.lataa_rahaa(111)
        self.maksukortti.saldo_euroina()
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 11.11 euroa")
