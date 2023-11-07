import unittest
from kassapaate import Kassapaate 
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
      self.kassassa_rahaa = Kassapaate()
      self.edulliset = Kassapaate()
      self.maukkaat = Kassapaate()


    def test_luotu_kassa_on_olemassa(self):
        self.assertNotEqual(self.kassassa_rahaa, None)


    def test_konstruktori_asettaa_kassa_saldon_oikein(self):
        self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100000)


    def test_konstruektori_asettaa_myytyjen_lounaiden_maaran_nollaan(self):
        self.assertEqual(self.edulliset.edulliset, 0)
        self.assertEqual(self.maukkaat.maukkaat, 0)



    def test_syo_edullisesti_kateisella_maksu_oikea_ei_vaihtorahaa_edullist_kasvaa(self):
      vaihtoraha = self.kassassa_rahaa.syo_edullisesti_kateisella(240)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100240)
      self.assertEqual(vaihtoraha, 0)

      self.edulliset.syo_edullisesti_kateisella(240)
      self.assertEqual(self.edulliset.edulliset, 1)


    def test_syo_edullisesti_kateisella_maksu_oikea_tulee_vaihtorahaa_edulliset_kasvaa(self):#
      vaihtoraha = self.kassassa_rahaa.syo_edullisesti_kateisella(500)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100240)
      self.assertEqual(vaihtoraha, 260)

      self.edulliset.syo_edullisesti_kateisella(500)
      self.assertEqual(self.edulliset.edulliset, 1)


    def test_syo_edullisesti_kateisella_maksu_vaaramaara_ei_tule_vaihtorahaa_edulliset_ei_kasva_palauttaa_maksun(self):
      vaihtoraha = self.kassassa_rahaa.syo_edullisesti_kateisella(50)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100000)
      self.assertEqual(vaihtoraha, 50)

      self.edulliset.syo_edullisesti_kateisella(50)
      self.assertEqual(self.edulliset.edulliset, 0)





    def test_syo_maukkaasti_kateisella_maksu_oikea_ei_vaihtorahaa_maukkaat_kasvaa(self):
      vaihtoraha = self.kassassa_rahaa.syo_maukkaasti_kateisella(400)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100400)
      self.assertEqual(vaihtoraha, 0)

      self.maukkaat.syo_maukkaasti_kateisella(400)
      self.assertEqual(self.maukkaat.maukkaat, 1)


    def test_syo_maukkaasti_kateisella_maksu_oikea_tulee_vaihtorahaa_maukkaat_kasvaa(self):
      vaihtoraha = self.kassassa_rahaa.syo_maukkaasti_kateisella(500)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100400)
      self.assertEqual(vaihtoraha, 100)

      self.maukkaat.syo_maukkaasti_kateisella(500)
      self.assertEqual(self.maukkaat.maukkaat, 1)


    def test_syo_maukkaasti_kateisella_maksu_vaaramaara_ei_tule_vaihtorahaa_maukkaat_ei_kasva_palauttaa_maksun(self):
      vaihtoraha = self.kassassa_rahaa.syo_maukkaasti_kateisella(50)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100000)
      self.assertEqual(vaihtoraha, 50)

      self.maukkaat.syo_maukkaasti_kateisella(50)
      self.assertEqual(self.maukkaat.maukkaat, 0)


    def test_syo_edullisesti_kortilla_maksu_oikea_edulliset_kasvaa(self):
      self.maksukortti = Maksukortti(240)
      self.assertEqual(self.kassassa_rahaa.syo_edullisesti_kortilla(self.maksukortti), True)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100000)

      self.edulliset.syo_edullisesti_kortilla(self.maksukortti)
      self.assertEqual(self.kassassa_rahaa.edulliset, 1)#MIKSI EI self.edulliset.edulliset....????


    def test_syo_edullisesti_kortilla_ei_tarpeeksi_varoja(self):
      self.maksukortti = Maksukortti(100)
      self.assertEqual(self.kassassa_rahaa.syo_edullisesti_kortilla(self.maksukortti), False)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100000)

      self.edulliset.syo_edullisesti_kortilla(self.maksukortti)
      self.assertEqual(self.kassassa_rahaa.edulliset, 0)#MIKSI EI self.edulliset.edulliset....????


    def test_syo_maukkaasti_kortilla_maksu_oikea_maukkaat_kasvaa(self):
      self.maksukortti = Maksukortti(400)
      self.assertEqual(self.kassassa_rahaa.syo_maukkaasti_kortilla(self.maksukortti), True)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100000)

      self.maukkaat.syo_maukkaasti_kortilla(self.maksukortti)
      self.assertEqual(self.kassassa_rahaa.maukkaat, 1)#MIKSI EI self.edulliset.edulliset....????


    def test_syo_maukkaasti_kortilla_ei_tarpeeksi_varoja(self):
      self.maksukortti = Maksukortti(100)
      self.assertEqual(self.kassassa_rahaa.syo_maukkaasti_kortilla(self.maksukortti), False)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 100000)

      self.maukkaat.syo_edullisesti_kortilla(self.maksukortti)
      self.assertEqual(self.kassassa_rahaa.maukkaat, 0)#MIKSI EI self.edulliset.edulliset....????
   
    def test_kortille_rahaa_ladattaessa_kortin_saldo_muuttuu_ja_kassassa_oleva_rahamäärä_kasvaa_ladatulla_summalla(self):
      self.maksukortti = Maksukortti(100000)
      self.kassassa_rahaa.lataa_rahaa_kortille(self.maksukortti, 50000)
      self.assertEqual(self.maksukortti.saldo, 150000)
      self.assertEqual(self.kassassa_rahaa.kassassa_rahaa, 150000)
   
