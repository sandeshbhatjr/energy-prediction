import pytest
import pandas as pd
import numpy as np

from empredictor.features import holiday_features

def test_holidays_correspond_to_standard_ones():
	test_df = pd.DataFrame(index=pd.date_range(start='2020-01-01', end='2020-12-31'))
	test_df['holidays'] = holiday_features(test_df, ohe=False)
	returned_holiday_set = set(test_df['holidays'])
	expected_holiday_set = set([
		'75. Jahrestag der Befreiung vom Nationalsozialismus und der Beendigung des Zweiten Weltkriegs in Europa',
		'Allerheiligen, Allerhellgen', 
		'Buß- und Bettag',
		'Christi Himmelfahrt, Christi Himmelfaart',
		'Erster Mai, Staatsfeiertag, Dag vun der Aarbecht',
		'Erster Weihnachtstag, Christtag, Chrëschtdag', 
		'Europadag',
		'Fronleichnam', 
		'Heilige Drei Könige', 
		'Internationaler Frauentag',
		'Karfreitag', 
		'Mariä Empfängnis',
		'Mariä Himmelfahrt, Léiffrawëschdag', 
		'Nationalfeierdag',
		'Nationalfeiertag', 
		'Neujahr, Neijoerschdag', 
		'None',
		'Ostermontag, Ouschterméindeg', 
		'Ostersonntag',
		'Pfingstmontag, Péngschtméindeg', 
		'Pfingstsonntag',
		'Reformationstag', 
		'Tag der Deutschen Einheit', 
		'Weltkindertag',
		'Zweiter Weihnachtstag, Stefanitag, Stiefesdag',
	])
	assert expected_holiday_set.issubset(returned_holiday_set)
