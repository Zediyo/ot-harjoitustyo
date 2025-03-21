import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
	def setUp(self):
		self.kassapaate = Kassapaate()

	def test_luotu_kortti_on_olemassa(self):
		self.assertNotEqual(self.kassapaate, None)
        
	def test_kassa_alussa_oikein(self):
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
		self.assertEqual(self.kassapaate.edulliset, 0)
		self.assertEqual(self.kassapaate.maukkaat, 0)

	def test_syo_edullisesti_kateisella(self):
		self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
		self.assertEqual(self.kassapaate.edulliset, 1)

	def test_syo_edullisesti_kateisella_liian_vahan(self):
		self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(230), 230)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
		self.assertEqual(self.kassapaate.edulliset, 0)

	def test_syo_maukkaasti_kateisella(self):
		self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
		self.assertEqual(self.kassapaate.maukkaat, 1)

	def test_syo_maukkaasti_kateisella_liian_vahan(self):
		self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
		self.assertEqual(self.kassapaate.maukkaat, 0)

	def test_syo_edullisesti_kortilla(self):
		kortti = Maksukortti(300)
		self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), True)
		self.assertEqual(kortti.saldo_euroina(), 0.6)
		self.assertEqual(self.kassapaate.edulliset, 1)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

	def test_syo_edullisesti_kortilla_ei_rahaa(self):
		kortti = Maksukortti(200)
		self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)
		self.assertEqual(kortti.saldo_euroina(), 2.0)
		self.assertEqual(self.kassapaate.edulliset, 0)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

	def test_syo_maukkaasti_kortilla(self):
		kortti = Maksukortti(500)
		self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), True)
		self.assertEqual(kortti.saldo_euroina(), 1.0)
		self.assertEqual(self.kassapaate.maukkaat, 1)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

	def test_syo_maukkaasti_kortilla_ei_rahaa(self):
		kortti = Maksukortti(200)
		self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)
		self.assertEqual(kortti.saldo_euroina(), 2.0)
		self.assertEqual(self.kassapaate.maukkaat, 0)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

	def test_lataa_rahaa_kortille(self):
		kortti = Maksukortti(200)
		self.kassapaate.lataa_rahaa_kortille(kortti, 500)
		self.assertEqual(kortti.saldo_euroina(), 7.0)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

	def test_lataa_rahaa_kortille_negatiivinen(self):
		kortti = Maksukortti(200)
		self.kassapaate.lataa_rahaa_kortille(kortti, -500)
		self.assertEqual(kortti.saldo_euroina(), 2.0)
		self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

	def test_kassassa_rahaa_euroina(self):
		self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)







# Kassassa oleva rahamäärä ei muutu kortilla ostettaessa
# Kortille rahaa ladattaessa kortin saldo muuttuu ja kassassa oleva rahamäärä kasvaa ladatulla summalla