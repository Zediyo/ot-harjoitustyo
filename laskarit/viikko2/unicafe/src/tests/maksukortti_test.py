import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
	def setUp(self):
		self.maksukortti = Maksukortti(1000)

	def test_luotu_kortti_on_olemassa(self):
		self.assertNotEqual(self.maksukortti, None)
        
	### t6 ###
	def test_saldo_alussa_oikein(self):
		self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

	def test_saldo_lataus(self):
		self.maksukortti.lataa_rahaa(500)
		self.assertEqual(self.maksukortti.saldo_euroina(), 15.0)

	def test_saldo_otto(self):
		self.maksukortti.ota_rahaa(500)
		self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)

	def test_saldo_otto_ylitys(self):
		self.maksukortti.ota_rahaa(1100)
		self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

	def test_saldo_otto_true(self):
		self.assertEqual(self.maksukortti.ota_rahaa(500), True)

	def test_saldo_otto_false(self):
		self.assertEqual(self.maksukortti.ota_rahaa(1100), False)
