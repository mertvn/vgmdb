# -*- coding: UTF-8 -*-
import os
import datetime
import unittest

from ._rdf import TestRDF
from vgmdb import event

base = os.path.dirname(__file__)

class TestEventRDF(TestRDF):
	data_parser = lambda self,x: event.parse_event_page(x)
	outputter_type = 'event'
	def setUp(self):
		pass

	def run_m3_tests(self, graph):
		test_count_results = {
			"select ?type where { <@base#subject> rdf:type mo:ReleaseEvent . }" : 1,
			"select ?type where { <@base#subject> rdf:type schema:MusicEvent . }" : 1,
			"select ?person where { <@base#subject> event:time <@base#release_event> . }" : 1,
			"select ?date where { <@base#release_event> tl:at ?date . }" : 1,
			"select ?album where { <@base#subject> mo:release ?album . }" : 39
		}
		test_first_result = {
			"select ?date where { <@base#release_event> tl:at ?date . }" : datetime.date(2012,10,27),
			"select ?date where { <@base#subject> schema:startDate ?date . }" : datetime.date(2012,10,27),
			"select ?catalog where { ?album mo:catalogue_number ?catalog . ?album schema:name ?title . ?album schema:name \"a Tale\"@en . }" : "N/A",
			"select ?catalog where { ?album mo:catalogue_number ?catalog . ?album schema:name ?title . ?album schema:name \"AD:60\"@en . }" : "DVSP-0084",
			"select ?release_date where { ?album dcterms:created ?release_date . ?album schema:name \"a Tale\"@en . }" : datetime.date(2012,10,28),
			"select ?release_date where { ?album schema:datePublished ?release_date . ?album schema:name \"a Tale\"@en . }" : datetime.date(2012,10,28),
			"select ?publisher where { ?album schema:name \"Hiten\"@en . ?album mo:publisher ?publisher . }" : "<@baseorg/1014#subject>",
			"select ?name where { ?album mo:publisher ?publisher . ?publisher foaf:name ?name . ?album dcterms:title \"a Tale\"@en . filter(lang(?name)='en') }" : "Clinochlore"
		}

		self.run_tests(graph, test_count_results, test_first_result)

		return
	def test_m3_rdfa(self):
		graph = self.load_rdfa_data('event_m3.html')
		self.run_m3_tests(graph)
	def test_m3_rdf(self):
		graph = self.load_rdf_data('event_m3.html')
		self.run_m3_tests(graph)
